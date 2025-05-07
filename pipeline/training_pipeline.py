from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataPreprocessor
from src.model_training import ModelTraining
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml_file
import os


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.info("Starting the training pipeline.")
    data_ingestion = DataIngestion(read_yaml_file(CONFIG_PATH))
    try:
        data_ingestion.run()
    except CustomException as e:
        logger.error(f"Custom exception caught: {e}")
    finally:
        logger.info("Data ingestion process finished.")
            
    # Data Preprocessing
    try:
        data_preprocessor = DataPreprocessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
        data_preprocessor.process()
    except CustomException as e:
        logger.error(f"Custom exception caught: {e}")
    finally:
        logger.info("Data preprocessing process finished.")
            
    # Model Training
    try:
        model_trainer = ModelTraining(PROCESSED_TRAIN_PATH, PROCESSED_TEST_PATH, MODEL_OUTPUT_PATH)
        model_trainer.run()
    except CustomException as e:
        logger.error(f"Custom exception caught: {e}")
    finally:
        logger.info("Model training process finished.")
    logger.info("Training pipeline completed.")
    logger.info("All processes finished successfully.")