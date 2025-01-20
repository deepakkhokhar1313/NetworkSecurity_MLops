from networksecurity.exceptionHandling.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

import yaml
import os,sys
import numpy as np
import dill
import pickle

def read_yaml_file(file_path: str) ->dict:
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e

def write_yaml_file(file_path: str, content: object, replece:bool = False) ->None:
    try:
        if replece:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_numpy_array_data(file_path:str, array:np.array):
    '''
    Save uumpy array data to file
    file path: location to save.
    array: the array that to be saved.
    '''
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_object(file_path:str, obj:object) -> None:
    try:
        logging.info("Entered the save object method of mainutils class")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("exited the saved_object method of mainutils class.")
    except Exception as e:
        raise NetworkSecurityException(e,sys)