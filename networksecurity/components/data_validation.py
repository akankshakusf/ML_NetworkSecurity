#import packages
from scipy.stats import ks_2samp
import pandas as pd
import os, sys

## Configuration of the Data Ingestion & validation Config 
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file

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
        
        