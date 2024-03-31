from Housing.src.pipeline.training_pipeline import Pipeline 
from Housing.src.exception import HousingException
from Housing.src.logger import logging
from Housing.src.config.configuration import HousingConfiguration
from Housing.src.components.data_validation import DataValidation
from Housing.src.components.data_ingestion import DataIngestion
from Housing.src.components.data_transformation import DataTransformation
from Housing.src.entity.artifact_entity import DataIngestionArtifact ,DataValidationArtifacts ,DataTransformationArtifact
def main():
    try:
        
        pipeline = Pipeline()
        data_ingestion_artifacts = pipeline.start_data_ingestion()
        data_validation_artifacts = pipeline.start_data_validation(
            data_ingestion_artifacts=data_ingestion_artifacts
        )
        data_transformation_artifacts = pipeline.start_data_transformation(
            data_ingestion_artifacts=data_ingestion_artifacts ,
            data_validation_artifact= data_validation_artifacts
        )
        




        # housing_configuration = HousingConfiguration()
        # data_validation_config = housing_configuration.get_data_validation_config()
        # data_ingestion_config = housing_configuration.get_data_ingestion_config()
        # data_transformation_config = housing_configuration.get_data_transformation_config()
        # print(data_transformation_config)
        # print("Completed")
        # data_transformation =DataTransformation(
        #     data_transformation_config=data_transformation_config ,
        #     data_ingestion_artifact=
        # )

        # data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        # data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
    
        # data_validation = DataValidation(data_validation_config , data_ingestion_artifact)
        # data_validation.validate_dataset_schema()
        # print("Completed")

    except Exception as e:
        logging.error(f"{e}")
        print(e)

if __name__ == "__main__":
    main()