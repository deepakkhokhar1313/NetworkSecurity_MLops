from networksecurity.exceptionHandling.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

import os, sys

from networksecurity.entity.config_entity import ModelTrinerConfig
from networksecurity.entity.artifact_entity import ModelTrainerArtifact, DataTransformationArtifacts

from networksecurity.utils.main_utils.utils import load_numpy_array, save_object, load_object,evaluate_models
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
import mlflow
import dagshub

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)
from dotenv import load_dotenv
load_dotenv()

# Explicitly use the token for authentication
# dagshub.auth.add_app_token(os.getenv("DAGSHUB_TOKEN"))
dagshub.init(repo_owner='deepakkhokhar1313', 
            repo_name='NetworkSecurity_MLops', 
            mlflow=True,
             )

class ModelTrainer:
    def __init__(self,
                 model_trainer_config: ModelTrinerConfig,
                 data_transformation_artifacts: DataTransformationArtifacts):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifacts = data_transformation_artifacts
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def track_mlflow(self,best_model, classificationmetric):
        try:
            with mlflow.start_run():
                f1_score = classificationmetric.f1_score
                precision_score = classificationmetric.precision_score
                recall_score = classificationmetric.recall_score

                mlflow.log_metric("f1_score", f1_score)
                mlflow.log_metric("precision_score", precision_score)
                mlflow.log_metric("recall_score", recall_score)

                mlflow.sklearn.log_model(best_model,"model")

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def train_model(self, x_train, y_train, x_test, y_test):
        try:
            models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
            }

            params={
                "Decision Tree":{
                    'criterion':['gini','entropy','log_loss'],
                    # 'splitter':['best', 'random'],
                    # 'max_features':['sqrt','log2']
                },
                "Random Forest":{
                    # 'criterion':['gini','entropy','log_loss'],
                    # 'max_features':['sqrt','log2'],
                    'n_estimators':[8,16,32,64,128,256]
                },
                "Gradient Boost":{
                    # 'criterion':['gini','entropy','log_loss'],
                    # 'max_features':['sqrt','log2'],
                    # 'loss':['log_loss', 'exponential'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                    'n_estimators':[8,16,32,64,128,256]
                },
                "Logistic Regression":{},
                "AdaBoost":{
                    'learning_rate':[.1,.01,.05,.001],
                    'n_estimators':[8,16,32,64,128,256]
                }  
            }

            model_report:dict = evaluate_models(x_train,y_train,x_test,y_test,
                                            models=models,params=params)

            # To get the best model
            best_model_score = max(sorted(model_report.values()))

            # To get the best model name from dict
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]
            y_train_pred = best_model.predict(x_train)

            classification_train_metric = get_classification_score(y_true=y_train,
                                                             y_pred=y_train_pred)
            # track the experiment using mlflow
            self.track_mlflow(best_model, classification_train_metric)


            y_test_pred = best_model.predict(x_test)

            classification_test_metric = get_classification_score(y_true=y_test,
                                                             y_pred=y_test_pred)
            
            # track the experiment using mlflow
            self.track_mlflow(best_model, classification_test_metric)

            preprocessor = load_object(file_path=self.data_transformation_artifacts.transformed_object_file_path)

            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)

            network_model = NetworkModel(preprocessor=preprocessor,
                                         model=best_model)
            save_object(self.model_trainer_config.trained_model_file_path, obj=network_model)
            save_object("final_models/model.pkl",best_model)
            # Model trainer Artifacts
            model_trainer_artifacts = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact= classification_train_metric,
                test_metric_artifact=classification_test_metric,
            )

            return model_trainer_artifacts
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifacts.transformed_train_file_path
            test_file_path = self.data_transformation_artifacts.transformed_test_file_path

            #  Loadinig training array and testing array
            train_arr = load_numpy_array(train_file_path)
            test_arr = load_numpy_array(test_file_path)
            logging.info(f"train arr size is = {len(train_arr)} and test array size is {len(test_arr)}")
            x_train, y_train, x_test, y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1],
            )

            model = self.train_model(x_train,y_train, x_test, y_test)
            return model
        except Exception as e:
            raise NetworkSecurityException(e, sys)