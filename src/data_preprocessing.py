import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml_file, load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)

class DataPreprocessor:
    
    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        if not os.path.exists(processed_dir):
            os.makedirs(processed_dir)
        self.label_encoder = LabelEncoder()
        self.smote = SMOTE(random_state=42)
        self.config = read_yaml_file(config_path)

    def preprocess_data(self, df):
        try:
            logger.info("Starting data preprocessing.")
            logger.info("Dropping the columns.")
            df.drop(columns=['Unnamed: 0','Booking_ID'], inplace=True)
            df.drop_duplicates(inplace=True)
            
            cat_cols = self.config["data_processing"]["categorical_columns"]
            num_cols = self.config["data_processing"]["numerical_columns"]
            logger.info("Applying label encoding to categorical columns.")
            label_encoder = LabelEncoder()
            mappings = {}
            for col in cat_cols:
                df[col] = label_encoder.fit_transform(df[col])
                mappings[col] = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))
            logger.info("Label encoding mappings are: ")
            for col, mapping in mappings.items():
                logger.info(f"{col}: {mapping}")
            logger.info("Applying skewness handling.")
            skew_theshold = self.config["data_processing"]["skewness_threshold"]
            skewness = df[num_cols].apply(lambda x: x.skew()).sort_values(ascending=False)
            
            for column in skewness[skewness > skew_theshold].index:
                df[column] = np.log1p(df[column])
            logger.info("Skewness handling completed.")
            
            return df
        except Exception as e:
            logger.error(f"Error during data preprocessing: {e}")           
            raise CustomException(f"Failed during data preprocessing", e)

    def balance_data(self, df):
        try:
            logger.info("Starting data balancing.")
            X = df.drop(columns=['booking_status'])
            y = df['booking_status']
            logger.info(f"Shape of X: {X.shape}, Shape of y: {y.shape}")
            logger.info("Starting data balancing using SMOTE.")
            X_resampled, y_resampled = self.smote.fit_resample(X, y)
            balanced_df = pd.DataFrame(X_resampled, columns=X.columns)
            balanced_df['booking_status'] = y_resampled
            logger.info("Data balancing completed.")
            logger.info(f"Shape of balanced data: {balanced_df.shape}")
            return balanced_df
        except Exception as e:
            logger.error(f"Error during data balancing: {e}")
            raise CustomException(f"Failed during data balancing", e)

    def select_features(self, df):
        try:
            logger.info("Starting feature selection.")
            X = df.drop(columns=['booking_status'])
            y = df['booking_status']
            model = RandomForestClassifier()
            model.fit(X, y)
            importances = model.feature_importances_
            feature_importances_df = pd.DataFrame({'Feature': X.columns, 'Importance': importances})
            feature_importances_df = feature_importances_df.sort_values(by='Importance', ascending=False)
            logger.info("Feature importances calculated.")
            num_features_to_select = self.config["data_processing"]["num_features_to_select"]
            if num_features_to_select > len(X.columns):
                raise ValueError(f"Number of features to select {num_features_to_select} exceeds available features {len(X.columns)}")
            topk_features = feature_importances_df.head(num_features_to_select)['Feature'].values
            logger.info(f"Top {num_features_to_select} features:")
            for feature in topk_features:
                logger.info(feature)
            logger.info("Feature importances:")
            for feature, importance in zip(X.columns, importances):
                logger.info(f"{feature}: {importance}")
            logger.info("Feature selection completed.")
            topk_df = df[topk_features.tolist() + ['booking_status']]
            logger.info(f"Shape of data after feature selection: {topk_df.shape}")
            return topk_df
        except Exception as e:
            logger.error(f"Error during feature selection: {e}")
            raise CustomException(f"Failed during feature selection", e)
        finally:
            logger.info("Feature selection process finished.")
            
    def save_processed_data(self, df, file_path):
        try:
            logger.info(f"Saving processed data to {file_path}")
            df.to_csv(file_path, index=False)
            logger.info("Processed data saved successfully.")
        except Exception as e:
            logger.error(f"Error saving processed data: {e}")
            raise CustomException(f"Failed to save processed data", e)
        finally:
            logger.info("Data saving process finished.")

    def process(self):
        try:
            logger.info("Starting data processing.")
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)
            
            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)
            
            train_df = self.balance_data(train_df)
            test_df = self.balance_data(test_df)
            
            train_df = self.select_features(train_df)
            test_df = test_df[train_df.columns]
            
            self.save_processed_data(train_df, PROCESSED_TRAIN_PATH)
            self.save_processed_data(test_df, PROCESSED_TEST_PATH)
            
            logger.info("Data processing completed successfully.")
        except Exception as e:
            logger.error(f"Error during data preprocessing: {e}")
            raise CustomException(f"Failed during data preprocessing", e)
        finally:
            logger.info("Data preprocessing process finished.")


if __name__ == "__main__":
    try:
        data_preprocessor = DataPreprocessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
        data_preprocessor.process()
    except CustomException as e:
        logger.error(f"Custom exception caught: {e}")
    finally:
        logger.info("Data preprocessing process finished.")