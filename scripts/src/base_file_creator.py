from abc import ABC, abstractmethod


class BaseFileCreator(ABC):
    def __init__(self, estimator_prefix, estimator_path, algorithms_path):
        self.estimator_path = estimator_path
        self.algorithms_path = algorithms_path
        self.lowercase_prefix = estimator_prefix.lower()
        self.uppercase_prefix = estimator_prefix.upper()

    @abstractmethod
    def write(self):
        pass

    @abstractmethod
    def _get_file_content(self):
        pass

    # @abstractmethod
    # def _create_imports(self):
    #     pass

    # @abstractmethod
    # def _create_class(self):
    #     pass

    # @abstractmethod
    # def _create_constructor(self):
    #     pass

    # def _create_methods(self):
    #     pass
