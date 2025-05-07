import os
import sys
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml_file

logger = get_logger(__name__)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GCP_CREDENTIALS_PATH

class DataIngestion:
    def __init__(self,config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.bucket_file_name = self.config["bucket_file_name"]
        self.train_test_ratio = self.config["train_ratio"]
        
        os.makedirs(RAW_DIR, exist_ok=True)
        
        logger.info(f"Data Ingestion started with {self.bucket_name} and file name is {self.bucket_file_name}")

    def download_csv_from_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.bucket_file_name)
            blob.download_to_filename(RAW_FILE_PATH)
            logger.info(f"CSV file is sucessfully downloaded from GCP: {self.bucket_file_name} to {RAW_FILE_PATH}")
        except Exception as e:
            logger.error(f"Error downloading file from GCP: {e}")
            raise CustomException(f"Failed to download CSV file from GCP", e) 

    def split_data(self):
        try:
            logger.info("Starting data splitting process.")
            df = pd.read_csv(RAW_FILE_PATH)
            train_data, test_data = train_test_split(df, test_size=1-self.train_test_ratio, random_state=42)
            train_data.to_csv(TRAIN_FILE_PATH)
            test_data.to_csv(TEST_FILE_PATH)
            logger.info(f"Data split completed. Train data saved to {TRAIN_FILE_PATH} and test data saved to {TEST_FILE_PATH}")
        except Exception as e:
            logger.error(f"Error during data splitting: {e}")
            raise CustomException(f"Failed to split data into training and testing sets", e) 
    
    def run(self):
        try:    
            logger.info("Starting data ingestion process.")
            self.download_csv_from_gcp()    
            self.split_data()
            logger.info("Data ingestion process completed successfully.")
        except Exception as e:
            logger.error(f"Error during data ingestion: {e}")
            raise CustomException(f"Failed during data ingestion process", e)
        finally:
            logger.info("Data ingestion process finished.")

if __name__ == "__main__":
    data_ingestion = DataIngestion(read_yaml_file(CONFIG_PATH))
    try:
        data_ingestion.run()
    except CustomException as e:
        logger.error(f"Custom exception caught: {e}")
    finally:
        logger.info("Data ingestion process finished.")
# This code is designed to download a CSV file from Google Cloud Storage, split it into training and testing sets, and save the results locally.
# It uses the Google Cloud Storage client library to handle the download and pandas for data manipulation.
# The code also includes error handling and logging to provide detailed information about the process.