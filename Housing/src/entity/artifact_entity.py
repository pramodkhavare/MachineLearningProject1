#We will store output into these tuples

from collections import namedtuple


DataIngestionArtifact = namedtuple('DataIngestionArtifact',
['train_file_path' ,'test_file_path' ,'is_ingested' ,'message'] )

DataValidationArtifacts = namedtuple(
    'DataValidationArtifacts' ,
    []
)