"""
This module generates the Estimator class
"""
from .base_file_creator import BaseFileCreator

class CreateSpecificAlgorithm(BaseFileCreator):

    def write(self):
        f = open(f"{self.estimator_path}/sample.py", "w", encoding="utf8")
        f.write(self._get_file_content())
        f.close()

    def _get_file_content(self):
        """
        Generates the file with the imports and the class definition
        """
        return self._create_imports() + self._create_class()

    def _create_imports(self):
        return f"from ...{self.uppercase_prefix}Estimator.{self.lowercase_prefix}_algorithm import {self.uppercase_prefix}Algorithm\n" + \
            f"from ...{self.uppercase_prefix}Estimator.{self.lowercase_prefix}_problem import {self.uppercase_prefix}Problem\n\n\n"

    def _create_class(self):
        """
        Generates the class with the constructor
        """
        template = f"class Sample({self.uppercase_prefix}Algorithm):\n\n"
        return template + self._create_constructor() + self._create_methods()

    def _create_constructor(self):
        """
        Generates the __init__ method for the Algorithm class
        """

        template = f"\tdef __init__(self, problem: {self.uppercase_prefix}Problem, **kwargs):\n" + \
            "\t\tsuper().__init__(problem, **kwargs)\n\n"
        return template

    def _create_methods(self):
        """
        Generates the methods to be ovewritten
        """
        template = "\tdef _compute_time_complexity(self, parameters):\n" + \
            "\t\tpass\n\n" + \
            "\tdef _compute_memory_complexity(self, parameters):\n" + \
            "\t\tpass\n\n"
        return template
