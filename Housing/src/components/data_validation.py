from Housing.src.config.configuration import HousingConfiguration 
from Housing.src.logger import logging 
from Housing.src.exception import HousingException 
from Housing.src.entity.config_entity import DataValidationConfig
from Housing.src.entity.artifact_entity import  DataIngestionArtifact
import os ,sys 
import pandas as pd
from Housing.src.utils.utils import read_yaml ,check_lists_match


class DataValidation():
    def __init__(self ,data_validation_config : DataValidationConfig ,
                 data_ingestion_artifact :DataIngestionArtifact) -> None:
        try:
            logging.info(f'{"*" * 20} Data Validation Step Started {"*" *20}') 
            self.data_validation_config  = data_validation_config 
            self.data_ingestion_artifact = data_ingestion_artifact

        except Exception as e:
            raise HousingException(e ,sys) from e
        
    def check_file_exist(self)->bool:
        try:
            logging.info('Checking Train and Test file exist or not')
            is_train_file_exist = False 
            is_test_file_exist = False 

            train_file_path = self.data_ingestion_artifact.train_file_path 
            test_file_path = self.data_ingestion_artifact.test_file_path

            is_train_file_exist = os.path.exists(train_file_path) 
            is_test_file_exist = os.path.exists(test_file_path)

            is_available = is_test_file_exist and is_train_file_exist 
            logging.info(f"Checked Train and Test file exist or not : [{is_available}]")
            if not is_available:
                training_file = self.data_ingestion_artifact.train_file_path 
                testing_file = self.data_ingestion_artifact.test_file_path 
                logging.info("We Cant procees because train/test file is not available")
                raise Exception(f"Training file:[{training_file}] or \
                                 Testing File :[{testing_file}] is not available")
            return is_available
        
        except Exception as e:
            raise HousingException(e ,sys) from e
        
    def validate_dataset_schema(self) -> bool:
        try:
            logging.info('Checking columns of train and test file')
            validation_status = False 

            schema_file_path = self.data_validation_config.schema_file_path
            schema_file = read_yaml(schema_file_path)
            expecting_columns = list(schema_file['columns'].keys())

            train_dataframe = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_dataframe = pd.read_csv(self.data_ingestion_artifact.test_file_path )


            actual_train_columns = list(train_dataframe.columns)
            actual_test_columns = list(test_dataframe.columns)

            train_validation_status =check_lists_match(actual_train_columns ,expecting_columns)
            test_validation_status = check_lists_match(actual_test_columns ,expecting_columns)


            validation_status = train_validation_status and test_validation_status
            logging.info(f'Checked columns of train and test file : [{validation_status}]')
            if not validation_status:
                logging.info("We cant procees because there is mismatch in required columns and available columns")
                raise Exception(f"Expected and actual column mismatch")
            
            
            return validation_status  
             
        except Exception as e:
            raise HousingException(e ,sys) from e

        
    def initiate_data_validation(self):
        try:
            is_available = self.check_file_exist()
            validation_status = self.validate_dataset_schema()
        except Exception as e:
            raise HousingException(e ,sys) from e