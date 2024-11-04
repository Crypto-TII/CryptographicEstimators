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
from .rsd_constants import *
from math import log2, ceil
from cryptographic_estimators.helper import is_prime_power, ngates


class RSDProblem(BaseProblem):
    """
    Construct an instance of RSDProblem.
    Contains the parameters to optimize over.

        Args:
            q (int): Order of the base finite field
            m (int): Degree of the extension field
            n (int): Dimension of the vector space
            k (int): Dimension of the code
            r (int): Target rank
            theta (float, optional): Exponent of the conversion factor. Defaults to 2.
            nsolutions (int, optional): Number of solutions in logarithmic scale. Defaults to max(expected_number_solutions, 0).
            memory_bound (float, optional): Maximum allowed memory to use for solving the problem. Defaults to inf.

        Note:
            - If 0 <= theta <= 2, every multiplication in GF(q) is counted as log2(q) ^ theta binary operation.
            - If theta = None, every multiplication in GF(q) is counted as 2 * log2(q) ^ 2 + log2(q) binary operation
    """

    def __init__(self, q: int, m: int, n: int, k: int, r: int, **kwargs):  # Fill with parameters
        super().__init__(**kwargs)
        self.parameters[RSD_ORDER_BASE_FIELD] = q
        self.parameters[RSD_DEGREE_EXTENSION] = m
        self.parameters[RSD_DIMENSION_VECTOR_SPACE] = n
        self.parameters[RSD_DIMENSION_CODE] = k
        self.parameters[RSD_TARGET_RANK] = r
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
            >>> from cryptographic_estimators.RSDEstimator.rsd_estimator import RSDProblem
            >>> RSDP = RSDProblem(q=2, m=127, n=118, k=48, r=7)
            >>> RSDP.to_bitcomplexity_time(200)
                200
        """
        q = self.parameters[RSD_ORDER_BASE_FIELD]
        theta = self._theta
        return ngates(q, basic_operations, theta=theta)

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """
        Return the memory bit-complexity associated to a given number of elements to store

        INPUT:

        - ``elements_to_store`` -- number of memory operations (logarithmic)

        """
        q = self.parameters[RSD_ORDER_BASE_FIELD]

        return log2(ceil(log2(q))) + elements_to_store

    def expected_number_solutions(self):
        """
        Return the logarithm of the expected number of existing solutions to the problem

        """
        pass

    def get_parameters(self):
        """
        Return the optimizations parameters
        """
        return list(self.parameters.values())

    @property
    def theta(self):
        """Returns the value of `theta`."""
        return self._theta

    @theta.setter
    def theta(self, value: float):
        """Sets the value of `theta`"""
        self._theta = value

    def order_of_the_base_field(self):
        """Return the order of the based finite field.

        Tests:
            >>> from cryptographic_estimators.RSDEstimator.rsd_problem  import RSDProblem
            >>> RSDP = RSDProblem(q=2, m=127, n=118, k=48, r=7)
            >>> RSDP.order_of_the_base_field()
            2
        """
        return self.parameters[RSD_ORDER_BASE_FIELD]

    def degree_extension(self):
        """Return the degree of the field extension.

         Tests:
            >>> from cryptographic_estimators.RSDEstimator.rsd_problem  import RSDProblem
            >>> RSDP = RSDProblem(q=2, m=127, n=118, k=48, r=7)
            >>> RSDP.degree_extension()
            127
        """
        return self.parameters[RSD_DEGREE_EXTENSION]

    def dimension_vector_spapce(self):
        """Return the dimension of the vector space.

        Tests:
            >>> from cryptographic_estimators.RSDEstimator.rsd_problem  import RSDProblem
            >>> RSDP = RSDProblem(q=2, m=127, n=118, k=48, r=7)
            >>> RSDP.dimension_vector_spapce()
            118
        """
        return self.parameters[RSD_DIMENSION_VECTOR_SPACE]

    def dimension_code(self):
        """Return the dimension of the code.

        Tests:
            >>> from cryptographic_estimators.RSDEstimator.rsd_problem  import RSDProblem
            >>> RSDP = RSDProblem(q=2, m=127, n=118, k=48, r=7)
            >>> RSDP.dimension_code()
            48
        """
        return self.parameters[RSD_DIMENSION_CODE]

    def target_rank(self):
        """Return the target rank.

       Tests:
            >>> from cryptographic_estimators.RSDEstimator.rsd_problem  import RSDProblem
            >>> RSDP = RSDProblem(q=2, m=127, n=118, k=48, r=7)
            >>> RSDP.target_rank()
            7
        """
        return self.parameters[RSD_TARGET_RANK]

    def __repr__(self):
        """Returns a string representation of the object.

        Tests:
            >>> from cryptographic_estimators.RSDEstimator.rsd_problem  import RSDProblem
            >>> RSDP = RSDProblem(q=2, m=127, n=118, k=48, r=7)
            >>> RSDP
            Rank Syndrome Decoding problem with (q, m, n, k, r) = (2,127,118,48,7)
        """
        q, m, n, k, r = self.get_parameters()
        rep = "Rank Syndrome Decoding problem with (q, m, n, k, r) = " \
              + "(" + str(q) + "," + str(m) + "," + str(n) + "," + \
              str(k) + "," + str(r) + ")"
        return rep
