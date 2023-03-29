"""
This module generates the Estimator class
"""
from .base_file_creator import BaseFileCreator

class CreateEstimator(BaseFileCreator):

    def write(self):
        f = open(f"{self.estimator_path}/{self.lowercase_prefix}_estimator.py", "w", encoding="utf8")
        f.write(self._get_file_content())
        f.close()

    def _get_file_content(self):
        """
        Generates the file with the imports and the class definition
        """
        return self._create_imports() + self._create_class()

    def _create_imports(self):
        """
        Generates the imports at the top of the file
        """
        template = f"from ..{self.uppercase_prefix}Estimator.{self.lowercase_prefix}_algorithm import {self.uppercase_prefix}Algorithm\n" + \
            f"from ..{self.uppercase_prefix}Estimator.{self.lowercase_prefix}_problem import {self.uppercase_prefix}Problem\n" + \
            f"from ..base_estimator import BaseEstimator\n" + \
            "from math import inf\n\n\n"
        return template

    def _create_class(self):
        """
        Generates the class with the constructor
        """
        template = f"class {self.uppercase_prefix}Estimator(BaseEstimator):\n" + \
            "\t\"\"\" \n\n" + \
            "\tINPUT:\n\n" + \
            "\t- ``excluded_algorithms`` -- a list/tuple of excluded algorithms (default: None)\n\n" + \
            "\t\"\"\" \n" + \
            "\texcluded_algorithms_by_default = []\n\n"
        return template + self._create_constructor()

    def _create_constructor(self):
        """
        Generates the __init__ method for the Estimator class
        """
        template = "\tdef __init__(self, memory_bound=inf, **kwargs):  # Add problem parameters\n" + \
            "\t\tif not kwargs.get(\"excluded_algorithms\"):\n" + \
            "\t\t\tkwargs[\"excluded_algorithms\"] = []\n\n" + \
            "\t\tkwargs[\"excluded_algorithms\"] += self.excluded_algorithms_by_default\n" + \
            f"\t\tsuper({self.uppercase_prefix}Estimator, self).__init__({self.uppercase_prefix}Algorithm, {self.uppercase_prefix}Problem(memory_bound=memory_bound, **kwargs), **kwargs)\n"
        return template
