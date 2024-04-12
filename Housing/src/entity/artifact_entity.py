#We will store output into these tuples

from collections import namedtuple


DataIngestionArtifact = namedtuple('DataIngestionArtifact',
['train_file_path' ,'test_file_path' ,'is_ingested' ,'message'] )

DataValidationArtifacts = namedtuple(
    'DataValidationArtifacts' ,
    ["schema_file_path" , "report_file_path" ,'report_page_file_path' ,"is_validated" ,"message"]
)

DataTransformationArtifact =namedtuple(
    'DataTransformationArtifact' ,
    ['is_transformed' ,"message" ,"transformed_train_file_path" ,"transformed_test_file_path",
    "preprocessing_obj_file_path"]
)

ModelTrainingArtifacts = namedtuple(
    'ModelTrainingArtifacts' , ['trained_model_file_path' ,'train_rmse' ,'train_accuracy' ,'test_rmse' ,'test_accuracy' ,'model_accuracy']
)


ModelEvaluationArtifact = namedtuple(
    "ModelEvaluationArtifact", ["is_model_accepted", "evaluated_model_path"]
)

ModelPusherArtifacts = namedtuple(
    'ModelPusherArtifacts' ,["is_model_pushed" ,"export_model_file_path"]
)