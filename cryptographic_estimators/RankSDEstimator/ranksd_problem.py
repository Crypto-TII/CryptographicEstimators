# ****************************************************************************
# Copyright 2023 Technology Innovation Institute
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ****************************************************************************


from ..base_problem import BaseProblem
from .ranksd_constants import *
from math import log2, ceil
from cryptographic_estimators.helper import is_prime_power, ngates


class RankSDProblem(BaseProblem):
    """Construct an instance of RankSDProblem.

       Args:
            q (int): Base field order.
            m (int): Extension degree.
            n (int): Code length.
            k (int): Code dimension.
            r (int): Target rank.
            theta (float, optional): Exponent of the conversion factor. Defaults to 2.
            memory_bound (float, optional): Maximum allowed memory to use for solving the problem. Defaults to inf.

       Note:
            - If 0 <= theta <= 2, every multiplication in GF(q) is counted as log2(q) ^ theta binary operation.
            - If theta = None, every multiplication in GF(q) is counted as 2 * log2(q) ^ 2 + log2(q) binary operation
    """

    def __init__(self, q: int, m: int, n: int, k: int, r: int, **kwargs):  # Fill with parameters
        super().__init__(**kwargs)
        self.parameters[RANKSD_BASE_FIELD_ORDER] = q
        self.parameters[RANKSD_DEGREE_EXTENSION] = m
        self.parameters[RANKSD_CODE_LENGTH] = n
        self.parameters[RANKSD_CODE_DIMENSION] = k
        self.parameters[RANKSD_TARGET_RANK] = r
        self._theta = kwargs.get("theta", 2)

        if q is not None and not is_prime_power(q):
            raise ValueError("q must be a prime power")

        if n < 1:
            raise ValueError("n must be >= 1")

        if m < 1:
            raise ValueError("m must be >= 1")

        if k < 1:
            raise ValueError("k must be >= 1")

        if r < 1:
            raise ValueError("r must be >= 1")

        if self._theta is not None and not (0 <= self._theta <= 2):
            raise ValueError("theta must be either None or 0<=theta <= 2")

    def to_bitcomplexity_time(self, basic_operations: float):
        """Return the bit-complexity corresponding to a certain amount of basic_operations.

        Args:
            basic_operations (float): Number of basic operations (logarithmic)

        Tests:
            >>> from cryptographic_estimators.RankSDEstimator.ranksd_estimator import RankSDProblem
            >>> RSDP = RankSDProblem(q=2, m=127, n=118, k=48, r=7)
            >>> RSDP.to_bitcomplexity_time(200)
            200.0

        """
        q = self.parameters[RANKSD_BASE_FIELD_ORDER]
        theta = self._theta
        return ngates(q, basic_operations, theta=theta)

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """Return the memory bit-complexity associated to a given number of elements to store

         Args:
             elements_to_store: number of memory operations (logarithmic)

        """
        q = self.parameters[RANKSD_BASE_FIELD_ORDER]

        return log2(ceil(log2(q))) + elements_to_store

    def expected_number_solutions(self):
        """Return the logarithm of the expected number of existing solutions to the problem"""
        pass

    def get_parameters(self):
        """Return the optimizations parameters"""
        return list(self.parameters.values())

    @property
    def theta(self):
        """Returns the value of `theta`."""
        return self._theta

    @theta.setter
    def theta(self, value: float):
        """Sets the value of `theta`"""
        self._theta = value

    def base_field_order(self):
        """Return the order of the base finite field.

        Tests:
            >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem  import RankSDProblem
            >>> RSDP = RankSDProblem(q=2, m=127, n=118, k=48, r=7)
            >>> RSDP.base_field_order()
            2
        """
        return self.parameters[RANKSD_BASE_FIELD_ORDER]

    def degree_extension(self):
        """Return the degree of the field extension.

         Tests:
            >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem  import RankSDProblem
            >>> RSDP = RankSDProblem(q=2, m=127, n=118, k=48, r=7)
            >>> RSDP.degree_extension()
            127
        """
        return self.parameters[RANKSD_DEGREE_EXTENSION]

    def code_length(self):
        """Return the dimension of the vector space.

        Tests:
            >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem  import RankSDProblem
            >>> RSDP = RankSDProblem(q=2, m=127, n=118, k=48, r=7)
            >>> RSDP.code_length()
            118
        """
        return self.parameters[RANKSD_CODE_LENGTH]

    def code_dimension(self):
        """Return the dimension of the code.

        Tests:
            >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem  import RankSDProblem
            >>> RSDP = RankSDProblem(q=2, m=127, n=118, k=48, r=7)
            >>> RSDP.code_dimension()
            48
        """
        return self.parameters[RANKSD_CODE_DIMENSION]

    def target_rank(self):
        """Return the target rank.

       Tests:
            >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem  import RankSDProblem
            >>> RSDP = RankSDProblem(q=2, m=127, n=118, k=48, r=7)
            >>> RSDP.target_rank()
            7
        """
        return self.parameters[RANKSD_TARGET_RANK]

    def __repr__(self):
        """Returns a string representation of the object.

        Tests:
            >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem  import RankSDProblem
            >>> RSDP = RankSDProblem(q=2, m=127, n=118, k=48, r=7)
            >>> RSDP
            Rank Syndrome Decoding problem with (q, m, n, k, r) = (2,127,118,48,7)
        """
        q, m, n, k, r = self.get_parameters()
        rep = "Rank Syndrome Decoding problem with (q, m, n, k, r) = " \
              + "(" + str(q) + "," + str(m) + "," + str(n) + "," + \
              str(k) + "," + str(r) + ")"
        return rep
