import os ,sys 
from Housing.src.entity.config_entity import ModelEvaluationConfig  
from Housing.src.entity.artifact_entity import  DataIngestionArtifact ,DataValidationArtifacts ,DataTransformationArtifact ,ModelTrainingArtifacts ,ModelEvaluationArtifact
from Housing.src.logger import logging 
from Housing.src.exception import HousingException 
import numpy as np 
from Housing.src.utils.utils import read_yaml ,save_numpy_array  ,save_object ,write_yaml ,load_object ,load_array ,load_data
from Housing.src.constant import *
from Housing.src.entity.model_factory import evaluate_regression_model


class ModelEvaluation:
    def __init__(self, 
                config:ModelEvaluationConfig ,
                data_ingestion_artifacts : DataIngestionArtifact ,
                data_validation_artifacts : DataValidationArtifacts,
                model_training_artifacts : ModelTrainingArtifacts ,
                data_transformation_artifacts : DataTransformationArtifact):
        try:

            logging.info(f'\n\n{"*" * 20} Model Evaluation Step Started {"*" *20}') 
            self.model_evaluation_config = config
            self.data_ingestion_artifacts = data_ingestion_artifacts
            self.data_validation_artifacts = data_validation_artifacts
            self.model_training_artifacts = model_training_artifacts 


            self.data_transformation_artifacts = data_transformation_artifacts
    

        except Exception as e:
            raise HousingException(e ,sys) from e
        
    def get_best_model(self):
        try:
            logging.info(f"Getting Best Model From Past")
            model = None 
            model_evaluation_file_path = self.model_evaluation_config.model_evaluation_file_path


            if not os.path.exists(model_evaluation_file_path):
                print('Model Evaluation File Path Is Empty So We Wil Create Empty File')
                logging.info(f"{model_evaluation_file_path} is not exist so we will create empty file at same location")
                write_yaml(
                    file_path= model_evaluation_file_path ,
                    data =None
                )
                return model #(model =None) 
            

            #If model_evaluation_file_path is present(suppose 2nd time you runnning)
            model_eval_file_content = read_yaml(yaml_file_path=model_evaluation_file_path)

            #dict() will create empty dictionary
            if model_eval_file_content is None:
                logging.info(f"{model_evaluation_file_path} file is empty we will create empty dictionary inside that file")
                model_eval_file_content = dict()
                
            else:
                model_eval_file_content = model_eval_file_content
            
            if BEST_MODEL_KEY not in model_eval_file_content.keys():
                return model 
        
            
            model = load_object(file_path=model_eval_file_content[BEST_MODEL_KEY][MODEL_PATH_KEY])
            return model 

        except Exception as e:
            raise HousingException(e ,sys) from e
        
    def update_evaluation_report(self ,model_evaluation_artifacts:ModelEvaluationArtifact):
        try:
            print('update_evaluation_report Function')
            evaal_file_path = self.model_evaluation_config.model_evaluation_file_path 
            model_eval_file_content = read_yaml(yaml_file_path=evaal_file_path)

            model_eval_file_content = dict() if model_eval_file_content is None else model_eval_file_content
                
            previous_best_model_path = None 
            if BEST_MODEL_KEY in model_eval_file_content:
                previous_best_model_path = model_eval_file_content[BEST_MODEL_KEY] 
                print(f'Previous Model Path:-{previous_best_model_path}')
                logging.info(f"Previous Best Model Evaluation Content : [{model_eval_file_content}]")


            #eval_result will store current trained data details
            eval_result = {
                BEST_MODEL_KEY : {
                    MODEL_PATH_KEY : model_evaluation_artifacts.evaluated_model_path
                }
            }

            if previous_best_model_path is not None:
                print(f"model_evaluation_config:-{self.model_evaluation_config}")
                model_history = {self.model_evaluation_config.CURRENT_TIME_STAMP: previous_best_model_path}
                if HISTORY_KEY not in model_eval_file_content:
                    history = {HISTORY_KEY: model_history}
                    eval_result.update(history)
                else:
                    model_eval_file_content[HISTORY_KEY].update(model_history)

            model_eval_file_content.update(eval_result)
            print(eval_result)
            print(model_eval_file_content)

            logging.info(f"Updated eval result:{model_eval_file_content}")
            write_yaml(file_path=evaal_file_path, data=model_eval_file_content)


        except Exception as e:
            raise HousingException(e ,sys) from e


        
    def initiate_model_evaluation(self):
        try:
            trained_model_path =self.model_training_artifacts.trained_model_file_path
            trained_model_object = load_object(trained_model_path)
            print(trained_model_path)

            train_file_path = self.data_ingestion_artifacts.train_file_path 
            test_file_path =self.data_ingestion_artifacts.test_file_path 

            schema_file_path = self.data_validation_artifacts.schema_file_path
            
            train_dataframe = load_data(file_path=train_file_path ,schema_file_path=schema_file_path)
            test_dataframe = load_data(file_path=test_file_path ,schema_file_path=schema_file_path)

            schema_content = read_yaml(yaml_file_path=schema_file_path)

            target_column_name = schema_content[TARGET_COLUMN_KEY]


            # target_column
            logging.info(f"Converting target column into numpy array.")
            train_target_arr = np.array(train_dataframe[target_column_name])
            test_target_arr = np.array(test_dataframe[target_column_name])
            logging.info(f"Conversion completed target column into numpy array.")

            

            #Dropping Target Column From Dataframe
            logging.info(f"Dropping target column from the dataframe.")
            train_dataframe = train_dataframe.drop(columns=[target_column_name] )
            test_dataframe = test_dataframe.drop(columns=[target_column_name] )
            logging.info(f"Dropping target column from the dataframe completed.")
            logging.info('Applying Preprocessor on data')
            logging.info(f"Preprocessor_location :[{self.data_transformation_artifacts.preprocessing_obj_file_path}]")
            preprocessor = load_object(file_path=self.data_transformation_artifacts.preprocessing_obj_file_path)
            train_dataframe = preprocessor.fit_transform(train_dataframe)
            test_dataframe = preprocessor.fit_transform(test_dataframe)
            previous_best_model =self.get_best_model()

            


            if previous_best_model is None:
                logging.info(f"We dont have best model in past.Hence accepting current modele as best model")
                model_evaluation_artifacts = ModelEvaluationArtifact(
                    is_model_accepted=True ,
                    evaluated_model_path=trained_model_path
                )
                self.update_evaluation_report(model_evaluation_artifacts=model_evaluation_artifacts)
                logging.info(f"Model accepted. Model eval artifact {model_evaluation_artifacts} created")
                return model_evaluation_artifacts 
            model_list = [previous_best_model, trained_model_object]
            print(model_list)
            print(type(previous_best_model).__name__)
            print(type(trained_model_object).__name__)

           
            
            metric_info_artifact = evaluate_regression_model(model_list=model_list,
                                                               X_train=train_dataframe,
                                                               y_train=train_target_arr,
                                                               X_test=test_dataframe,
                                                               y_test=test_target_arr,
                                                               base_accuracy=self.model_training_artifacts.model_accuracy
                                                       )

            logging.info(f"Model evaluation completed. model metric artifact: {metric_info_artifact}")

            if metric_info_artifact is None:
                response = ModelEvaluationArtifact(is_model_accepted=False,
                                                   evaluated_model_path=trained_model_path
                                                   )
                logging.info(response)
                return response

            if metric_info_artifact.index_number == 1:
                model_evaluation_artifact = ModelEvaluationArtifact(evaluated_model_path=trained_model_path,
                                                                    is_model_accepted=True)
                self.update_evaluation_report(model_evaluation_artifact)
                logging.info(f"Model accepted. Model eval artifact {model_evaluation_artifact} created")

            else:
                logging.info("Trained model is no better than existing model hence not accepting trained model")
                model_evaluation_artifact = ModelEvaluationArtifact(evaluated_model_path=trained_model_path,
                                                                    is_model_accepted=False)
            return model_evaluation_artifact
        except Exception as e:
            raise HousingException(e, sys) from e



