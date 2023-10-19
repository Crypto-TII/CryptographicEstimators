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


class UOVAlgorithm(BaseAlgorithm):
    def __init__(self, problem: UOVProblem, **kwargs):
        """
        Base class for UOV algorithms complexity estimator

        INPUT:

        - ``problem`` -- UOVProblem object including all necessary parameters

        """
        super(UOVAlgorithm, self).__init__(problem, **kwargs)
        self._name = "BaseUOVAlgorithm"

    def __repr__(self):
        """
        """
        n, m, q = self.problem.get_parameters()
        return f"{self._name} estimator for the UOV signature scheme with with {n} variables and {m} polynomials"
