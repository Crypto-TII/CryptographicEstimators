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
from ..MQEstimator.mq_helper import ngates


class RANKSDProblem(BaseProblem):
    """
    Construct an instance of RANKSDProblem. Contains the parameters to optimize
    over.

    INPUT: 
        - Fill with parameters

    """

    def __init__(self, q: int, m: int, n: int, k: int, r: int, **kwargs):  # Fill with parameters
        super().__init__(**kwargs)
        self.parameters[RANKSD_q] = q
        self.parameters[RANKSD_m] = m
        self.parameters[RANKSD_n] = n
        self.parameters[RANKSD_k] = k
        self.parameters[RANKSD_r] = r
        self._theta = kwargs.get("theta", 2)

    def to_bitcomplexity_time(self, basic_operations: float):
        """
        Return the bit-complexity corresponding to a certain amount of basic_operations

        INPUT:

        - ``basic_operations`` -- Number of basic operations (logarithmic)

        """
        q = self.parameters[RANKSD_q]
        theta = self._theta
        return ngates(q, basic_operations, theta=theta)

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """
        Return the memory bit-complexity associated to a given number of elements to store

        INPUT:

        - ``elements_to_store`` -- number of memory operations (logarithmic)

        """
        q = self.parameters[RANKSD_q]

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

    def __repr__(self):
        return "RANKSDProblem"
