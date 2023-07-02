# Use an official Ubuntu base image
FROM ubuntu:20.04

# Set the timezone
ENV TZ=Europe/Prague
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install Python and other necessary dependencies
RUN apt-get update && apt-get install python3.9 python3.9-distutils python3-pip -y

# Set the working directory in the container
RUN mkdir /app
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN python3.9 -m pip install --no-cache-dir -r requirements.txt

# Create directory
RUN mkdir /usr/local/lib/python3.9/dist-packages/preon/resources

# Copy the application code into the container
COPY src/main.py .
COPY data/ebi_drugs.csv.gz /usr/local/lib/python3.9/dist-packages/preon/resources/

# Unzip the database file
RUN gunzip /usr/local/lib/python3.9/dist-packages/preon/resources/ebi_drugs.csv.gz

# Specify the command to run your application
CMD python3.9 main.py && printf  "\nYou have \e[31m\e[1m1 minute\e[0m to copy the output file from docker via command: \e[35mdocker cp $(cat /etc/hostname):/app/result.xlsx .\e[0m \n" && sleep 1m