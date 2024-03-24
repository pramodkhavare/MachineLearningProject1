from Housing.src.entity.config_entity import (DataIngestionConfig ,DataTransfrmationConfig ,
                                              DataValidationConfig ,ModelTrainingConfig ,
                                              ModelEvaluationConfig , ModelPusherConfig ,TrainingPipelineConfig)

from Housing.src.utils.utils import read_yaml 
from Housing.src.constant import *
from Housing.src.exception import HousingException
from Housing.src.logger import logging
class HousingConfiguration():
    def __init__(self , config_file_path = CONFIG_FILE_PATH ,
                 current_time_stamp = CURRENT_TIME_STAMP):
        try:
            self.config_info = read_yaml(yaml_file_path= config_file_path)
            self.training_pipeline_config = self.get_training_pipeline_config()
            self.time_stamp = current_time_stamp

        except Exception as e:
            raise HousingException (e ,sys)


        

    def get_data_ingestion_config(self) ->DataIngestionConfig:
        try:
            config = self.config_info[DATA_INGESTION_CONFIG_KEY]

            data_ingestion_dir_key = os.path.join(
                self.training_pipeline_config.artifact_dir ,
                config[DATA_INGESTION_DIR_KEY] ,
                self.time_stamp
            )

            dataset_download_url = config[DATASET_DOWNLOAD_URL_KEY]

            tgz_download_dir = os.path.join(
                self.training_pipeline_config.artifact_dir  ,
                data_ingestion_dir_key ,
                config[TGZ_DOWNLOAD_DIR_KEY]
            ) 

            raw_data_dir = os.path.join(
                self.training_pipeline_config.artifact_dir ,
                data_ingestion_dir_key ,
                config[RAW_DATA_DIR_KEY]

            )

            ingested_dir = os.path.join(
                self.training_pipeline_config.artifact_dir ,
                data_ingestion_dir_key ,
                config[INGESTED_DIR_KEY]
            )

            ingested_train_dir = os.path.join(
                ingested_dir ,
                config[INGESTED_TRAIN_DIR]
            )

            ingested_test_dir = os.path.join(
                ingested_dir ,
                config[INGESTED_TEST_DIR]
            )
        
        
            data_ingestion_config= DataIngestionConfig(
                dataset_download_url= dataset_download_url,
                tgz_download_dir= tgz_download_dir,
                raw_data_dir= raw_data_dir,
                ingested_dir= ingested_dir,
                ingested_train_dir= ingested_train_dir,
                ingested_test_dir= ingested_test_dir
            )
            logging.info("Data ingestion config step completed")
            return data_ingestion_config

        except Exception as e:
            raise HousingException (e ,sys) from e 
        

    def get_data_validation_config(self) ->DataValidationConfig:
        try:
            config = self.config_info[DATA_VALIDATION_CONFIG_KEY]
            data_validation_dir_key = os.path.join(
                self.training_pipeline_config.artifact_dir ,
                config[DATA_VALIDATION_DIR_KEY] ,
                self.time_stamp
            )

            schema_file_path = os.path.join(
                ROOT_DIR,
                config[DATA_VALIDATION_SCHEMA_DIR_KEY] ,
                config[DATA_VALIDATION_SCHEMA_FILE_KEY]
            )

            report_file_path =  os.path.join(
                self.training_pipeline_config.artifact_dir ,
                data_validation_dir_key ,
                config[DATA_VALIDATION_REPORT_FILE_NAME_KEY]
            )

            report_page_file_path = os.path.join(
                self.training_pipeline_config.artifact_dir ,
                data_validation_dir_key,
                config[DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY]
            )

            data_validation_config = DataValidationConfig(
                schema_file_path = schema_file_path ,
                report_file_path= report_file_path ,
                report_page_file_path= report_page_file_path
            )

            print(data_validation_config)

            return data_validation_config
                    
        except Exception as e:
            raise HousingException(e,sys) from e 







    def get_data_transformation_config(self) ->DataTransfrmationConfig:
        try:
            config = self.config_info[DATA_TRANSFORMATION_CONFIG_KEY]

            add_bedroom_per_room = config[ADD_BEDROOM_PER_ROOM_KEY]
            transformed_dir = os.path.join(
                self.training_pipeline_config.artifact_dir ,
                config[TRANSFORMED_DIR_KEY],
                self.time_stamp
            )
            transformed_train_dir = os.path.join(
                transformed_dir ,
                config[TRANSFORMED_TRAIN_DIR]
            )
            transformed_test_dir = os.path.join(
                transformed_dir ,
                config[TRANSFORMED_TEST_DIR]
            )
            preprocessed_object_dir = os.path.join(
                transformed_dir ,
                config[PREPROCESSED_DIR_KEY]
            )
            data_transformation_config = DataTransfrmationConfig(
                add_bedroom_per_room = add_bedroom_per_room ,
                transformed_dir= transformed_dir ,
                transformed_train_dir = transformed_train_dir ,
                transformed_test_dir = transformed_test_dir ,
                preprocessed_object_dir = preprocessed_object_dir
            )

            return data_transformation_config
        
        except Exception as e:
            raise HousingException (e ,sys) from e

    


    def get_model_trainer_config(self) ->ModelTrainingConfig:

        try:
            # self.config_info[]
            # trainer_model_file_path = 

        #     model_trainer_config=ModelTrainingConfig(
        #     trained_model_file_path= ,
        #     model_file_name= ,
        #     base_accuracy= 0.6
        # ) 
            pass

        except Exception as e:
            raise HousingException (e ,sys)
        
    def get_model_evaluation_config(self) ->ModelEvaluationConfig:
        pass 

    def get_model_pusher_config(self) ->ModelPusherConfig:
        pass

    def get_training_pipeline_config(self) ->TrainingPipelineConfig:
        try:
            config = self.config_info[TRAINING_PIPELINE_CONFIG]
            artifact_dir  = os.path.join(ROOT_DIR 
                                         ,config[TRAINING_PIPELINE_CONFIG_ARTIFACTS_DIR])
            
            training_pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)
            return training_pipeline_config

        except Exception as e:
            raise HousingException (e ,sys)

