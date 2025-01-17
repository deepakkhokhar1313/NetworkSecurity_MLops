from dataclasses import dataclass
'''
Dataclasses are used as a decorator to make an empty class like without funtions
'''

@dataclass
class DataIngestionArtifact:
    trained_file_path:str
    test_file_path:str