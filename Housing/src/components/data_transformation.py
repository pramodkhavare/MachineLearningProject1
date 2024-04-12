from Housing.src.config.configuration import HousingConfiguration 
import os ,sys 
from Housing.src.entity.config_entity import DataTransfrmationConfig  
from Housing.src.entity.artifact_entity import  DataIngestionArtifact ,DataValidationArtifacts ,DataTransformationArtifact
from Housing.src.logger import logging 
from Housing.src.exception import HousingException 
from sklearn.base import BaseEstimator,TransformerMixin
import pandas as pd 
import numpy as np 
from sklearn.preprocessing import StandardScaler ,OneHotEncoder 
from sklearn.pipeline import Pipeline 
from sklearn.compose import ColumnTransformer
from Housing.src.utils.utils import read_yaml ,save_numpy_array  ,save_object
from Housing.src.constant import *
from sklearn.impute import SimpleImputer

COLUMN_TOTAL_ROOMS = 'total_rooms' 
COLUMN_POPULATION = 'population'
COLUMN_TOTAL_BEDROOMS = 'total_bedrooms'
COLUMN_HOUSEHOLDS = 'households' 


class FeatureGenerator(BaseEstimator ,TransformerMixin):
    def __init__(self ,add_bedroom_per_room =True ,
                 total_room_ix = 3,
                 population_ix = 5 ,
                 households_ix = 6 ,
                 total_bedroom_ix = 4 ,
                 columns =None):
        """
        total_room_ix,population_ix ,households_ix ,total_bedroom_ix are id of these column inside dataset
        """ 

        try:
            
            self.columns = columns 
            if self.columns is not None:
                total_room_ix =self.columns.index(COLUMN_TOTAL_ROOMS)
                population_ix = self.columns.index(COLUMN_POPULATION)
                total_bedroom_ix = self.columns.index(COLUMN_TOTAL_BEDROOMS)
                households_ix = self.columns.index(COLUMN_HOUSEHOLDS)
            
            self.add_bedroom_per_room = add_bedroom_per_room  
            self.total_room_ix = total_room_ix 
            self.population_ix =population_ix 
            self.households_ix =households_ix 
            self.total_bedroom_ix = total_bedroom_ix

        except Exception as e:
            raise HousingException(e,sys) from e
        
    def fit(self ,X,y=None):
        return self  
    


    def transform(self ,X ,y=None):
        try:
            room_per_households = X[: ,self.total_room_ix] / X[: ,self.households_ix]

            population_per_households = X[: ,self.population_ix] / X[: ,self.households_ix]

            bedroom_per_room = X[: ,self.total_bedroom_ix]/X[: ,self.total_room_ix]

            if self.add_bedroom_per_room:
                generated_feature = np.c_[
                    X ,room_per_households , population_per_households,bedroom_per_room
                ]
            else:
                generated_feature = np.c_[X,room_per_households ,population_per_households]
            
            return generated_feature
        
        except Exception as e:
            raise HousingException(e,sys) from e 
        




class DataTransformation():
    def __init__(self ,
                 data_transformation_config : DataTransfrmationConfig,
                 data_ingestion_artifact :DataIngestionArtifact ,
                 data_validation_artifact : DataValidationArtifacts):
        try:

            logging.info(f'\n\n{"*" * 20} Data Transformation Step Started {"*" *20}') 
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact 
            self.data_validation_artifact = data_validation_artifact

        except Exception as e:
            raise HousingException(e ,sys) from e
        

    @staticmethod  
    def check_data_type(file_path ,schema_file_path):
        try:
            train_data = pd.read_csv(file_path)
            schema_data = read_yaml(schema_file_path)
            schema = schema_data[SCHEMA_FILE_COLUMN_KEY]


            for column in train_data.columns:
                if column in list(schema.keys()):
                    train_data[column].astype(schema[column])
                
                else:
                    raise Exception(e ,sys) 
            return train_data


        except Exception as e:
            raise HousingException(e ,sys) from e 
        

    def get_data_transformer_object(self) ->ColumnTransformer:
        try:
            
            logging.info("We are Creating Data Transformation Object")
            schema_file_path = self.data_validation_artifact.schema_file_path 
            dataset_schema = read_yaml(schema_file_path)

            
            numerical_column = dataset_schema[SCHEMA_NUMERICAL_COLUMN_KEY].split(" ")
            categorical_column =dataset_schema[SCHEMA_CATEGORICAL_COLUMN_KEY].split(" ")
            

            num_pipeline = Pipeline(
               steps=[
                ('impute' ,SimpleImputer(strategy='median')) ,
                ('feature_generator' ,FeatureGenerator(
                    # add_bedroom_per_romm= self.data_transformation_config.add_bedroom_per_room,
                    # columns=numerical_column
                )) ,
                ('scalar' ,StandardScaler())
                ]
                   )
            cat_pipeline = Pipeline(
               steps=[
                ('impute' ,SimpleImputer(strategy='most_frequent')) ,
                ('encode' ,OneHotEncoder()) ,
                ('scalar' ,StandardScaler(with_mean=False))
                ]
                   )
            logging.info('Applying Transformer on Data')
            
            
            preprocessor = ColumnTransformer([
                ('num_pipeline' , num_pipeline ,numerical_column) ,
                ('cat_pipeline' ,cat_pipeline ,categorical_column)
                ])
            return preprocessor 


        except Exception as e:
            raise HousingException(e ,sys) from e 

    def initiated_data_transformation(self)->DataTransformationArtifact:
        try:
            
            logging.info(f'{"*"*20}Data Transformation started {"*"*20}')
            preprocessing_obj = self.get_data_transformer_object()

            logging.info(f'Loading Data from {self.data_ingestion_artifact} and {self.data_ingestion_artifact.test_file_path}')
            
            # train_data ,test_data = self.get_dataset() 
            train_file_path = self.data_ingestion_artifact.train_file_path 
            test_file_path = self.data_ingestion_artifact.test_file_path 

            train_data = pd.read_csv(train_file_path)
            test_data = pd.read_csv(test_file_path)


            logging.info(f"Load Schema of Data from [{self.data_validation_artifact.schema_file_path}]")

            schema_file_path =self.data_validation_artifact.schema_file_path
            schema = read_yaml(schema_file_path)
            

            target_column_name = schema[TARGET_COLUMN_KEY]
            

            logging.info("Separating Output column from Train and test data")
            input_train_df = train_data.drop(columns=[target_column_name])
            output_train_df = train_data[[target_column_name]]

            input_test_df = test_data.drop(columns=[target_column_name])
            output_test_df = test_data[[target_column_name]]

            logging.info("Applying Preprocessor on Train and Test Data")
            
            input_train_arr = preprocessing_obj.fit_transform(input_train_df)
            input_test_arr = preprocessing_obj.transform(input_test_df)
            
            final_train_arr = np.c_[
                input_train_arr ,np.array(output_train_df)
            ]
            final_test_arr = np.c_[
                input_test_arr ,np.array(output_test_df)
            ]

            train_file_name = os.path.basename(self.data_ingestion_artifact.train_file_path).replace('csv' ,'npz')
            test_file_name = os.path.basename(self.data_ingestion_artifact.test_file_path).replace('csv' ,'npz')
            

            transformed_train_dir = self.data_transformation_config.transformed_train_dir
            transformed_test_dir = self.data_transformation_config.transformed_test_dir 
            
            transformed_train_file_path = os.path.join(
                transformed_train_dir , train_file_name 
            )

            transformed_test_file_path = os.path.join(
                transformed_test_dir ,test_file_name 
            )
            

            
            logging.info(f"Transformed Train Data will save at : [{transformed_train_file_path}]")
            logging.info(f"Transformed Test Data will save at : [{transformed_test_file_path}]")

            preprocessor_obje_file_path = os.path.join(
                self.data_transformation_config.transformed_dir ,
                self.data_transformation_config.preprocessed_object_dir ,
                self.data_transformation_config.preprocessing_object_file_name
            )
            

            save_object(
                file_path=preprocessor_obje_file_path ,
                obj=preprocessing_obj
            )
            
            save_numpy_array(
                file_path = transformed_train_file_path ,
                array = final_train_arr 
            )
            save_numpy_array(
                file_path = transformed_test_file_path ,
                array = final_test_arr
            )
            
            
            data_transformtion_artifacts = DataTransformationArtifact(
                is_transformed=True ,
                message= "Data Transformation Is Succefull",
                transformed_train_file_path= transformed_train_file_path ,
                transformed_test_file_path= transformed_test_file_path ,
                preprocessing_obj_file_path = preprocessor_obje_file_path

            )
            logging.info(data_transformtion_artifacts)
            # print("Data Transformation Completed")
            logging.info(f'{"*"*20}Data Transformation Completed {"*"*20}')

            return data_transformtion_artifacts

        except Exception as e:
            raise HousingException (e ,sys) from e