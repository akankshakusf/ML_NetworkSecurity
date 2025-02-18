#import packages
from scipy.stats import ks_2samp
import pandas as pd
import os, sys

## Configuration of the Data Ingestion & validation Config 
from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file
~

#for logging and exception handling 
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class DataValidation:
    def __init__(self,data_ingestion_artifacts:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        
        try:
            self.data_ingestion_artifacts=data_ingestion_artifacts
            self.data_validation_config=data_validation_config
            self._schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys) 
        
    # Define methods that operate independently of class instances and class state.
    @staticmethod
    #lets read the file that we got from the artifacts
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        
        except Exception as e:
            raise NetworkSecurityException(e,sys) 
        
    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns=len(self._schema_config)
            #check how many number of columns we got from schema
            logging.info(f"Required number of columns:{number_of_columns}")

            #check how many number of columns we got from dataframe
            logging.info(f"Dataframe has columns:{len(dataframe.columns)}")

            if len(dataframe.columns)==number_of_columns:
                return True
            return False

        except Exception as e:
            raise NetworkSecurityException(e,sys) 
        

    def check_numerical_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            numerical_columns = dataframe.select_dtypes(include=['number']).columns
            if len(numerical_columns) > 0:
                logging.info(f"Numerical columns found: {numerical_columns}")
                return True
            else:
                logging.info("No numerical columns found in the dataframe.")
                return False
        except Exception as e:
            raise NetworkSecurityException(e, sys)         
        
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path=self.data_ingestion_artifacts.trained_file_path
            test_file_path=self.data_ingestion_artifacts.test_file_path

            #we need to read the data that comes in 
            train_dataframe=DataValidation.read_data(train_file_path)
            test_dataframe=DataValidation.read_data(test_file_path)

            #after validating len(dataframe.columns)==number_of_columns 

            #check status if no. columns match or not match show error accordingly 
            #checking for train
            status=self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message=f"{error_message}Train dataframe does not contain all columns.\n"
            
            #checking for test
            status=self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message=f"{error_message}Test dataframe does not contain all columns.\n"

             # Check for numerical columns in train and test dataframes
            train_numerical_status = self.check_numerical_columns(dataframe=train_dataframe)
            test_numerical_status = self.check_numerical_columns(dataframe=test_dataframe)

            if not train_numerical_status:
                error_message = f"{error_message}Train dataframe does not contain numerical columns.\n"
            if not test_numerical_status:
                error_message = f"{error_message}Test dataframe does not contain numerical columns.\n"


            

        except Exception as e:
            raise NetworkSecurityException(e,sys) 
        


        