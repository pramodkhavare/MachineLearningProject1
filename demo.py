from Housing.src.pipeline.training_pipeline import Pipeline 
from Housing.src.exception import HousingException
from Housing.src.logger import logging
from Housing.src.config.configuration import HousingConfiguration
from Housing.src.components.data_validation import DataValidation
from Housing.src.components.data_ingestion import DataIngestion
def main():
    try:
        housing_configuration = HousingConfiguration()
        data_ingestion_config = housing_configuration.get_data_ingestion_config()

        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        data_validation_config = housing_configuration.get_data_validation_config()
        data_validation = DataValidation(data_validation_config , data_ingestion_artifact)
        data_validation.validate_dataset_schema()

    except Exception as e:
        logging.error(f"{e}")
        print(e)

if __name__ == "__main__":
    main()