import os

RAW_DIR = "artifacts/raw"
RAW_FILE_PATH = os.path.join(RAW_DIR, "raw.csv")
TRAIN_FILE_PATH = os.path.join(RAW_DIR, "train.csv")
TEST_FILE_PATH = os.path.join(RAW_DIR, "test.csv")

CONFIG_PATH = "config/data_ingestion.yaml"
GCP_CREDENTIALS_PATH = "secrets/mlopsproject1-458817-b324618844db.json"
######### DATA PRCOCESSING #########

PROCESSED_DIR = "artifacts/processed"       
PROCESSED_TRAIN_PATH = os.path.join(PROCESSED_DIR, "processed_train.csv")
PROCESSED_TEST_PATH = os.path.join(PROCESSED_DIR, "processed_test.csv")
PROCESSED_MODEL_PATH = os.path.join(PROCESSED_DIR, "processed_model.pkl")

########## MODEL TRAINING ###########
MODEL_OUTPUT_PATH = "artifacts/models/lgbm_model.pkl"
