import os ,sys 
from datetime import datetime
#We are going to store information but not in classes but tuple
# We can use other options like list ,dict (dict is mutable)
from collections import namedtuple



def get_time_stamp():
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

#
TrainingPipelineConfig = namedtuple('TrainingPipelineConfig' ,
                                    ['artifact_dir'])


#Info related with Data Ingestion
DataIngestionConfig = namedtuple("DataIngestionConfig" ,
['dataset_download_url' , 'tgz_download_dir' ,'raw_data_dir' , 'ingested_dir','ingested_train_dir' ,'ingested_test_dir'])

#Info related with Data Validation
DataValidationConfig= namedtuple("DataValidationConfig" ,
['schema_file_path' ,'report_file_path' ,'report_page_file_path' ])

#Info Related with Data Transformation
DataTransfrmationConfig = namedtuple('DataTransfrmationConfig' ,
['add_bedroom_per_room' ,'transformed_dir' ,'transformed_train_dir' ,'transformed_test_dir' 
 ,'preprocessed_object_dir' ,'preprocessing_object_file_name'])

#Info Related with Model Training
ModelTrainingConfig = namedtuple('ModelTrainingConfig' ,
                    ['trained_model_file_path' ,'model_file_name' ,'base_accuracy' ,'model_config_file_path'])


#Info Related with Model Evaluation use test data and compare with base model
ModelEvaluationConfig = namedtuple("ModelEvaluationConfig" ,
["model_evaluation_file_path"])


#Production model saved in these folder and if your model performing better then that model will save at these location
ModelPusherConfig = namedtuple('ModelPusherConfig' ,
                               ['export_dir_path' ,'export_file_path'])

