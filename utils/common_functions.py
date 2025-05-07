import os
import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException
import yaml

logger = get_logger(__name__)
@staticmethod
def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns its content as a dictionary.
    
    Args:
        file_path (str): Path to the YAML file.
        
    Returns:
        dict: Content of the YAML file.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        if not file_path.endswith('.yaml') and not file_path.endswith('.yml'):
            raise ValueError(f"The file {file_path} is not a valid YAML file.")
        logger.info(f"Reading YAML file: {file_path}")
        with open(file_path, 'r') as file:
            content = yaml.safe_load(file)
        return content
    except Exception as e:
        logger.error(f"Error reading YAML file: {e}")
        raise CustomException(f"Error reading YAML file", e) 

def load_data(path):
    try:
        logger.info(f"Loading data from path: {path}")
        df = pd.read_csv(path)
        logger.info(f"Data loaded successfully with shape: {df.shape}")
        return df
    except Exception as e:
        logger.error(f"Error loading data from path: {path}, Error: {e}")
        raise CustomException(f"Failed to load data from path: {path}", e)