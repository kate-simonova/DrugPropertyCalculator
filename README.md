# DrugPropertyCalculator
DrugPropertyCalculator is used to search for normalized drug names and calculate molecular descriptors.

The example input: adenocard, bg8967, diflucan, ibrutinib, bivalirudin

The example output for the following drug names:

| **Original Name** | **ChEMBL ID** | **Match** | **Name**    | **Smiles**                                                                                                                                                                                                                                                                                                                                                   | **Targets** | **HBA** | **HBD** | **tPSA** | **AvgMolecularWeight** | **AromaticRings** | **ChiralCentres** | **HeavyAtoms** | **LogP** | **Refractivity** | **RuleOfThree** | **RuleOfFive** | **Score** | **Rank** |
| ----------------- | ------------- | --------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------- | ------- | ------- | -------- | ---------------------- | ----------------- | ----------------- | -------------- | -------- | ---------------- | --------------- | -------------- | --------- | -------- |
| adenocard         | CHEMBL477     | exact     | ADENOSINE   | Nc1ncnc2c1ncn2[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O                                                                                                                                                                                                                                                                                                              | 163.0       | 9       | 4       | 139,54   | 267,25                 | 2                 | 4                 | 19             | \-1,98   | 62,74            | FALSE           | TRUE           | 0,77      | 3        |
| bg8967            | CHEMBL2103749 | exact     | BIVALIRUDIN | CC[C@H](C)[C@H](NC(=O)[C@H](CCC(=O)O)NC(=O)[C@H](CCC(=O)O)NC(=O)[C@H](Cc1ccccc1)NC(=O)[C@H](CC(=O)O)NC(=O)CNC(=O)[C@H](CC(N)=O)NC(=O)CNC(=O)CNC(=O)CNC(=O)CNC(=O)[C@@H]1CCCN1C(=O)[C@H](CCCNC(=N)N)NC(=O)[C@@H]1CCCN1C(=O)[C@H](N)Cc1ccccc1)C(=O)N1CCC[C@H]1C(=O)N[C@@H](CCC(=O)O)C(=O)N[C@@H](CCC(=O)O)C(=O)N[C@@H](Cc1ccc(O)cc1)C(=O)N[C@@H](CC(C)C)C(=O)O | 5.0         | 29      | 28      | 901,57   | 2180,32                | 3                 | 16                | 155            | \-8,12   | 539,81           | FALSE           | FALSE          | \-9,86    | 4        |
| bivalirudin       | CHEMBL2103749 | exact     | BIVALIRUDIN | CC[C@H](C)[C@H](NC(=O)[C@H](CCC(=O)O)NC(=O)[C@H](CCC(=O)O)NC(=O)[C@H](Cc1ccccc1)NC(=O)[C@H](CC(=O)O)NC(=O)CNC(=O)[C@H](CC(N)=O)NC(=O)CNC(=O)CNC(=O)CNC(=O)CNC(=O)[C@@H]1CCCN1C(=O)[C@H](CCCNC(=N)N)NC(=O)[C@@H]1CCCN1C(=O)[C@H](N)Cc1ccccc1)C(=O)N1CCC[C@H]1C(=O)N[C@@H](CCC(=O)O)C(=O)N[C@@H](CCC(=O)O)C(=O)N[C@@H](Cc1ccc(O)cc1)C(=O)N[C@@H](CC(C)C)C(=O)O | 5.0         | 29      | 28      | 901,57   | 2180,32                | 3                 | 16                | 155            | \-8,12   | 539,81           | FALSE           | FALSE          | \-9,86    | 4        |
| diflucan          | CHEMBL106     | exact     | FLUCONAZOLE | OC(Cn1cncn1)(Cn1cncn1)c1ccc(F)cc1F                                                                                                                                                                                                                                                                                                                           | 368.0       | 7       | 1       | 81,65    | 306,28                 | 3                 | 0                 | 22             | 0,74     | 70,3             | FALSE           | TRUE           | 1,99      | 1        |
| ibrutinib         | CHEMBL1873475 | exact     | IBRUTINIB   | C=CC(=O)N1CCC[C@@H](n2nc(-c3ccc(Oc4ccccc4)cc3)c3c(N)ncnc32)C1                                                                                                                                                                                                                                                                                                | 404.0       | 7       | 1       | 99,16    | 440,51                 | 4                 | 1                 | 33             | 4,22     | 126,74           | FALSE           | TRUE           | 1,72      | 2        |


A  list of commands to execute (the tool takes 1-2 to run):

```
git clone git@github.com:kate-simonova/DrugPropertyCalculator.git

cd DrugPropertyCalculator

docker build -t drug_calc_app .
docker run drug_calc_app
```
