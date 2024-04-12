from Housing.src.config.configuration import HousingConfiguration
from Housing.src.entity.config_entity import DataIngestionConfig
from Housing.src.entity.artifact_entity import DataIngestionArtifact
from Housing.src.logger import logging
from Housing.src.exception import HousingException
import os ,sys 
import tarfile 
from six.moves import urllib
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit 
import shutil

class DataIngestion():
    def __init__(self ,data_ingestion_config :DataIngestionConfig):
        try:
            logging.info(f"{'*'*20}Data Ingestion Step Started{'*'*20}")
            self.config = data_ingestion_config  
            # print(self.config)
        except Exception as e:
            raise HousingException(e ,sys) from e
        


    def download_tgz_file(self):
        try:          
            if os.path.exists(self.config.tgz_download_dir):
               (
                  shutil.rmtree(self.config.tgz_download_dir) 
               ) 
            os.makedirs(self.config.tgz_download_dir ,exist_ok=True)

            housing_file_name = os.path.basename(self.config.dataset_download_url)
            tgz_file_path = os.path.join(self.config.tgz_download_dir ,housing_file_name)

            logging.info(f"Downloading Data at file: [{tgz_file_path}]  from url: [{self.config.dataset_download_url}]")
            filename ,url = urllib.request.urlretrieve(
                url= self.config.dataset_download_url ,
                filename= tgz_file_path
            )
            logging.info(f"File : [{tgz_file_path}] has been downloaded successfully")

            return tgz_file_path

        except Exception as e:
            # logging.info(f'Unable to Donload file: [{tgz_file_path}]')
            raise HousingException(e,sys) from e




    def extract_tgz_file(self ,tgz_file_path :str):
        try:
            if os.path.exists(self.config.raw_data_dir):
                shutil.rmtree(self.config.raw_data_dir)

            os.makedirs(self.config.raw_data_dir ,exist_ok=True)

            logging.info(f"Extracting data into [{self.config.raw_data_dir}]")

            with tarfile.open(tgz_file_path) as housing_tgz_file_obj:
                housing_tgz_file_obj.extractall(path=self.config.raw_data_dir)

            logging.info(f"Extraction is completed") 

        except Exception as e:
            logging.info("Unable to unzip data")
            raise HousingException(e ,sys) from e


    def split_data_train_test(self):
        try:
            raw_data_dir = self.config.raw_data_dir 

            file_name = os.listdir(raw_data_dir)[0]
            train_file_name = "train_data_" + file_name 
            test_file_name = "test_data_" + file_name 

            housing_file_path = os.path.join(raw_data_dir , file_name)

            logging.info(f"Reading Csv file : {housing_file_path}")

            housing_data_frame = pd.read_csv(housing_file_path)

            housing_data_frame['income_cat'] = pd.cut(
                housing_data_frame['median_income'] ,
                bins =[0.0 ,1.5 ,3 ,4.5 ,6 ,np.inf] ,
                labels= [1,2,3,4,5]
            )

            logging.info("Splitting data into train and test data")

            split = StratifiedShuffleSplit(n_splits=1 ,test_size= 0.2 ,random_state=42)



            start_train_set =None 
            start_test_set = None

            for train_index ,test_index in split.split(housing_data_frame ,housing_data_frame['income_cat']):
                start_train_set = housing_data_frame.loc[train_index].drop(['income_cat'] ,axis=1)
                start_test_set = housing_data_frame.loc[test_index].drop(['income_cat'] ,axis=1)

            train_file_path =os.path.join(self.config.ingested_train_dir , train_file_name)
            test_file_path = os.path.join(self.config.ingested_test_dir ,test_file_name)

            if start_train_set is not None:
                os.makedirs(self.config.ingested_train_dir ,exist_ok= True)
                logging.info(f"Saving training data to file :{train_file_path}")
                start_train_set.to_csv(train_file_path,index = False)


            if start_test_set is not None:
                os.makedirs(self.config.ingested_test_dir ,exist_ok= True)
                # print(start_test_set)
                logging.info(f"Saving test data to file :{test_file_path}")
                start_test_set.to_csv(test_file_path ,index = False)


            data_ingestion_artifacts = DataIngestionArtifact(
                train_file_path= train_file_path,
                test_file_path=test_file_path ,
                is_ingested= True,
                message= f"Data Ingestion is completed successfully"
            )

            return data_ingestion_artifacts


        except Exception as e:
            logging.info("Unable to split data")
            raise HousingException(e ,sys) from e


    
    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            tgz_file_path = self.download_tgz_file()
            self.extract_tgz_file(tgz_file_path=tgz_file_path)
            data_ingestion_artifacts = self.split_data_train_test()
            logging.info(f"{'*'*20}Data Ingestion Step Completed{'*'*20}")
            # print("Data Ingestion Completed")
            return data_ingestion_artifacts
        
        except Exception as e:
            raise HousingException(e ,sys) from e
        
    def _del_(self):
        logging.info(f"{'*'*20} Data Ingesteion Pipeline Completed {'*'*20}")
