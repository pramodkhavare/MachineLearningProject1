from Housing.src.config.configuration import HousingConfiguration
from Housing.src.components.data_ingestion import DataIngestion
from Housing.src.components.data_validation import DataValidation
from Housing.src.exception import HousingException
from Housing.src.entity.artifact_entity import DataIngestionArtifact ,DataValidationArtifacts
from Housing.src.logger import logging
import os ,sys
class Pipeline:
    def __init__(self ,config:HousingConfiguration=HousingConfiguration()):
        try:
            self.config = config 

        except Exception as e:
            raise HousingException(e ,sys) from e 

    def start_data_ingestion(self) ->DataIngestionArtifact:
        try:
            data_ingestion_config = self.config.get_data_ingestion_config()
        
            data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
            data_ingestion_output = data_ingestion.initiate_data_ingestion()
            return data_ingestion_output
            print('Data Ingestion Completed')
             
        except Exception as e:
            raise HousingException(e ,sys) from e
        

    def start_data_validation(self)->DataValidationArtifacts:
        try:
            data_validation_config = self.config.get_data_validation_config()
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation =DataValidation(data_validation_config=data_validation_config ,
                                            data_ingestion_artifact= data_ingestion_artifact)

            data_validation_output = data_validation.initiate_data_validation() 
            return data_validation_output
        except Exception as e:
            raise HousingException(e ,sys) from e
          

    def start_data_transformation(self):
        try:
            pass 
        except Exception as e:
            raise HousingException(e ,sys) from e  

      

    def start_model_training(self):
        try:
            pass 
        except Exception as e:
            raise HousingException(e ,sys) from e  


    def start_model_evaluation(self):
        try:
            pass 
        except Exception as e:
            raise HousingException(e ,sys) from e  
        
    def model_pusher(self):
        try:
            pass 
        except Exception as e:
            raise HousingException(e ,sys) from e
        

    def run_pipeline(self):
        try:
            data_ingestion_artifacts = self.start_data_ingestion()

        except Exception as e:
            raise HousingException(e ,sys) from e 
        