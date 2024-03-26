from Housing.src.exception import HousingException 
from Housing.src.logger import logging
import sys ,os 
from ensure import ensure_annotations
import yaml
import numpy as np
import pandas as pd
import dill

def write_yaml(file_path:str ,data:dict):
    """
    This function willl create Yaml file and save data in that file
    """
    try:
        os.makedirs(os.path.dirname(file_path) ,exist_ok=True)
        with open(file_path ,'w') as yaml_file:
            if data is not None :
                yaml.dump(data ,yaml_file)

    except Exception as e:
        logging.info(f'unable to create Yaml file at {file_path}')
        raise HousingException(e ,sys)
    

def read_yaml(yaml_file_path:str):
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
    


def check_lists_match(list1, list2):
    # Check if the lengths of the lists are different
    if len(list1) != len(list2):
        return False
    
    # Compare each element of the lists
    for i in range(len(list1)):
        if list1[i] != list2[i]:
            return False  # If any element doesn't match, return False
    
    return True

def save_numpy_array(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise HousingException(e, sys) from e
     

def load_array(file_path:str)->np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path ,'rb') as file:
            return np.load(file)

    except Exception as e:
        raise HousingException(e,sys)

    
def save_object(file_path:str,obj):
    """
    file_path: str
    obj: Any sort of object
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise HousingException(e,sys) from e


def load_object(file_path:str):
    """
    file_path: str
    """
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise HousingException(e,sys) from e

    
@ensure_annotations
def get_csv_dataset(file_path):
        try:
            dataframe = pd.read_csv(file_path)

            return dataframe

        except Exception as e:
            raise HousingException(e ,sys) from e 