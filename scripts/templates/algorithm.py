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
from .$$lower_case_prefix$$_problem import $$UPPER_CASE_PREFIX$$Problem


class $$UPPER_CASE_PREFIX$$Algorithm(BaseAlgorithm):
    def __init__(self, problem: $$UPPER_CASE_PREFIX$$Problem, **kwargs):
        """
        Base class for $$UPPER_CASE_PREFIX$$ algorithms complexity estimator

        INPUT:

        - ``problem`` -- $$UPPER_CASE_PREFIX$$Problem object including all necessary parameters

        """
        self._name = "sample_name"
        super($$UPPER_CASE_PREFIX$$Algorithm, self).__init__(problem, **kwargs)

    def __repr__(self):
        """
        NOTE: self._name must be instanciated via the child class
        """
        pass