"""
This module generates the Algorithm class
"""
from .base_file_creator import BaseFileCreator

class CreateAlgorithm(BaseFileCreator):

    def write(self):
        f = open(f"{self.estimator_path}/{self.lowercase_prefix}_algorithm.py", "w", encoding="utf8")
        f.write(self._get_file_content())
        f.close()

    def _get_file_content(self):
        """
        Generates the file with the imports and the class definition
        """
        with open(self.algorithms_path + '/DummyEstimator/dummy_algorithm.py', 'r') as file:
            data = file.read()
        return data