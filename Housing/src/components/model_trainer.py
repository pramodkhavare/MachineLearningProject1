from Housing.src.config.configuration import HousingConfiguration 
import os ,sys 
from Housing.src.entity.config_entity import ModelTrainingConfig ,DataTransfrmationConfig 
from Housing.src.entity.artifact_entity import  DataIngestionArtifact ,DataValidationArtifacts ,DataTransformationArtifact ,ModelTrainingArtifacts
from Housing.src.logger import logging 
from Housing.src.exception import HousingException 
from Housing.src.entity.model_factory import ModelFactory ,GridSearchedBestModel ,MetricInfoArtifact
import pandas as pd 
import numpy as np 
from Housing.src.utils.utils import read_yaml ,save_numpy_array  ,save_object ,load_array ,load_object
from Housing.src.constant import *
import pickle
from typing import List
from Housing.src.entity.model_factory import evaluate_regression_model

class Final_Housing_model():
    def __init__(self ,model_obj ,preprocessor_obj):

        self.model_obj = model_obj
        self.preprocessor_obj = preprocessor_obj 


    def predict(self ,X):
        try:
            transformed_feature = self.preprocessor_obj.transform(X)
            prediction = self.model_obj.predict(transformed_feature)
            return prediction 

        except Exception as e:
            logging.info("Unable To Predict Output")
            raise HousingException(e,sys)
        


class ModelTrainer():
    def __init__(self,
                model_training_config :ModelTrainingConfig ,
                data_transformation_artifacts :DataTransformationArtifact ,
                ):
        try:
            logging.info(f'\n\n{"*" *20} Model Training Started{"*" *20}')
            self.model_training_config =model_training_config
            self.data_transformation_artifacts =data_transformation_artifacts 
        except  Exception as e:
            raise HousingException(e,sys) from e
        
    
        
    def initiate_model_training(self ):
        try:
            logging.info("Loading Transformed Data Into Varible") 

            transformed_train_file_path = self.data_transformation_artifacts.transformed_train_file_path
            transformed_test_file_path = self.data_transformation_artifacts.transformed_test_file_path 

            train_array = load_array(transformed_train_file_path)
            test_array = load_array(transformed_test_file_path)

            logging.info("Splitting Array Into input and target column")

            x_train ,y_train ,x_test ,y_test = train_array[: ,:-1] ,train_array[: ,-1] ,test_array[: ,:-1] ,test_array[: ,-1]

            logging.info('Data Split process completed')
            logging.info(f"Shape of train and test data is x_train: [{x_train.shape}] ,x_test : [{x_test.shape}] ,y_train: [{y_train.shape}] ,y_test:[{y_test.shape}]")

            logging.info("Extracting Model Information From Config File")
            
            model_config_file_path= self.model_training_config.model_config_file_path

            base_accuracy = self.model_training_config.base_accuracy

            model_factory = ModelFactory(model_config_path=model_config_file_path)
            #You will Get best model from following ccode
            best_model =model_factory.get_best_model(X=x_train ,y=y_train ,base_accuracy=base_accuracy) 

            logging.info(f"Best Model We Found On Training Data Is :[{best_model}]")

            logging.info(f"Extracting trained model list.")
            grid_searched_best_model_list:List[GridSearchedBestModel]=model_factory.grid_searched_best_model_list

            
            model_list = [model.best_model for model in grid_searched_best_model_list]
            
            logging.info(f"Model List : [{model_list}]")

            """MetricInfoArtifact = namedtuple("MetricInfo",
                                ["model_name", "model_object", "train_rmse", "test_rmse", "train_accuracy",
                                 "test_accuracy", "model_accuracy", "index_number"])"""
            metric_info:MetricInfoArtifact = evaluate_regression_model(
                model_list=model_list ,
                X_train= x_train ,y_train= y_train ,X_test=x_test ,y_test=y_test,
                base_accuracy=base_accuracy 
            )
            
            print('Metric Info')
            print(metric_info)
            
            

            logging.info(f"Best model found and saved into MetricInfoArtifact") 
            preprocessor_obj = load_object(file_path=self.data_transformation_artifacts.preprocessing_obj_file_path)
            model_obj = metric_info.model_object 
            final_housing_model = Final_Housing_model(
                model_obj=model_obj ,
                preprocessor_obj= preprocessor_obj
            )

            trained_model_file_path =self.model_training_config.trained_model_file_path 

            save_object(file_path=trained_model_file_path ,obj=model_obj)
            logging.info(f'Model is saved at [{trained_model_file_path}]')
            logging.info(f'preprocessor Object is saved at [{self.data_transformation_artifacts.preprocessing_obj_file_path}]')


            #Getting Details 
            train_rmse = metric_info.train_rmse 
            train_accuracy = metric_info.train_accuracy 
            test_rmse = metric_info.test_rmse 
            test_accuracy = metric_info.test_accuracy 
            model_accuracy = metric_info.model_accuracy



            model_training_artifacts:ModelTrainingArtifacts =ModelTrainingArtifacts(
                trained_model_file_path= trained_model_file_path,
                train_rmse= train_rmse,
                train_accuracy= train_accuracy,
                test_rmse= test_rmse,
                test_accuracy= test_accuracy,
                model_accuracy= model_accuracy
            )

            logging.info(f"Model Training Artifacts :[{model_training_artifacts}]")

            return model_training_artifacts



        except  Exception as e:
            raise HousingException(e,sys) from e
        
    def __del__(self):
        logging.info(f"{'>>' * 30}Model trainer log completed.{'<<' * 30} ")


        