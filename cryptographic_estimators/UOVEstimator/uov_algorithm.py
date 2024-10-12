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


from cryptographic_estimators.base_algorithm import BaseAlgorithm
from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem


class UOVAlgorithm(BaseAlgorithm):
    def __init__(self, problem: UOVProblem, **kwargs):
        """Base class for UOV algorithms complexity estimator.

        Args:
            problem (UOVProblem): UOVProblem object including all necessary parameters
            **kwargs: Additional keyword arguments
                w (int): Linear algebra constant (default: 2)
                h (int): External hybridization parameter (default: 0)
                memory_access (int): Specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
                complexity_type (int): Complexity type to consider (0: estimate, 1: tilde O complexity, default: 0)
                bit_complexities (int): Determines if complexity is given in bit operations or basic operations (default 1: in bit)
        """
        super(UOVAlgorithm, self).__init__(problem, **kwargs)

        self._h = kwargs.get("h", 0)
        self._w = kwargs.get("w", 2.81)
        self._name = "BaseUOVAlgorithm"

        if self._w is not None and not 2 <= self._w <= 3:
            raise ValueError("w must be in the range 2 <= w <= 3")

        if self._h < 0:
            raise ValueError("h must be >= 0")

    def linear_algebra_constant(self):
        """Return the linear algebra constant.

        Tests:
            >>> from cryptographic_estimators.UOVEstimator.uov_algorithm import UOVAlgorithm
            >>> from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            >>> UOVAlgorithm(UOVProblem(n=10, m=5, q=4), w=2).linear_algebra_constant()
            2
        """
        return self._w

    def __repr__(self):
        n, m, q = self.problem.get_parameters()
        return f"{self._name} estimator for the UOV signature scheme with parameters (q, n, m) = ({q}, {n}, {m})"
