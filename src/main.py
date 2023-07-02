BLUE = '\033[34m'
RESET = '\033[0m'

print(BLUE + f"\nDrugPropertyCalculator started to work on your drug list.\n" + RESET)

# importing necessary modules
from preon.normalization import PrecisionOncologyNormalizer
from preon.drug import load_ebi_drugs
import preon

import pandas as pd
import functools

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors, Crippen, Descriptors


class DrugPropertyCalculator:
    def __init__(self):
        drug_names, drug_ids = load_ebi_drugs() 
        self.normalizer = PrecisionOncologyNormalizer().fit(drug_names, drug_ids)
        path_ebi_drugs = f"{preon.__path__[0]}/resources/ebi_drugs.csv"
        self.ebi_drugs = pd.read_csv(path_ebi_drugs, sep=";", usecols=["ChEMBL ID","Name", "Smiles", "Targets"], dtype={'ChEMBL ID': 'str', 'Name': 'str', 'Smiles':"str", 'Targets': "str"})


    def generate_drug_info(self, drug_lst, output_filename):
        '''
        (public)
        the function performed name normalization based on the ChEMBL ID of the molecule, then calculates molecular descriptors based on SMILES molecule representation

        Input: a list of original names
        Output: df of original name, ChEMBL ID and Match, normalized name (column Name), SMILES,  molecular descriptors, and rank
        '''
        df = self.__find_chembl(drug_lst)
        
        df_merged = pd.merge(df, self.ebi_drugs, on='ChEMBL ID', how='inner')
        df_merged = self.__calculate_molecule_properties(df_merged)
        df_merged['Rank'] = df_merged['Score'].rank(ascending=False, method='dense')

        df_merged.to_excel(output_filename, float_format='%.2f', index=False)

        return "Finished successfully - extracted properties are saved in the Excel file '{}'.".format(output_filename)


    def __find_chembl(self, drug_lst):
        '''
        the function is used to find ChEMBL ID via preon package - https://www.biorxiv.org/content/10.1101/2023.05.22.540912v1
        
        Input: a list of original names
        Output: df of original name, ChEMBL ID, and Match
        '''
        result = []

        for drug_name in drug_lst:
            original_name, chembl_id, match = self.normalizer.query(drug_name)
            result.append((original_name[0], chembl_id[0][0], match["match_type"]))

        return pd.DataFrame(result, columns=['Original Name', "ChEMBL ID", "Match"])
    

    def __calculate_molecule_properties(self, df):
        '''
        used to calculate molecular descriptors, rule of three and five, and score for ranking

        Input: df with SMILES notation
        Output: df with calculated molecular descriptors, rule of three and five, and calculated score
        '''
        prop_functions = {
            'HBA': rdMolDescriptors.CalcNumHBA,
            'HBD': rdMolDescriptors.CalcNumHBD,
            'tPSA': rdMolDescriptors.CalcTPSA,
            'AvgMolecularWeight': rdMolDescriptors._CalcMolWt,
            'AromaticRings': rdMolDescriptors.CalcNumAromaticRings,
            'ChiralCentres': rdMolDescriptors.CalcNumAtomStereoCenters,
            'HeavyAtoms': rdMolDescriptors.CalcNumHeavyAtoms,
            'LogP': Crippen.MolLogP,
            'Refractivity': Crippen.MolMR,
        }

        for prop_name, prop_func in prop_functions.items():
            df[prop_name] = df['Smiles'].apply(
                lambda x: self.__calc_molecule_property(x, prop_func)
            )

        df['RuleOfThree'] = df.apply(self.__passes_rule_of_three, axis=1)
        df['RuleOfFive'] = df.apply(self.__passes_rule_of_five, axis=1)
        df['Score'] = df.apply(self.__calc_score, axis=1)
        return df


    @staticmethod
    def __calc_molecule_property(smiles, prop_func):
        '''
        helper function for the calculation of the descriptor

        Input: SMILES notation and rdkit function that calculates descriptor
        Output: descriptor value 
        '''
        mol = Chem.MolFromSmiles(smiles)
        return prop_func(mol)


    @staticmethod
    def __passes_rule_of_five(row):
        '''
        checks if passes rule of the five for the drug discovery

        Input: values from the dataframe based on Lipinski's rule
        Output: boolean value

        no more than 5 hydrogen bond donors
        no more than 10 hydrogen bond acceptors
        molecular weight of less than 500 Da
        logP less than 5
        '''
        return row["AvgMolecularWeight"] < 500 and row["LogP"] <= 5 and row["HBD"] <= 5 and row["HBA"] <= 10 


    @staticmethod
    def __passes_rule_of_three(row):
        '''
        checks if passes rule of the three for the lead discovery

        Input: values from the dataframe based on Lipinski's rule
        Output: boolean value

        the molecular weight of a fragment is < 300
        the cLogP is ≤3
        the number of hydrogen bond donors is ≤ 3
        the number of hydrogen bond acceptors is ≤ 3
        '''
        return row["AvgMolecularWeight"] < 300 and row["LogP"] <= 3 and row["HBD"] <= 3 and row["HBA"] <= 3 


    @classmethod
    def __calc_score(cls, row):
        '''
        used to calclulate the score based on which the molecules are ranked
        
        Input: values from the dataframe based on Lipinski's rule
        Output: the higher value indicate the best molecular properties
        '''
        return (500-row["AvgMolecularWeight"])/500 + cls.__log_p_penalty(row["LogP"]) + (5-row["HBD"])/5 + (10-row["HBA"])/10


    @staticmethod
    def __log_p_penalty(value):
        '''
        ranking lopP values

        Input: logP value
        Output: score for the value

        https://www.sailife.com/understanding-lipinskis-rule-of-5-and-the-role-of-logp-value-in-drug-design-and-development/
        the best logP value is around 1.5 so the scoring for implemented as below due to the negative values
        '''
        if value > 1 and value <= 2:
            return 1
        elif value > -0.5 and value <= 5:
            return 0.5
        return 0

# example usage
sample_lst = ["Adenosine","Adenocard","BG8967","Bivalirudin","BAYT006267","diflucan","ibrutinib","PC-32765"]


DPC = DrugPropertyCalculator()
print(DPC.generate_drug_info(sample_lst, "result.xlsx"))
