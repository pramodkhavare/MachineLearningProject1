#This file will contain all constant required for code
#We will read config.yaml file with help of these connstant
#Variable in config.yaml = value in constant
import os ,sys 
from datetime import datetime


CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
ROOT_DIR = os.getcwd()  



CONFIG_DIR = "config"
CONFIG_FILE_NAME = "config.yaml"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR , CONFIG_DIR ,CONFIG_FILE_NAME)



#Hard Coded variable related with training pipeline
TRAINING_PIPELINE_CONFIG = 'training_pipeline_config' 
TRAINING_PIPELINE_CONFIG_PIPELINE_NAME = 'pipeline_name' 
TRAINING_PIPELINE_CONFIG_ARTIFACTS_DIR = 'artifact_dir'


#VARIABLE RELATED WITH DATA INGESTION
DATA_INGESTION_DIR_KEY = 'data_ingestion_dir'
DATA_INGESTION_CONFIG_KEY = 'data_ingestion_config'
DATASET_DOWNLOAD_URL_KEY = 'dataset_download_url'
TGZ_DOWNLOAD_DIR_KEY = 'tgz_download_dir'
RAW_DATA_DIR_KEY = 'raw_data_dir'
INGESTED_DIR_KEY = 'ingested_dir'
INGESTED_TRAIN_DIR = 'ingested_train_dir'
INGESTED_TEST_DIR = 'ingested_test_dir'

#VARIABLE RELATED WITH DATA VALIDATION
DATA_VALIDATION_DIR_KEY = 'data_validation_dir'
DATA_VALIDATION_CONFIG_KEY = 'data_validation_config'
DATA_VALIDATION_SCHEMA_DIR_KEY = 'schema_dir'
DATA_VALIDATION_SCHEMA_FILE_KEY = 'schema_file_name'
DATA_VALIDATION_REPORT_FILE_NAME_KEY = 'report_file_name' 
DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY = 'report_page_file_name'
SCHEMA_COLUMN_KEY = 'columns'
SCHEMA_TARGET_COLUMN_KEY = 'target_columns'

#VARIABLE RELATED WITH DATA TRANSFORMATION_CONFIG
TRANSFORMED_DIR_KEY = 'transformed_dir'
DATA_TRANSFORMATION_CONFIG_KEY = 'data_transformation_config'
ADD_BEDROOM_PER_ROOM_KEY = 'add_bedroom_per_room'
TRANSFORMED_TRAIN_DIR_KEY = 'transformed_train_dir'
TRANSFORMED_TEST_DIR_KEY = 'transformed_test_dir'
PREPROCESSING_DIR_KEY ='preprocessing_dir'
PREPROCESSING_OBJECT_FILE_NAME_KEY = 'preprocessing_object_file_name'

SCHEMA_FILE_COLUMN_KEY = 'columns'
SCHEMA_NUMERICAL_COLUMN_KEY = 'numerical_column'
SCHEMA_CATEGORICAL_COLUMN_KEY = 'categorical_column'
TARGET_COLUMN_KEY = 'target_columns'


#VARIABLE RELATED WITH DEFINING MODEL 
MODEL_TRAINING_CONFIG_KEY = "model_training_config"
TRAINED_MODEL_DIR_NAME_KEY = "trained_model_main_dir_name"
TRAINED_MODEL_ARTIFACTS_KEY = "trained_model_dir"
MODEL_FILE_NAME_KEY = "model_file_name"
BASE_ACCURACY = "base_accuracy"
MODEL_CONFIG_DIR = "model_config_dir"
MODEL_CONFIG_FILE_NAME_KEY = "model_config_file_name" 


#Constatn For Model Evaluation
MODEL_EVALUATION_ARTIFACT_DIR = 'model_evaluation'
MODEL_EVALUATION_CONFIG_KEY = 'model_evaluation_config'
MODEL_EVALUATION_FILE_NAME_KEY = 'model_evaluation_file_name'
BEST_MODEL_KEY = "best_model"
HISTORY_KEY = "history"
MODEL_PATH_KEY = "model_path"



#Constatn For Model Pushing
MODEL_PUSHER_CONFIG_KEY = 'model_pusher_config'
MODEL_PUSHER_CONFIG_EXPORT_DIR_PATH_KEY = 'export_dir_path'
MODEL_PUSHER_CONFIG_EXPORT_FILE_NAME = 'export_file_name'


#Constatn For Output 
EXPERIMENT_DIR_NAME="experiment"
EXPERIMENT_FILE_NAME="experiment.csv"