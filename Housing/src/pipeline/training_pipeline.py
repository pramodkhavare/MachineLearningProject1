from Housing.src.config.configuration import HousingConfiguration
from Housing.src.components.data_ingestion import DataIngestion
from Housing.src.components.data_validation import DataValidation
from Housing.src.components.data_transformation import DataTransformation
from Housing.src.exception import HousingException
from Housing.src.entity.artifact_entity import DataIngestionArtifact ,DataValidationArtifacts ,DataTransformationArtifact
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
            
             
        except Exception as e:
            raise HousingException(e ,sys) from e
        

    def start_data_validation(self,data_ingestion_artifacts: DataIngestionArtifact)->DataValidationArtifacts:
        try:
            data_validation_config = self.config.get_data_validation_config()
            data_ingestion_artifact =data_ingestion_artifacts
            data_validation =DataValidation(data_validation_config=data_validation_config ,
                                            data_ingestion_artifact= data_ingestion_artifact)

            data_validation_output = data_validation.initiate_data_validation() 
            return data_validation_output
        except Exception as e:
            raise HousingException(e ,sys) from e
          

    def start_data_transformation(self ,data_ingestion_artifacts:DataIngestionArtifact ,data_validation_artifact:DataValidationArtifacts) ->DataTransformationArtifact:
        try:
            data_transformation_config = self.config.get_data_transformation_config()
            data_ingestion_artifact = data_ingestion_artifacts
            data_validation_artifact= data_validation_artifact
            data_transformation_artifacts = DataTransformation(
                data_transformation_config=data_transformation_config ,
                data_ingestion_artifact= data_ingestion_artifact ,
                data_validation_artifact= data_validation_artifact
            )
            data_transformation_artifacts.initiated_data_transformation()
            return data_transformation_artifacts
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
        