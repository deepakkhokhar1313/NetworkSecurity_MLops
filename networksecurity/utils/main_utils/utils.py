from networksecurity.exceptionHandling.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

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
    
def load_object(file_path:str) ->object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file {file_path} doesn't exist.")
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def load_numpy_array(file_path:str) -> np.array:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file {file_path} doesn't exist.")
        with open(file_path, "rb") as file_obj:
            array = np.load(file_obj)
        return array
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def evaluate_models(x_train,y_train,x_test,y_test,models,params):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = params[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(x_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(x_train,y_train)

            y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)

            train_model_score = r2_score(y_train,y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

            return report
    except Exception as e:
        raise NetworkSecurityException(e,sys)