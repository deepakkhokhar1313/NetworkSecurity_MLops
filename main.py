from networksecurity.exceptionHandling.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import DataIngestionArtifact

from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
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
    except Exception as e:
        raise NetworkSecurityException(e, sys)