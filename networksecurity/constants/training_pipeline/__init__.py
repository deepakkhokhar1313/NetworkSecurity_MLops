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

'''
Data Ingestion related constant start with DATA_INGESTION var name
'''

DATA_INGESTION_COLLECTION_NAME:str = "NETWORKSECURITY"
DATA_INGESTION_DATABASE_NAME: str = "DEEPAK"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = "ingsted"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION:float = 0.2
