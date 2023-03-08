from ..base_problem import BaseProblem


class SEProblem(BaseProblem):
    """
    Construct an instance of the Sub-Code Equivalence Problem

    INPUT:

    - ``n`` -- code length
    - ``k`` -- code dimension
    - ``nsolutions`` -- number of (expected) solutions of the problem in logarithmic scale
    """

    def __init__(self, n: int, k:int, nsolutions: int, **kwargs): 
        super().__init__(**kwargs)

    def to_bitcomplexity_time(self, basic_operations: float):
        """
        Returns the bit-complexity corresponding to basic_operations field additions

        INPUT:

        - ``basic_operations`` -- Number of field additions (logarithmic)

        """
        pass

    def to_bitcomplexity_memory(self, basic_operations: float):
        """
        Returns the memory bit-complexity associated to a given number of elements to store

        INPUT:

        - ``elements_to_store`` -- number of memory operations (logarithmic)

        """
        pass

    def expected_number_solutions(self):
        """
        Returns the logarithm of the expected number of existing solutions to the problem

        """
        pass

    def __repr__(self):
        """
        """
        pass

    def get_parameters(self):
        """
        """
        pass
