from ..base_problem import BaseProblem
from math import log2



class DummyProblem(BaseProblem):
    """
    Construct an instance of DummyProblem. Contains the parameters to optimize
    over.

    INPUT:

    - ``problem_parameter1`` -- First parameter of the problem
    - ``problem_parameter2`` -- Second parameter of the problem
    - ``nsolutions`` -- number of solutions of the problem in logarithmic scale
    """

    def __init__(self, problem_parameter1: float, problem_parameter2: float, **kwargs):
        super().__init__(**kwargs)

        # implement restrictions if apply e.g.
        if problem_parameter1 < problem_parameter2:
            raise ValueError("Parameter1 needs to be larger or equal than Parameter2")

        self.parameters["Parameter1"] = problem_parameter1
        self.parameters["Parameter2"] = problem_parameter2

        self.nsolutions = kwargs.get("nsolutions", max(self.expected_number_solutions(), 0))

    def to_bitcomplexity_time(self, basic_operations: float):
        """
        Returns the bit-complexity corresponding to a certain amount of basic_operations

        INPUT:

        - ``basic_operations`` -- Number of basic operations (logarithmic)

        """
        p1 = self.parameters["Parameter1"]
        bit_complexity_of_one_basic_operation = log2(p1) + 4
        return basic_operations + bit_complexity_of_one_basic_operation

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """
        Returns the memory bit-complexity associated to a given number of elements to store

        INPUT:

        - ``elements_to_store`` -- number of memory operations (logarithmic)

        """
        logarithm_of_bits_required_to_store_one_basic_element = 4
        return elements_to_store + logarithm_of_bits_required_to_store_one_basic_element

    def expected_number_solutions(self):
        """
        Returns the logarithm of the expected number of existing solutions to the problem

        """
        return self.parameters["Parameter1"] - self.parameters["Parameter2"]

    def get_parameters(self):
        """
        Returns the optimizations parameters
        """
        par1 = self.parameters["Parameter1"]
        par2 = self.parameters["Parameter2"]
        return par1, par2

    def __repr__(self):
        """
        """
        par1, par2 = self.get_parameters()
        rep = "dummy problem with (problem_parameter1, problem_parameter2) = " \
              + "(" + str(par1) + "," + str(par2) + ")"

        return rep


