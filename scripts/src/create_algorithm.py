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
        return self._create_imports() + self._create_class()

    def _create_imports(self):
        return "from ..base_algorithm import BaseAlgorithm\n\n\n"

    def _create_class(self):
        """
        Generates the class with the constructor
        """
        template = f"class {self.uppercase_prefix}Algorithm(BaseAlgorithm):\n\n"
        return template + self._create_constructor() + self._create_methods()

    def _create_constructor(self):
        """
        Generates the __init__ method for the Algorithm class
        """
        template = "\tdef __init__(self, problem, **kwargs):\n" + \
            f"\t\tsuper({self.uppercase_prefix}Algorithm, self).__init__(problem, **kwargs)\n\n"
        return template

    def _create_methods(self):
        """
        Generates the methods to be ovewritten
        """
        template = "\tdef __repr__(self):\n" + \
            "\t\tpass\n\n"
        return template
