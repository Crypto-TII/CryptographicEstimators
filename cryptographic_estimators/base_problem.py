from math import inf


class BaseProblem(object):
    """
    Construct an instance of BaseProblem

    INPUT:

    - ``parameters`` -- dict of parameters of the problem.
    - ``base_field`` -- characteristic of the base field
    - ``nsolutions`` -- number of solutions of the problem
    - ``memory_bound`` -- maximum allowed memory to use for solving the problem

    """
    def __init__(self, **kwargs):
        self.parameters = {}
        self.base_field = None
        self.nsolutions = None
        self.memory_bound = inf if "memory_bound" not in kwargs else kwargs["memory_bound"]

    def expected_number_solutions(self):
        """
        Returns the expected number of existing solutions to the problem

        """
        return NotImplementedError

    def to_bitcomplexity_time(self, basic_operations):
        """
        Returns the bit-complexity associated to a given number of basic-operations

        INPUT:

        -``basic_operations`` -- number of basic operations (logarithmic)

        """
        return basic_operations

    def to_bitcomplexity_memory(self, elements_to_store):
        """
        Returns the bit-complexity associated to a given number of basic-operations

        INPUT:

        -``basic_operations`` -- number of basic operations (logarithmic)

        """
        return elements_to_store
