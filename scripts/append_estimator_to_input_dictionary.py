"""
This module appends the structure for the new estimator into the input_dicitonary.json
"""
import json


class AppendEstimator():
    def __init__(self):
        estimator_prefix = input(
            "Enter a prefix for your Estimator (For example for SyndromeDecoding we use SD): ")
        self.estimator_prefix = estimator_prefix
        self.estimator_label = input("Enter the estimator full name: ")
        self.upper_estimator_prefix = self.estimator_prefix.upper()

    def write(self):
        with open("./input_dictionary.json", "r") as file:
            data = json.load(file)

            data["estimators"].append(
                json.loads(self.get_estimator_content()))
        json.dump(data, open("./input_dictionary.json", "w"), indent=2)

    def get_estimator_content(self):
        template = open(
            "./scripts/templates/input_dictionary_template.json").read()
        template = template.replace("$$UPPER_CASE_PREFIX$$",
                                    self.upper_estimator_prefix)
        template = template.replace("$$DISPLAY_LABEL$$",
                                    self.estimator_label)
        return template


ae = AppendEstimator()
ae.write()
