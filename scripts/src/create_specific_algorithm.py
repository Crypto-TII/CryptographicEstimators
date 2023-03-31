"""
This module generates the Estimator class
"""
from .base_file_creator import BaseFileCreator

class CreateSpecificAlgorithm(BaseFileCreator):

    def write(self):
        f = open(f"{self.estimator_path}/dummy_algorithm1.py", "w", encoding="utf8")
        f.write(self._get_file_content())
        f.close()

    def _get_file_content(self):
        """
        Generates the file with the imports and the class definition
        """
        with open(self.algorithms_path + '/DummyEstimator/DummyAlgorithms/dummy_algorithm1.py', 'r') as file:
            data = file.read()
            data = data.replace('DummyAlgorithm', self.uppercase_prefix + 'Algorithm')
            data = data.replace('DummyProblem', self.uppercase_prefix + 'Problem')
            data = data.replace('DummyEstimator', self.uppercase_prefix + 'Estimator')
            return data.replace('DummyAlgorithm1', self.uppercase_prefix + 'Algorithm1')
        
