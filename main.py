from networksecurity.exceptionHandling.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import DataIngestionArtifact

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.components.data_ingestion import DataIngestion
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
    except Exception as e:
        raise NetworkSecurityException(e, sys)