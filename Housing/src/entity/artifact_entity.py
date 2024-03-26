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