"""
This module appends the structure for the new estimator into the input_dicitonary.json
"""


import os


class AppendEstimator():
    def __init__(self, estimator_prefix):
        self.upper_estimator_prefix = estimator_prefix.upper()
        self.lower_estimator_prefix = estimator_prefix.lower()

    def write(self):
        f = open("./input_dictionary.json", "rb+")
        f.seek(-8, 2)
        new_estimator_content = "},\n" + self.get_estimator_content()
        f.write(new_estimator_content.encode('ascii'))
        f.close()

    def get_estimator_content(self):
        tabs = "\t" * 2
        template = f"{tabs}"+"{\n" + \
            f"{tabs}" + f"\"estimator_id\": \"{self.upper_estimator_prefix}Estimator\",\n" + \
            f"{tabs}" + f"\"algorithm_id\": \"{self.upper_estimator_prefix}Algorithm\",\n" + \
            f"{tabs}" + "\"display_label\": \"Dummy Problem Estimator\",\n" + \
            f"{tabs}" + "\"landing_page_content\": \"# Dummy Markdown + Tex Landing Page\",\n" + \
            self.get_problem_parameters() + \
            self.get_estimators_parameters() + \
            f"{tabs}" + "\"optional_parameters\":[]\n" + \
            f"{tabs}" + "}\n" \
            "\t]\n" \
            "}"
        return template

    def get_problem_parameters(self):
        tabs = "\t"
        template = f"{tabs}" * 2 + "\"problem_parameters\": [\n" + \
            f"{tabs}" * 3 + "{\n" + \
            f"{tabs}" * 4 + "\"id\": \"Parameter1\",\n" + \
            f"{tabs}" * 4 + "\"type\": \"number\",\n" + \
            f"{tabs}" * 4 + "\"display_label\": \"Parameter 1\",\n" + \
            f"{tabs}" * 4 + "\"placeholder\": \"Insert parameter\",\n" + \
            f"{tabs}" * 4 + "\"tooltip\": \"This is the first problem parameter\",\n" + \
            f"{tabs}" * 3 + "}\n" + \
            f"{tabs}" * 2 + "],\n"
        return template

    def get_estimators_parameters(self):
        tabs = "\t"
        template = f"{tabs}" * 2 + "\"estimator_parameters\": [\n" + \
            f"{tabs}" * 3 + "{\n" + \
            f"{tabs}" * 4 + "\"id\": \"included_algorithms\",\n" + \
            f"{tabs}" * 4 + "\"type\": \"multiple_selector\",\n" + \
            f"{tabs}" * 4 + "\"direction\": \"column\",\n" + \
            f"{tabs}" * 4 + "\"display_label\": \"Included algorithms\",\n" + \
            f"{tabs}" * 4 + "\"tooltip\": \"Algorithms to include for optimization\",\n" + \
            f"{tabs}" * 4 + "\"default_value\": [],\n" + \
            f"{tabs}" * 4 + "\"excluded_algorithms\": [],\n" + \
            f"{tabs}" * 4 + "\"options\": [],\n" + \
            f"{tabs}" * 4 + "\"dependencies\": []\n" + \
            f"{tabs}" * 3 + "}\n" + \
            f"{tabs}" * 2 + "],\n"
        return template

    def get_algorithms_init_content(self):
        template = f"from .sample import Sample\n" + \
                    "# TODO: Remember to add the algorithms to the import above"
        return template
