"""
This module generates the Estimator class
"""
from .base_file_creator import BaseFileCreator


class CreateSpecificAlgorithm():

    def __init__(self, estimator_prefix, algortihms_path):
        self.algorithms_path = algortihms_path
        self.lowercase_prefix = estimator_prefix.lower()
        self.uppercase_prefix = estimator_prefix.upper()

    def write(self,):
        f = open(f"{self.algorithms_path}/{self.lowercase_prefix}_algorithm1.py",
                 "w", encoding="utf8")
        f.write(self._get_file_content())
        f.close()

    def _get_file_content(self):
        """
        Generates the file with the imports and the class definition
        """
        with open('./scripts/templates/specific_algorithm.py', 'r') as file:
            data = file.read()
            data = data.replace('$$UPPER_CASE_PREFIX$$', self.uppercase_prefix)
            data = data.replace('$$lower_case_prefix$$', self.lowercase_prefix)
            return data
