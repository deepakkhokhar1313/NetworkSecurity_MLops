from networksecurity.exceptionHandling.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import DataIngestionArtifact

from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig,ModelTrinerConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
import sys

if __name__ == "__main__":
    try:
        trainingPipelineConfig = TrainingPipelineConfig()
        dataIngestionConfig = DataIngestionConfig(trainingPipelineConfig)

        data_ingestion = DataIngestion(dataIngestionConfig)
        logging.info(
            "Initiate the data ingestion."
        )
        dataIngestionArtifact = data_ingestion.initiate_data_ingestion()
        print(dataIngestionArtifact)
        logging.info(
            "Data Ingestion completed."
        )
        

        data_validation_config = DataValidationConfig(trainingPipelineConfig)
        data_validation = DataValidation(dataIngestionArtifact,data_validation_config)
        logging.info(
            "Data Validation started."
        )
        data_validation_artifacts = data_validation.initiate_data_validation()
        logging.info(
            "Data Validation completed."
        )
        print(data_validation_artifacts)

        logging.info("Data transformation started.")
        data_transformation_config = DataTransformationConfig(trainingPipelineConfig)
        data_transformation = DataTransformation(data_validation_artifacts,
                                                 data_transformation_config)
        data_transformation_artifacts = data_transformation.initiate_data_transformation()
        print(data_transformation_artifacts)
        logging.info("Data transformation completed.")

        logging.info("Model Trainer Started")
        model_trainer_config = ModelTrinerConfig(trainingPipelineConfig)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,
                                     data_transformation_artifacts=data_transformation_artifacts)
        model_trainer_artifacts = model_trainer.initiate_model_trainer()
        print(model_trainer_artifacts)
        logging.info("Model Training completed.")
    except Exception as e:
        raise NetworkSecurityException(e, sys)