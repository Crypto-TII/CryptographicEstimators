from ..base_problem import BaseProblem
from .pk_constants import *
from math import log2, factorial


class PKProblem(BaseProblem):
    """
    Construct an instance of the Permuted Kernel Problem

    INPUT:

    - ``n`` -- columns of the matrix
    - ``m`` -- rows of the matrix
    - ``q`` -- size of the field
    - ``ell`` -- rows of the matrix whose permutation should lie in the kernel
    - ``nsolutions`` -- number of (expected) solutions of the problem in logarithmic scale
    """

    def __init__(self, n: int, m: int, q: int, ell=1, **kwargs):
        super().__init__(**kwargs)

        self.parameters[PK_COLUMNS] = n
        self.parameters[PK_ROWS] = m
        self.parameters[PK_FIELD_SIZE] = q
        self.parameters[PK_DIMENSION] = ell

        if q ** ell < n:
            raise ValueError("q^ell should be at least n, otherwise possible number of permutations is not maximal")

        self.nsolutions = kwargs.get("nsolutions", max(self.expected_number_solutions(), 0))

    def to_bitcomplexity_time(self, basic_operations: float):
        """
        Returns the bit-complexity corresponding to basic_operations field additions

        INPUT:

        - ``basic_operations`` -- Number of Fq additions (logarithmic)

        """
        return basic_operations + log2(self.parameters[PK_FIELD_SIZE])

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """
        Returns the memory bit-complexity associated to a given number of elements to store

        INPUT:

        - ``elements_to_store`` -- number of Fq elements the algorithm needs to store (logarithmic)

        """
        # TODO: how to count it? which measure, again Fq elementS? then we need to scale lists by an according factor
        return elements_to_store + log2(self.parameters[PK_FIELD_SIZE])

    def expected_number_solutions(self):
        """
        Returns the logarithm of the expected number of existing solutions to the problem

        """
        n, m, q, ell = self.get_parameters()
        return log2(factorial(n)) - log2(q) * m

    def __repr__(self):
        """
        """
        n, m, q, ell = self.get_parameters()
        rep = "permuted kernel problem with (n,m,q,ell) = " \
              + "(" + str(n) + "," + str(m) + "," + str(q) + "," + str(ell) + ")"

        return rep

    def get_parameters(self):
        """
        """
        return self.parameters.values()
