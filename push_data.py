import os
import sys
import json
from dotenv import load_dotenv
# Load environment variables from .env file into the system environment
load_dotenv()

# Retrieve MongoDB connection URL from environment variables
MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

# Get the path to the certificate authority file
import certifi
ca=certifi.where()


import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging 


class NetworkDataExtract():
    def __init__(self):
        try:
            pass # Constructor that does nothing but could be a place for initialization code
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json_converter(self,file_path):
        try:
            # Read data from CSV file at given file_path
            data=pd.read_csv(file_path)
            # Reset index for the DataFrame
            data.reset_index(drop=True,inplace=True)
            # Convert DataFrame to JSON and then to a list of dictionaries
            records=list(json.loads(data.T.to_json()).values())
            # Return the list of dictionaries containing the data
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_mongo_db(self,records,database,collection):
        try:
            
            self.database=database
            self.collection=collection
            self.records=records

            # Create a MongoDB client using the connection URL
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            # Access the database from the client
            self.database = self.mongo_client[database]
            # Access the collection from the database
            self.collection = self.database[collection]

            # Insert the records into the collection
            self.collection.insert_many(self.records)
            # Return the number of records inserted
            return(len(self.records))
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

if __name__=='__main__':
    # Path to the CSV file containing data
    FILE_PATH="Network_Data\phisingData.csv"
    DATABASE="NetworkDB"
    Collection="NetworkData"
    # Create an instance 
    networkobj=NetworkDataExtract()
    # Convert CSV data to JSON format
    records=networkobj.csv_to_json_converter(file_path=FILE_PATH)
    print(records)
    # Insert records into MongoDB
    no_of_records=networkobj.insert_data_mongo_db(records,DATABASE,Collection)
    print(no_of_records)


    

