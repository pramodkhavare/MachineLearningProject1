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



DATA_INGESTION_CONFIG_KEY = 'data_ingestion_config'
DATA_INGESTION_DIR_KEY = 'data_ingestion_dir'
DATASET_DOWNLOAD_URL_KEY = 'dataset_download_url'
TGZ_DOWNLOAD_DIR_KEY = 'tgz_download_dir'
RAW_DATA_DIR_KEY = 'raw_data_dir'
INGESTED_DIR_KEY = 'ingested_dir'
INGESTED_TRAIN_DIR = 'ingested_train_dir'
INGESTED_TEST_DIR = 'ingested_test_dir'


DATA_TRANSFORMATION_CONFIG_KEY = 'data_transformation_config'
ADD_BEDROOM_PER_ROOM_KEY = 'add_bedroom_per_room'
TRANSFORMED_DIR_KEY = 'transformed_dir'
TRANSFORMED_TRAIN_DIR = 'transformed_train_dir'
TRANSFORMED_TEST_DIR = 'transformed_test_dir'
PREPROCESSED_DIR_KEY ='preprocessing_dir'
PREPROCESSED_OBJECT_FILE_PATH = 'preprocessed_object_file_path'