from networksecurity.exceptionHandling.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifacts,
    DataTransformationArtifacts,
    ModelTrainerArtifact
    )

from networksecurity.entity.config_entity import (
    DataIngestionConfig, 
    DataValidationConfig, 
    DataTransformationConfig,
    ModelTrinerConfig
    )

from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
import sys,os


class Trainingpipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.data_ingestion_config = DataIngestionConfig(
            training_pipeline_config=self.training_pipeline_config
        )
        self.data_validation_config = DataValidationConfig(
            training_pipeline_config= self.training_pipeline_config,
        )
        self.data_transformation_config = DataTransformationConfig(
            training_pipline_config=self.training_pipeline_config
        )
        self.model_trainer_config = ModelTrinerConfig(
            training_pipeline_config=self.training_pipeline_config
        )

    def start_data_ingestion(self):
        try:
            logging.info("Initiate the data ingestion.")
            data_ingestion = DataIngestion(
                self.data_ingestion_config,
            )
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data ingestion Completed and artifacts are : {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def start_data_validation(self, data_ingestion_artifacts = DataIngestionArtifact):
        try:
            logging.info("Initiate the data Validation.")
            data_validation = DataValidation(
                data_ingestion_artifacts= data_ingestion_artifacts,
                data_validation_config=self.data_validation_config,
            )
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"Data Validation Completed and artifacts are : {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_transformation(self, data_validation_artifacts = DataValidationArtifacts):
        try:
            logging.info("Initiate the data Transformation.")
            data_transformation = DataTransformation(
                data_validation_artifact= data_validation_artifacts,
                data_transformation_config= self.data_transformation_config,
            )
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info(f"Data Transformation Completed and artifacts are : {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    

    def start_model_trainer(self, data_transformation_artifacts = DataTransformationArtifacts):
        try:
            logging.info("Initiate the Model trainer.")
            model_trainer = ModelTrainer(
                data_transformation_artifacts= data_transformation_artifacts,
                model_trainer_config= self.model_trainer_config,
            )
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info(f"Model Trainer Completed and artifacts are : {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def run_pipeline(self):
        try:
            data_ingestion_artifacts = self.start_data_ingestion()
            data_validation_artifacts = self.start_data_validation(data_ingestion_artifacts)
            data_transformation_artifacts = self.start_data_transformation(data_validation_artifacts=data_validation_artifacts)
            model_trainer_artifacts = self.start_model_trainer(data_transformation_artifacts=data_transformation_artifacts)
            return model_trainer_artifacts
        except Exception as e:
            raise NetworkSecurityException(e, sys)