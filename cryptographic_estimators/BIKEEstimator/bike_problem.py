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
from .bike_constants import BIKE_DIMENSION, BIKE_SK_WEIGHT, BIKE_MSG_WEIGHT
from ..base_problem import BaseProblem
from math import log2


class BIKEProblem(BaseProblem):
    """
    Construct an instance of BIKEProblem. Contains the parameters to optimize
    over.

    INPUT:

    - ``r`` -- code dimension
    - ``w`` -- weight of secret key polynomial
    - ``t`` -- weight of polynomials encoding messages
    - ``memory_bound`` -- maximum allowed memory to use for solving the problem

    """

    def __init__(self, r: int, w: int, t: int, **kwargs):  # Fill with parameters
        super().__init__(**kwargs)
        self.parameters = {BIKE_DIMENSION: r, BIKE_SK_WEIGHT: w, BIKE_MSG_WEIGHT: t}

    def to_bitcomplexity_time(self, basic_operations: float):
        """
        Return the bit-complexity corresponding to a certain amount of basic_operations

        INPUT:

        - ``basic_operations`` -- Number of basic operations (logarithmic)

        """
        code_length = 2 * self.parameters[BIKE_DIMENSION]
        return basic_operations + log2(code_length)

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """
        Return the memory bit-complexity associated to a given number of elements to store

        INPUT:

        - ``elements_to_store`` -- number of memory operations (logarithmic)

        """
        code_length = 2 * self.parameters[BIKE_DIMENSION]
        return elements_to_store + log2(code_length)

    def __repr__(self):
        """
        """
        r, w, t = self.get_parameters()
        rep = "BIKE instance with (r,w,t) = " + "(" + str(r) + "," + str(w) + "," + str(t) + ")"
        return rep
