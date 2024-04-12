from Housing.src.pipeline.training_pipeline import Pipeline 
from Housing.src.exception import HousingException
from Housing.src.logger import logging
from Housing.src.config.configuration import HousingConfiguration
from Housing.src.components.data_validation import DataValidation
from Housing.src.components.data_ingestion import DataIngestion
from Housing.src.components.data_transformation import DataTransformation
from Housing.src.components.model_trainer import *
from Housing.src.entity.model_factory import get_sample_model_config_yaml_file
from Housing.src.entity.artifact_entity import DataIngestionArtifact ,DataValidationArtifacts ,DataTransformationArtifact
def main():
    try:
        
        pipeline = Pipeline(config=HousingConfiguration())
        pipeline.run()

    except Exception as e:
        logging.error(f"{e}")

        

if __name__ == "__main__":
    main()