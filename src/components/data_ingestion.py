import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts','train.csv')
    test_data_path: str = os.path.join('artifacts','test.csv')
    raw_data_path: str = os.path.join('artifacts','raw.csv')
    
class DataIngestion:
    def __init__(self) -> None:
        self.ingestion_cofig = DataIngestionConfig
    
    def initiate_data_ingestion(self):
        logging.info("Entered the data Ingestion Method or component")
        try:
            df = pd.read_csv('notebook/data/stud.csv')
            logging.info('Read the dataset as dataframe')
            os.makedirs(os.path.dirname(self.ingestion_cofig.train_data_path), exist_ok=True)
            
            df.to_csv(self.ingestion_cofig.raw_data_path,index=False,header=True)
            logging.info("Train test Split Initiated")
            train_set, test_set = train_test_split(df,test_size=0.2, random_state=1)
            
            train_set.to_csv(self.ingestion_cofig.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_cofig.test_data_path,index=False,header=True)
            logging.info('Ingestion of the data is completed')
            
            return (
                self.ingestion_cofig.train_data_path,
                self.ingestion_cofig.test_data_path
            )
        except Exception as e:
            raise CustomException(e,sys)
        
from src.components.data_transformation import DataTransformation
if __name__ == "__main__":
    obj = DataIngestion()
    
    train_data, test_data = obj.initiate_data_ingestion()
    
    trans_obj = DataTransformation()
    
    train_arr, test_arr,_ = trans_obj.initiate_data_transformation(train_data,test_data)
    
    model_trainer = ModelTrainer()
    
    print(model_trainer.initiate_model_trainer(train_arr, test_arr))