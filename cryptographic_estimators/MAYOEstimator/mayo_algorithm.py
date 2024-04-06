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


from ..base_algorithm import BaseAlgorithm
from .mayo_problem import MAYOProblem


class MAYOAlgorithm(BaseAlgorithm):
    def __init__(self, problem: MAYOProblem, **kwargs):
        """
        Base class for MAYO algorithms complexity estimator

        INPUT:

        - ``problem`` -- MAYOProblem object including all necessary parameters
        - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
        - ``complexity_type`` -- complexity type to consider (0: estimate, 1: tilde O complexity, default: 0)

        """
        super(MAYOAlgorithm, self).__init__(problem, **kwargs)

        self._h = kwargs.get("h", 0)
        self._w = kwargs.get("w", 2.81)
        self._name = "BaseMAYOAlgorithm"

        if self._w is not None and not 2 <= self._w <= 3:
            raise ValueError("w must be in the range 2 <= w <= 3")

        if self._h < 0:
            raise ValueError("h must be >= 0")
        
    def linear_algebra_constant(self):
        """
        Return the linear algebra constant

        TESTS::


        
        """
        return self._w

    def __repr__(self):
        """
        NOTE: self._name must be instanciated via the child class
        """
        n, m, o, k, q = self.get_parameters()
        return f"{self.name} estimator for the MAYO signature scheme with parameters (n, m, o, k, q) = ({n}, {m}, {o}, {k}, {q})"
