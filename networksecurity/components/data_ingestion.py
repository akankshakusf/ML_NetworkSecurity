#import packages
import os
import sys
import pandas as pd
import numpy as np
import pymongo
from sklearn.model_selection import train_test_split
from typing import List

#for logging and exception handling 
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


## Configuration of the Data Ingestion Config 
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

#to read data from mongo db set the load dot env file
from dotenv import load_dotenv
#initialize the environment
load_dotenv()

#finally, read Data from Mongo DB
MONGO_DB_URL=os.getenv("MONGO_DB_URL")

class DataIngestion:
    # this data ingestion is being called from config_entity.py
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    #first we need function that bring dataframe from mongo db
    def export_collection_as_dataframe(self):
        '''
        Read data from mongo db
        '''
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name

            # Create a MongoDB client using the connection URL
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            # Access the collection(tbl) from the database
            collection=self.mongo_client[database_name][collection_name]

            df= pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df=df.drop(columns=['_id'], axis=1)

            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys) 

    def export_data_into_feature_store(self,dataframe:pd.DataFrame):
        try:
            # this data ingestion is being called from config_entity.py
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            #get directory name
            dir_path=os.path.dirname(feature_store_file_path)
            #create directory(folder)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe            
        except Exception as e:
            raise NetworkSecurityException(e,sys) 
        

    def split_data_as_train_test(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set=train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            
            logging.info("Performed train test split on the dataframe")

            logging.info("Exited split_data_as_train_test method of Data Ingestion Class")

            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info(f"Exporting train and test file path")

            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)

            logging.info(f"Exported Train and test file path")

        except Exception as e:
            raise NetworkSecurityException(e,sys)      
    
        
    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_collection_as_dataframe()
            dataframe=self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            dataingestionartifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                        test_file_path=self.data_ingestion_config.testing_file_path)
            
            return dataingestionartifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)

            
