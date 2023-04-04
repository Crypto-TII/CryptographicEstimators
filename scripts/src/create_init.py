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
        with open('./scripts/templates/estimator_init.py', 'r') as file:
            data = file.read()
            data = data.replace('$$lower_case_prefix$$',
                                self.lower_estimator_prefix)
            return data.replace('$$UPPER_CASE_PREFIX$$', self.upper_estimator_prefix)

    def write_algorithms_init(self, algorithm_path):
        file = open(f"{algorithm_path}/__init__.py", "w", encoding="utf8")
        file.write(self.get_algorithms_init_content())
        file.close()

    def get_algorithms_init_content(self):
        with open('./scripts/templates/algorithm_init.py', 'r') as file:
            data = file.read()
            data = data.replace('$$lower_case_prefix$$',
                                self.lower_estimator_prefix)
            return data.replace('$$UPPER_CASE_PREFIX$$', self.upper_estimator_prefix)
