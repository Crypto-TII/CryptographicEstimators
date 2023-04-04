"""
This module contains a script that generates all the scaffolding
code for a new estimator via the console.
"""
from os import path, mkdir, system
from src.create_algorithm import CreateAlgorithm
from src.create_estimator import CreateEstimator
from src.create_problem import CreateProblem
from src.create_specific_algorithm import CreateSpecificAlgorithm
from src.create_init import CreateInit
from src.create_constant import CreateConstants


class EstimatorGenerator():
    """
    Creates all the files and folders for implementation ready estimator
    """

    def __init__(self):
        estimator_prefix = input(
            "Enter a prefix for your Estimator (For example for SyndromeDecoding you could use SD): ")
        self.estimator_folder_name = estimator_prefix.upper() + "Estimator"
        self.algorithms_folder_name = estimator_prefix.upper() + "Algorithms"
        self.estimator_path = ""
        self.algorithms_path = ""
        self.estimator_prefix = estimator_prefix
        self.absolute_library_path = path.abspath("cryptographic_estimators")

    def create_estimator_folders(self):
        """
        Creates the estimator folder and the nested algorithms folder
        """
        print("# Creating folders...")

        self.estimator_path = path.join(
            self.absolute_library_path, self.estimator_folder_name)
        self.algorithms_path = path.join(
            self.estimator_path, self.algorithms_folder_name)

        self.__create_folder(self.estimator_path, self.estimator_folder_name)
        self.__create_folder(self.algorithms_path, self.algorithms_folder_name)

    def __create_folder(self, folder_path, folder_name):
        try:
            mkdir(folder_path, mode=0o777)
        except OSError as error:
            print(
                f"The directory {folder_name} already exits, please choose another name")
            print(error)

    def create_estimator_files(self):
        """
        Creates the Estimator,Problem, Algorithm and a Sample algorithm files
        """
        print("# Creating files...")
        CreateProblem(self.estimator_prefix, self.estimator_path,
                      self.absolute_library_path).write()
        CreateEstimator(self.estimator_prefix, self.estimator_path,
                        self.absolute_library_path).write()
        CreateAlgorithm(self.estimator_prefix, self.estimator_path,
                        self.absolute_library_path).write()
        CreateConstants(self.estimator_prefix, self.estimator_path,
                        self.absolute_library_path).write()
        CreateSpecificAlgorithm(
            self.estimator_prefix, self.algorithms_path).write()

    def create_init_files(self):
        """
        Create the init files for the package
        """
        print("# Creating init files...")
        CreateInit(self.estimator_prefix).write_estimator_init(
            self.estimator_path)
        CreateInit(self.estimator_prefix).write_algorithms_init(
            self.algorithms_path)

    def done(self):
        """Prints a done message"""
        print(
            f"# Done! You can now start by editing the files inside '{self.estimator_path}' and the input_dictionary")
        system('tree -d -I __pycache__ cryptographic_estimators')


eg = EstimatorGenerator()
eg.create_estimator_folders()
eg.create_estimator_files()
eg.create_init_files()
eg.done()
