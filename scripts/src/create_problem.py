"""
This module generates the Estimator class
"""
from .base_file_creator import BaseFileCreator

class CreateProblem(BaseFileCreator):

    def write(self):
        f = open(f"{self.estimator_path}/{self.lowercase_prefix}_problem.py", "w", encoding="utf8")
        f.write(self._get_file_content())
        f.close()

    def _get_file_content(self):
        """
        Generates the file with the imports and the class definition
        """
        return self._create_imports() + self._create_class()

    def _create_imports(self):
        return "from ..base_problem import BaseProblem\n\n\n"

    def _create_class(self):
        """
        Generates the class with the constructor
        """
        template = f"class {self.uppercase_prefix}Problem(BaseProblem):\n\n"
        return template + self._create_constructor() + self._create_methods()

    def _create_constructor(self):
        """
        Generates the __init__ method for the Problem class
        """
        template = "\tdef __init__(self, **kwargs): # Fill with parameters\n" + \
            "\t\tsuper().__init__(**kwargs)\n\n"
        return template

    def _create_methods(self):
        """
        Generates the methods to be ovewritten
        """
        template = "\tdef to_bitcomplexity_time(self, basic_operations):\n" + \
            "\t\tpass\n\n" + \
            "\tdef to_bitcomplexity_memory(self, basic_operations):\n" + \
            "\t\tpass\n\n" + \
            "\tdef expected_number_solutions(self):\n" + \
            "\t\tpass\n\n" + \
            "\tdef __repr__(self):\n" + \
            "\t\tpass\n\n" + \
            "\tdef get_parameters(self):\n" + \
            "\t\tpass\n\n"
        return template
