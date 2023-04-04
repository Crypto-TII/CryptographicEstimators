"""
This module generates the Estimator class
"""
from .base_file_creator import BaseFileCreator


class CreateProblem(BaseFileCreator):

    def write(self):
        f = open(
            f"{self.estimator_path}/{self.lowercase_prefix}_problem.py", "w", encoding="utf8")
        f.write(self._get_file_content())
        f.close()

    def _get_file_content(self):
        """
        Generates the file with the imports and the class definition
        """
        with open('./scripts/templates/problem.py', 'r') as file:
            data = file.read()
            return data.replace('$$UPPER_CASE_PREFIX$$', self.uppercase_prefix)
