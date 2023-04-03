"""
This module generates the Estimator class
"""
from .base_file_creator import BaseFileCreator


class CreateEstimator(BaseFileCreator):

    def write(self):
        f = open(
            f"{self.estimator_path}/{self.lowercase_prefix}_estimator.py", "w", encoding="utf8")
        f.write(self._get_file_content())
        f.close()

    def _get_file_content(self):
        """
        Generates the file with the imports and the class definition
        """
        with open(self.algorithms_path + '/DummyEstimator/dummy_estimator.py', 'r') as file:
            data = file.read()
            data = data.replace('$$Dummy$$', self.uppercase_prefix)
            data = data.replace('$$dummy$$', self.lowercase_prefix)
        return data
