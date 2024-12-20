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
from .mr_constants import *
from cryptographic_estimators.helper import is_prime_power, ngates
from math import log2, ceil


class MRProblem(BaseProblem):
    def __init__(self, q: int, m: int, n: int, k: int, r: int, **kwargs):
        """Construct an instance of MRProblem.

        Contains the parameters to optimize over.

        Args:
            q (int): Order of the finite field
            m (int): Number of rows of the input matrices
            n (int): Number of columns of the input matrices
            k (int): Length of the solution vector
            r (int): Target rank
            theta (float, optional): Exponent of the conversion factor. Defaults to 2.
            nsolutions (int, optional): Number of solutions in logarithmic scale. Defaults to max(expected_number_solutions, 0).
            memory_bound (float, optional): Maximum allowed memory to use for solving the problem. Defaults to inf.

        Note:
            - If 0 <= theta <= 2, every multiplication in GF(q) is counted as log2(q) ^ theta binary operation.
            - If theta = None, every multiplication in GF(q) is counted as 2 * log2(q) ^ 2 + log2(q) binary operation.
        """
        super().__init__(**kwargs)
        self.parameters[MR_FIELD_SIZE] = q
        self.parameters[MR_NUMBER_OF_ROWS] = m
        self.parameters[MR_NUMBER_OF_COLUMNS] = n
        self.parameters[MR_LENGTH_SOLUTION_VECTOR] = k
        self.parameters[MR_TARGET_RANK] = r
        self.nsolutions = kwargs.get("nsolutions", self.expected_number_solutions())
        self._theta = kwargs.get("theta", 2)

        if n < 1:
            raise ValueError("n must be >= 1")

        if m < 1:
            raise ValueError("m must be >= 1")

        if k < 1:
            raise ValueError("k must be >= 1")

        if not is_prime_power(q):
            raise ValueError("q must be a prime power")

        if self._theta is not None and not (0 <= self._theta <= 2):
            raise ValueError("theta must be either None or 0 <= theta <= 2")

    def to_bitcomplexity_time(self, basic_operations: float):
        """Return the bit-complexity corresponding to a certain amount of basic_operations.
    
        Args:
            basic_operations (float): Number of basic operations (logarithmic)

        Tests:
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> MRP = MRProblem(q=7, m=9, n=10, k=15, r=4)
            >>> MRP.to_bitcomplexity_time(200)
            202.97842293847626
        """
        q = self.parameters[MR_FIELD_SIZE]
        theta = self._theta
        return ngates(q, basic_operations, theta=theta)

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """Return the memory bit-complexity associated to a given number of elements to store.
    
        Args:
            elements_to_store (float): Number of memory operations (logarithmic)

        Tests:
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> MRP = MRProblem(q=7, m=9, n=10, k=15, r=4)
            >>> MRP.to_bitcomplexity_memory(100)
            101.58496250072116
        """
        q = self.parameters[MR_FIELD_SIZE]
        return log2(ceil(log2(q))) + elements_to_store

    @property
    def theta(self):
        """Returns the value of `theta`."""
        return self._theta

    @theta.setter
    def theta(self, value: float):
        """Sets the value of `theta`"""
        self._theta = value

    def expected_number_solutions(self):
        """Return the logarithm of the expected number of existing solutions to the problem."""
        q, m, n, k, r = self.get_parameters()
        if k + 1 <= (m - r) * (n - r):
            return 0
        else:
            return (k + 1 - (m - r) * (n - r)) * log2(q)

    def order_of_the_field(self):
        """Return the order of the field.

        Tests:
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> MRP = MRProblem(q=7, m=9, n=10, k=15, r=4)
            >>> MRP.order_of_the_field()
            7
        """
        return self.parameters[MR_FIELD_SIZE]

    def nrows(self):
        """Return the number of rows of the input matrix.

        Tests:
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> MRP = MRProblem(q=7, m=9, n=10, k=15, r=4)
            >>> MRP.nrows()
            9
        """
        return self.parameters[MR_NUMBER_OF_ROWS]

    def ncolumns(self):
        """Return the number of columns of the input matrix.

        Tests:
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> MRP = MRProblem(q=7, m=9, n=10, k=15, r=4)
            >>> MRP.ncolumns()
            10
        """
        return self.parameters[MR_NUMBER_OF_COLUMNS]

    def length_solution_vector(self):
        """Return the length of the solution vector.

        Tests:
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> MRP = MRProblem(q=7, m=9, n=10, k=15, r=4)
            >>> MRP.length_solution_vector()
            15
        """
        return self.parameters[MR_LENGTH_SOLUTION_VECTOR]

    def nmatrices(self):
        """Return the number of input matrices.

        Tests:
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> MRP = MRProblem(q=7, m=9, n=10, k=15, r=4)
            >>> MRP.nmatrices()
            16
        """
        return self.length_solution_vector() + 1

    def target_rank(self):
        """Return the target rank.

        Tests:
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> MRP = MRProblem(q=7, m=9, n=10, k=15, r=4)
            >>> MRP.target_rank()
            4
        """
        return self.parameters[MR_TARGET_RANK]

    def __repr__(self):
        """Returns a string representation of the object.

        Tests:
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> MRP = MRProblem(q=7, m=9, n=10, k=15, r=4)
            >>> MRP
            MinRank problem with (q, m, n, k, r) = (7,9,10,15,4)
        """
        q, m, n, k, r = self.get_parameters()
        rep = "MinRank problem with (q, m, n, k, r) = " \
              + "(" + str(q) + "," + str(m) + "," + str(n) + "," + \
              str(k) + "," + str(r) + ")"
        return rep
