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
from .rsd_problem import RSDProblem


class RSDAlgorithm(BaseAlgorithm):
    def __init__(self, problem: RSDProblem, **kwargs):
        """
        Base class for RSD algorithms complexity estimator

        INPUT:

        - ``problem`` -- RSDProblem object including all necessary parameters

        """
        super(RSDAlgorithm, self).__init__(problem, **kwargs)
        self._name = "RSDAlgorithm"
        self.w = kwargs.get("w", 3)
