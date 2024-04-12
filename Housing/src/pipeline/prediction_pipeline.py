from Housing.src.constant import *
from Housing.src.config.configuration import * 
from Housing.src.utils.utils import *
from Housing.src.logger import logging 
from Housing.src.exception import HousingException 




    
class HousingData():
    def __init__(self ,
                 longitude :float,
                 lattitude :float,
                 house_median_age:float,
                 total_rooms:float,
                 total_bedrooms:float,
                 population :float,
                 households :float,
                 median_income :float,
                 ocean_proximity ,
                 median_house_value: float = None
                 ):
        self.longitude =longitude 
        self.lattitude =lattitude
        self.house_median_age =house_median_age 
        self.total_rooms =total_rooms
        self.total_bedrooms =total_bedrooms
        self.population =population
        self.households = households 
        self.median_income =median_income 
        self.ocean_proximity =ocean_proximity
        self.median_house_value =median_house_value
        
        
    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = self.get_data_as_Dict()
            housing_data_dict = pd.DataFrame(custom_data_input_dict)
            logging.info('Data Gathered')
            return housing_data_dict
        except Exception as e:
            raise HousingException(e ,sys) from e
        
    def get_data_as_Dict(self):
        try:
            input_data = {
                'longitude' : [self.longitude],
                'latitude' :[self.lattitude],
                'housing_median_age' :[self.house_median_age],
                'total_rooms' :[self.total_rooms],
                'total_bedrooms' : [self.total_bedrooms],
                'population' : [self.population],
                'households' : [self.households],
                'median_income' : [self.median_income],
                'ocean_proximity' : [self.ocean_proximity]
            }
            return input_data
        except Exception as e:
            raise HousingException(e ,sys) from e
    
class Prediction():
    def __init__(self ,model_dir:str ,preprocessor_dir:str):
        try:
            #We will pass saved_models folde path as input 
            self.model_dir = model_dir 
            self.preprocessor_dir = preprocessor_dir

        except Exception as e:
            raise HousingException(e ,sys) from e
        
    def get_latest_model_path(self):
        try:
            # Get list of folders in the specified directory
            folder_list = os.listdir(self.model_dir)
            # Sort the folders by name (which represents the date)
            sorted_folders = sorted(folder_list, reverse=True)

            # Extract the newest folder (first element after sorting)
            newest_folder = sorted_folders[0] 
            filename = os.listdir(os.path.join(self.model_dir ,newest_folder))[0]
            file_path = os.path.join(self.model_dir ,newest_folder ,filename)
            print(file_path)
            return file_path
        except Exception as e:
            raise HousingException(e, sys) from e
        
    def get_latest_preprocessor_path(self):
        try:
            folder_path =self.preprocessor_dir
            folder_list = os.listdir(folder_path)
            sorted_folders = sorted(folder_list, reverse=True)
            newest_folder = sorted_folders[0] 
            preprocesssor_dir = os.listdir(os.path.join(folder_path,newest_folder))[0]
            preprocessor = os.listdir(os.path.join(folder_path,newest_folder ,preprocesssor_dir))[0]
            preprocessor_path = os.path.join(folder_path ,newest_folder ,preprocesssor_dir,preprocessor)

            return preprocessor_path

        except Exception as e:
            raise HousingException(e, sys) from e 

    
    def prediction(self ,features):
        try:
            logging.info("Prediction Has Been Started")
            model_path = self.get_latest_model_path()
            preprocessor_path = self.get_latest_preprocessor_path()
            print(model_path)
            model= load_object(model_path)
            preprocessor = load_object(preprocessor_path)
            features = preprocessor.transform(features)
            median_house_value = model.predict(features) 

            return median_house_value
        except Exception as e:
            logging.info('Unable to predict output')
            raise(HousingException(e ,sys)) from e