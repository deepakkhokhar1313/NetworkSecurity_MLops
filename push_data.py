import os
import sys
import json
# certifi is a python package that is used to provide truted certificat 
# when communicate https/tls/ssl server
import certifi
import pandas as pd
import numpy as np
import pymongo
from networksecurity.exceptionHandling.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
ca = certifi.where() # ca - certificate Authority(will store certificate created by certifi)

class NetworkDataExtract():
    def __init__(self, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.records = []

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]

            self.collection = self.database[self.collection]
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def csv_to_json_converter(sef, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def insert_data_to_mongodb(self, records):
        try:
            self.records = records

            self.collection.insert_many(self.records)
            return(len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e, sys)

if __name__=="__main__":
    FILE_PATH = "Network_Data/phishing.csv"
    DATABASE = "DEEPAK"
    COLLECTION = "NETWORKSECURITY"
    networkobj = NetworkDataExtract(DATABASE, COLLECTION)
    records = networkobj.csv_to_json_converter(FILE_PATH)
    # print(records)
    no_of_records = networkobj.insert_data_to_mongodb(records)
    print(no_of_records)





