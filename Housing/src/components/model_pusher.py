import os ,sys 
from Housing.src.entity.config_entity import ModelPusherConfig
from Housing.src.entity.artifact_entity import ModelTrainingArtifacts ,ModelEvaluationArtifact ,ModelPusherArtifacts
from Housing.src.logger import logging 
from Housing.src.exception import HousingException 
import numpy as np 
from Housing.src.utils.utils import read_yaml ,save_numpy_array  ,save_object ,write_yaml ,load_object ,load_array ,load_data
from Housing.src.constant import *
from Housing.src.constant import *
from Housing.src.entity.model_factory import evaluate_regression_model
import shutil

class ModelPusher:
    def __init__(self ,
                 model_pusher_config :ModelPusherConfig ,
                 model_evaluation_artifacts :ModelEvaluationArtifact):
        try:
            logging.info(f'\n\n{">" * 10} Model Pusher Step Started {"<" *10}') 
            self.model_pusher_config = model_pusher_config 
            self.model_evaluation_artifacts = model_evaluation_artifacts 

        except Exception as e:
            raise HousingException(e ,sys) from e
    

    def export_model(self)->ModelPusherArtifacts:
        try:
            evaluated_model_file_path = self.model_evaluation_artifacts.evaluated_model_path 
            export_dir = self.model_pusher_config.export_dir_path 

            export_model_file_path = self.model_pusher_config.export_dir_path 

            logging.info(f"Exporting model file from: [{evaluated_model_file_path}]")
            logging.info(f"Exporting model file at: [{export_model_file_path}]")

            os.makedirs(export_dir ,exist_ok=True)

            shutil.copy(src=evaluated_model_file_path, dst=export_model_file_path)

            logging.info(f"Exporting model file from: [{evaluated_model_file_path}]")

            model_pusher_artifacts = ModelPusherArtifacts(
                is_model_pushed= True ,
                export_model_file_path=export_model_file_path
            )
            logging.info(f"Model pusher artifact: [{model_pusher_artifacts}]")

            return model_pusher_artifacts


        except Exception as e:
            raise HousingException(e ,sys) from e
        
    
    def initiate_model_pushing(self):
        try:
            logging.info('initiate model pusher has been started') 

            export_model = self.export_model()
            logging.info('initiate model pusher has been completed') 
            return export_model

        except Exception as e:
            raise HousingException(e ,sys) from e
        
    def __del__(self):
        logging.info(f"{'>>' * 20}Model Pusher log completed.{'<<' * 20} ")
        