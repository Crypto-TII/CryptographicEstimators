"""
This module generates the Constants file
"""
from .base_file_creator import BaseFileCreator


class CreateConstants(BaseFileCreator):

    def write(self):
        f = open(f"{self.estimator_path}/{self.lowercase_prefix}_constants.py", "w", encoding="utf8")
        f.close()

    def _get_file_content(self):
        pass

