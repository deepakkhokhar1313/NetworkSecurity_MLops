import os
import sys
import numpy as np
import pandas as pd

'''
Defining common constant variable fo training pipeline
'''
TARGET_COLUMN = "class"
PIPELINE_NAME:str = "NetworkSecurity"
ARTIFACT_DIR:str = "Artifacts"
FILE_NAME:str = "phishing.csv"

TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"
SCHEMA_FILE_PATH = os.path.join("data_schema","schema.yaml")

'''
Data Ingestion related constant start with DATA_INGESTION var name
'''

DATA_INGESTION_COLLECTION_NAME:str = "NETWORKSECURITY"
DATA_INGESTION_DATABASE_NAME: str = "DEEPAK"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = "ingsted"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION:float = 0.2

'''
Data Validation related constant start with DATA_VALIDATION var name
'''
DATA_VALIDATION_DIR_NAME:str = "data_validation"
DATA_VALIDATION_VALID_DIR:str = "validated"
DATA_VALIDATION_INVALID_DIR:str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str = "report.yaml"

'''
Data Transformation related constant start with DATA_TRANSFORMATION var name
'''
DATA_TRANSFORMATION_DIR_NAME:str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str = "transformed_object"
PREPROCESSING_OBJECT_FILE_NAME:str="preprocessing.pkl"

# KKN imputer to replace nan values
DATA_TRANSFORMATION_IMPUTER_PARAMS:dict = {
    "missing_values":np.nan,
    "n_neighbors":3,
    "weights":"uniform",
}
