from Housing.src.config.configuration import HousingConfiguration 
from Housing.src.logger import logging 
from Housing.src.exception import HousingException 
from Housing.src.entity.config_entity import DataValidationConfig
from Housing.src.entity.artifact_entity import  DataIngestionArtifact
from Housing.src.entity.artifact_entity import DataValidationArtifacts
import os ,sys 
import pandas as pd
from Housing.src.utils.utils import read_yaml ,check_lists_match
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard 
from evidently.dashboard.tabs import DataDriftTab
import json 
from evidently.report import Report

class DataValidation():
    def __init__(self ,data_validation_config : DataValidationConfig ,
                 data_ingestion_artifact :DataIngestionArtifact) -> None:
        try:
            logging.info(f'\n\n{"*" * 20} Data Validation Step Started {"*" *20}') 
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
            print(self.data_ingestion_artifact)
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
    
    def fianal_data_validation(self):
        try:
            data_validation =False 
            data_validation = self.validate_dataset_schema() and  self.check_file_exist()
            return data_validation
        except Exception as e:
            raise HousingException(e,sys) from e

    def save_data_drift_report(self):
        try:
            profile = Profile(sections=[DataDriftProfileSection()])
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path) 


            profile.calculate(train_df ,test_df)


            
            report = json.loads(profile.json())
            #json.loads used for data to json format 
            #json.load used for file to convert into json format
        
            # print(self.data_validation_config.report_file_path )
            report_file_dir  = os.path.dirname(self.data_validation_config.report_file_path)
            os.makedirs(report_file_dir ,exist_ok= True)
            with open(self.data_validation_config.report_file_path ,'w') as report_file:
                json.dump(report ,report_file ,indent=6)

            return report

        except Exception as e:
            raise HousingException(e ,sys) from e
        

        
    def save_data_drift_report_page(self):
        try:
            dashboard = Dashboard(tabs =[DataDriftTab()])
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path) 
            dashboard.calculate(train_df ,test_df)


            dashboard_file_dir  = os.path.dirname(self.data_validation_config.report_page_file_path)
            os.makedirs(dashboard_file_dir ,exist_ok= True)


            dashboard.save(self.data_validation_config.report_page_file_path)

        except Exception as e:
            raise HousingException(e ,sys) from e

    def is_data_drift_found(self) ->bool:
        try:
            report = self.save_data_drift_report()
            self.save_data_drift_report_page()
            return True
        except Exception as e:
            raise HousingException(e ,sys) from e
        


    def initiate_data_validation(self):
        try:
            validation_status = self.fianal_data_validation()
            data_drif_found =self.is_data_drift_found()
            data_validation_artifact = DataValidationArtifacts(
                schema_file_path= self.data_validation_config.schema_file_path,
                report_file_path= self.data_validation_config.report_file_path,
                report_page_file_path= self.data_validation_config.report_page_file_path,
                is_validated= validation_status,
                message= f"We are able to validate Train and Test data successfully .Thank you Pramod Khavare"
            )
            # print("Data Validation Completed")
            logging.info(f"Data Validation is completed and result stored in DataValidationArtifacts [{data_validation_artifact}]")
            return data_validation_artifact
        except Exception as e:
            raise HousingException(e ,sys) from e