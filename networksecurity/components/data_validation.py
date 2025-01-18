from networksecurity.exceptionHandling.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifacts
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH



from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file
from scipy.stats import ks_2samp
import pandas as pd
import os, sys

class DataValidation:
    def __init__(self, data_ingestion_artifacts:DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifacts = data_ingestion_artifacts
            self.schema = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def validate_number_of_columns(self, dataframe:pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self.schema)
            logging.info(f"Required no of columns{number_of_columns}")
            logging.info(f"Dataframe's no of columns{len(dataframe.columns)}")

            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def detect_dataset_drift(self, base_df, current_df, threshold=0.05) -> bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                # ks_2samp is used to match the distribution of two columns
                is_same_dist = ks_2samp(d1,d2)
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update(
                    {
                        column:{
                            "p_value": float(is_same_dist.pvalue),
                            "drift_status":is_found
                        }
                    }
                )
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            # creating directory for report
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,
                            content=report)
            return status
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_validation(self) -> DataValidationArtifacts:
        try:
            training_file_path = self.data_ingestion_artifacts.trained_file_path
            test_file_path = self.data_ingestion_artifacts.test_file_path

            ## Read the data
            train_dataframe = DataValidation.read_data(training_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            # validate number of columns
            status = self.validate_number_of_columns(train_dataframe)
            if not status:
                error_message = f"Train Datframe doesn't contain all columns.\n"
            
            status = self.validate_number_of_columns(test_dataframe)
            if not status:
                error_message = f"test Datframe doesn't contain all columns.\n"
            
            status = self.detect_dataset_drift(base_df=train_dataframe, 
                                               current_df=test_dataframe)
            # if not status:
            #     error_message = f"There  is an drift in train and test data distribution.\n"
            
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path,
                index=False,
                header=True
            )
            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path,
                index=False,
                header=True
            )

            data_validation_artifacts = DataValidationArtifacts(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifacts.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifacts.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            return data_validation_artifacts
        except Exception as e:
            raise NetworkSecurityException(e,sys)
