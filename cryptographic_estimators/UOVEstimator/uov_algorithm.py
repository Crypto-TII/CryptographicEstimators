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
from .uov_problem import UOVProblem
from sage.arith.misc import is_prime_power


class UOVAlgorithm(BaseAlgorithm):
    def __init__(self, problem: UOVProblem, **kwargs):
        """
        Base class for UOV algorithms complexity estimator

        INPUT:

        - ``problem`` -- UOVProblem object including all necessary parameters
        - ``w`` -- linear algebra constant (default: 2)
        - ``h`` -- external hybridization parameter (default: 0)
        - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
        - ``complexity_type`` -- complexity type to consider (0: estimate, 1: tilde O complexity, default: 0)

        """
        super(UOVAlgorithm, self).__init__(problem, **kwargs)

        h = kwargs.get("h", 0)
        w = kwargs.get("w", 2.81)
        n = self.problem.nvariables()
        m = self.problem.npolynomials()
        q = self.problem.order_of_the_field()
        self._name = "BaseUOVAlgorithm"

        if n < 1:
            raise ValueError("n must be >= 1")

        if m < 1:
            raise ValueError("m must be >= 1")

        if q is not None and not is_prime_power(q):
            raise ValueError("q must be a prime power")

        if w is not None and not 2 <= w <= 3:
            raise ValueError("w must be in the range 2 <= w <= 3")

        if h < 0:
            raise ValueError("h must be >= 0")

        self._n = n
        self._m = m
        self._q = q
        self._w = w
        self._h = h

    def __repr__(self):
        """
        """
        n, m, q = self.problem.get_parameters()
        return f"{self._name} estimator for the UOV signature scheme with parameters (q, n, m) = ({q}, {n}, {m})"
