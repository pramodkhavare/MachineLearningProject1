from Housing.src.exception import HousingException 
from Housing.src.logger import logging
import sys ,os 
from ensure import ensure_annotations
from box import ConfigBox
import yaml

@ensure_annotations
def read_yaml(yaml_file_path :str):
    try:
        """
        Read yaml file and return content as dictionary
        yaml_file_path :str
        """
        with open(yaml_file_path , 'r') as file:
            content =  yaml.safe_load(file)
            return content

    except Exception as e:
        logging.info(f'unable to read Yaml file at {yaml_file_path}')
        raise HousingException(e ,sys)
    
