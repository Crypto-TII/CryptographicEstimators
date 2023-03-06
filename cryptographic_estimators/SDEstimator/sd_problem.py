from ..base_problem import BaseProblem
from math import comb, inf, log2
from sage.all import GF
from .sd_constants import *


class SDProblem(BaseProblem):
    """
    Construct an instance of Syndrome Decoding Problem

    INPUT:

    - ``n`` -- code length
    - ``k`` -- code dimension
    - ``w`` -- error weight
    - ``q`` -- size of the basefield of the code
    - ``nsolutions`` -- number of (expected) solutions of the problem in logarithmic scale
    """

    def __init__(self, n, k, w, q=2, **kwargs):
        super().__init__(**kwargs)
        if k > n:
            raise ValueError("k must be smaller or equal to n")
        if w > n-k:
            raise ValueError("w must be smaller or equal to n-k")

        self.parameters[SD_CODE_LENGTH] = n
        self.parameters[SD_CODE_DIMENSION] = k
        self.parameters[SD_ERROR_WEIGHT] = w
        self.baseField = GF(q)

        self.nsolutions = kwargs.get("nsolutions", max(self.expected_number_solutions(), 0))

    def to_bitcomplexity_time(self, basic_operations):
        """
        Returns the bit-complexity corresponding to basic_operations field additions

        INPUT:

        - ``basic_operations`` -- Number of field additions (logarithmic)

        """
        q = self.baseField.characteristic()
        n = self.parameters[SD_CODE_LENGTH]
        return log2(log2(q)) + log2(n) + basic_operations

    def to_bitcomplexity_memory(self, basic_operations):
        return self.to_bitcomplexity_time(basic_operations)

    def expected_number_solutions(self):
        """
        Returns the logarithm of the expected number of existing solutions to the problem

        """
        # todo fix for fq
        n, k, w, _ = self.get_parameters()
        return log2(comb(n, w)) - (n - k)

    def __repr__(self):
        n, k, w, _ = self.get_parameters()
        rep = "syndrome decoding problem with (n,k,w) = " \
              + "(" + str(n) + "," + str(k) + "," + str(w) + ") over " + str(self.baseField)

        return rep

    def get_parameters(self):
        n = self.parameters[SD_CODE_LENGTH]
        k = self.parameters[SD_CODE_DIMENSION]
        w = self.parameters[SD_ERROR_WEIGHT]
        q = self.baseField.characteristic()
        return n, k, w, q
