"""
This module generates the init files for the Estimator and for the Algorithms of the estimator
"""

class CreateInit():
    def __init__(self, estimator_prefix):
        self.upper_estimator_prefix = estimator_prefix.upper()
        self.lower_estimator_prefix = estimator_prefix.lower()

    def write_estimator_init(self, estimator_path):
        file = open(f"{estimator_path}/__init__.py", "w", encoding="utf8")
        file.write(self.get_estimator_init_content())
        file.close()

    def get_estimator_init_content(self):
        template = f"from .{self.lower_estimator_prefix}_algorithm import {self.upper_estimator_prefix}Algorithm\n" + \
                  f"from .{self.lower_estimator_prefix}_estimator import {self.upper_estimator_prefix}Estimator\n" + \
                  f"from .{self.lower_estimator_prefix}_problem import {self.upper_estimator_prefix}Problem\n" + \
                  f"from .{self.upper_estimator_prefix}Algorithms import {self.upper_estimator_prefix}Algorithm1\n" + \
                  "# TODO: Remember to add the algorithms to the import above"
        return template

    def write_algorithms_init(self, algorithm_path):
        file = open(f"{algorithm_path}/__init__.py", "w", encoding="utf8")
        file.write(self.get_algorithms_init_content())
        file.close()

    def get_algorithms_init_content(self):
        template = f"from .{self.lower_estimator_prefix}_algorithm1 import {self.upper_estimator_prefix}Algorithm1\n" + \
                    "# TODO: Remember to add the algorithms to the import above"
        return template
