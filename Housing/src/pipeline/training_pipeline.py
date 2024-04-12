from Housing.src.config.configuration import HousingConfiguration
from Housing.src.components.data_ingestion import DataIngestion
from Housing.src.components.data_validation import DataValidation
from Housing.src.components.data_transformation import DataTransformation
from Housing.src.components.model_evaluation import ModelEvaluation
from Housing.src.components.model_trainer import ModelTrainer 
from Housing.src.components.model_pusher import ModelPusher
from Housing.src.exception import HousingException
from Housing.src.entity.artifact_entity import DataIngestionArtifact ,DataValidationArtifacts ,DataTransformationArtifact ,ModelTrainingArtifacts , ModelPusherArtifacts ,ModelEvaluationArtifact
from Housing.src.logger import logging
import os ,sys
import pandas as pd
import uuid
from threading import Thread
from collections import namedtuple
from datetime import datetime
from Housing.src.constant import EXPERIMENT_DIR_NAME ,EXPERIMENT_FILE_NAME
Experiment = namedtuple("Experiment", ["experiment_id", "initialization_timestamp", "artifact_time_stamp",
                                       "running_status", "start_time", "stop_time", "execution_time", "message",
                                       "experiment_file_path", "accuracy", "is_model_accepted"])

class Pipeline(Thread):
    experiment:Experiment = Experiment(*([None]*11))
    experiment_file_path = None
    def __init__(self ,config:HousingConfiguration=HousingConfiguration()):
        try:
            os.makedirs(config.get_training_pipeline_config().artifact_dir ,exist_ok=True)
            Pipeline.experiment_file_path = os.path.join(config.get_training_pipeline_config().artifact_dir ,EXPERIMENT_DIR_NAME,EXPERIMENT_FILE_NAME)
            super().__init__(daemon=False ,name='pipeline')
            self.config = config 

        except Exception as e:
            raise HousingException(e ,sys) from e 

    def start_data_ingestion(self) ->DataIngestionArtifact:
        try:
            data_ingestion_config = self.config.get_data_ingestion_config()
        
            data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
            data_ingestion_output = data_ingestion.initiate_data_ingestion()

            print('Data Ingestion Completed\n')

            return data_ingestion_output
            
             
        except Exception as e:
            raise HousingException(e ,sys) from e
        

    def start_data_validation(self,data_ingestion_artifacts: DataIngestionArtifact)->DataValidationArtifacts:
        try:
            data_validation_config = self.config.get_data_validation_config()
            data_ingestion_artifact =data_ingestion_artifacts
            data_validation =DataValidation(data_validation_config=data_validation_config ,
                                            data_ingestion_artifact= data_ingestion_artifact)

            data_validation_output = data_validation.initiate_data_validation() 
            print('Data Validation Completed\n')
            return data_validation_output
        except Exception as e:
            raise HousingException(e ,sys) from e
          

    def start_data_transformation(self ,data_ingestion_artifacts:DataIngestionArtifact ,data_validation_artifact:DataValidationArtifacts) ->DataTransformationArtifact:
        try:
            data_transformation_config = self.config.get_data_transformation_config()
            data_ingestion_artifact = data_ingestion_artifacts
            data_validation_artifact= data_validation_artifact
            data_transformation_artifacts = DataTransformation(
                data_transformation_config=data_transformation_config ,
                data_ingestion_artifact= data_ingestion_artifact ,
                data_validation_artifact= data_validation_artifact
            )
            data_transformation_artifacts = data_transformation_artifacts.initiated_data_transformation()

            print('Data Transformation Completed\n')
            return data_transformation_artifacts
        except Exception as e:
            raise HousingException(e ,sys) from e  

      

    def start_model_training(self ,data_transformation_artifacts:DataTransformationArtifact):
        try:
            model_training_config = self.config.get_model_trainer_config()
            model_trainer = ModelTrainer(
                model_training_config=model_training_config ,
                data_transformation_artifacts= data_transformation_artifacts
            )

            print("Model Training Completed\n")
            return model_trainer.initiate_model_training()
        except Exception as e:
            raise HousingException(e ,sys) from e  


    def start_model_evaluation(self ,data_ingestion_artifacts:DataIngestionArtifact ,
                               data_validation_artifacts:DataValidationArtifacts ,model_training_artifacts:ModelTrainingArtifacts ,
                               data_transformation_artifacts:DataTransformationArtifact)->ModelEvaluationArtifact:
        try:
            model_evaluation_config = self.config.get_model_evaluation_config()
            
            model_evaluation = ModelEvaluation(
                config=model_evaluation_config ,
                data_ingestion_artifacts = data_ingestion_artifacts,
                data_validation_artifacts = data_validation_artifacts,
                model_training_artifacts = model_training_artifacts ,
                data_transformation_artifacts= data_transformation_artifacts
            )

            model_evaluation_artifacts =model_evaluation.initiate_model_evaluation()
            print("Model Evaluation Completed")

            return model_evaluation_artifacts
        except Exception as e:
            raise HousingException(e ,sys) from e  
        
    def start_model_pusher(self ,model_evaluation_artifacts:ModelEvaluationArtifact)->ModelPusherArtifacts:
        try:
            model_pusher_config = self.config.get_model_pusher_config()
            model_pusher = ModelPusher(
                model_pusher_config= model_pusher_config ,
                model_evaluation_artifacts=model_evaluation_artifacts
            )
            model_pusher_artifacts = model_pusher.initiate_model_pushing()
            print('Model Pusher Step Completed') 
            return model_pusher_artifacts
        except Exception as e:
            raise HousingException(e ,sys) from e
        

    def run_pipeline(self):
        try:
            if Pipeline.experiment.running_status :
                logging.info("Pipeline Is Already Running")
                return Pipeline.experiment 
            
            logging.info('Pipeline Starting')
            experiment_id = str(uuid.uuid4())

            Pipeline.experiment = Experiment(
                experiment_id= experiment_id ,initialization_timestamp=self.config.time_stamp ,
                artifact_time_stamp=self.config.time_stamp ,running_status= True ,
                start_time= datetime.now() ,stop_time=None ,execution_time=None ,
                message='Pipeline Has BEen Started' ,experiment_file_path=Pipeline.experiment_file_path ,
                is_model_accepted=None , accuracy=None
            )
            logging.info(f"Pipeline Experiment : {Pipeline.experiment}")
            self.save_experiment()

            data_ingestion_artifacts = self.start_data_ingestion()
            data_validation_artifacts = self.start_data_validation(data_ingestion_artifacts=data_ingestion_artifacts)
            data_transformation_artifacts = self.start_data_transformation(
                data_ingestion_artifacts=data_ingestion_artifacts ,
                data_validation_artifact= data_validation_artifacts
            )
            model_training_artifacts = self.start_model_training(
                data_transformation_artifacts= data_transformation_artifacts
            )
            model_evaluation_artifacts = self.start_model_evaluation(
                data_ingestion_artifacts=data_ingestion_artifacts ,data_validation_artifacts=data_validation_artifacts ,
                model_training_artifacts=model_training_artifacts ,data_transformation_artifacts=data_transformation_artifacts
            )
            if model_evaluation_artifacts.is_model_accepted:
                model_pusher_artifacts = self.start_model_pusher(
                    model_evaluation_artifacts=model_evaluation_artifacts
                )
                logging.info(f"Model Pusher Artifacts : {model_pusher_artifacts}")

            else:
                logging.info('Trained Model Rejected')
            logging.info('Pipeline completed')

            stop_time = datetime.now()

            Pipeline.experiment = Experiment(
                experiment_id= experiment_id ,initialization_timestamp=self.config.time_stamp ,
                artifact_time_stamp=self.config.time_stamp ,running_status= False ,
                start_time= Pipeline.experiment.start_time ,stop_time=stop_time ,execution_time=stop_time - Pipeline.experiment.start_time,
                message='Pipeline Has Been Completed' ,experiment_file_path=Pipeline.experiment_file_path ,
                is_model_accepted=model_evaluation_artifacts.is_model_accepted , accuracy=model_training_artifacts.model_accuracy
            )
            logging.info(f"Pipeline experiment: {Pipeline.experiment}")
            self.save_experiment()
        except Exception as e:
            raise HousingException(e ,sys) from e 
        




    def run(self):
        try:
            print(123)
            self.run_pipeline()

        except Exception as e:
            raise HousingException(e ,sys) from e
    def save_experiment(self):
        try:
            if Pipeline.experiment.experiment_id is not None:
                experiment = Pipeline.experiment
                experiment_dict = experiment._asdict()
                experiment_dict: dict = {key: [value] for key, value in experiment_dict.items()}

                experiment_dict.update({
                    "created_time_stamp": [datetime.now()],
                    "experiment_file_path": [os.path.basename(Pipeline.experiment.experiment_file_path)]})

                experiment_report = pd.DataFrame(experiment_dict)

                os.makedirs(os.path.dirname(Pipeline.experiment_file_path), exist_ok=True)
                if os.path.exists(Pipeline.experiment_file_path):
                    experiment_report.to_csv(Pipeline.experiment_file_path, index=False, header=False, mode="a")
                else:
                    experiment_report.to_csv(Pipeline.experiment_file_path, mode="w", index=False, header=True)
            else:
                print("First start experiment")
        except Exception as e:
            raise HousingException(e, sys) from e

    @classmethod
    def get_experiments_status(cls, limit: int = 5) -> pd.DataFrame:
        try:
            if os.path.exists(Pipeline.experiment_file_path):
                df = pd.read_csv(Pipeline.experiment_file_path)
                limit = -1 * int(limit)
                return df[limit:].drop(columns=["experiment_file_path", "initialization_timestamp"], axis=1)
            else:
                return pd.DataFrame()
        except Exception as e:
            raise HousingException(e, sys) from e