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


from ..$$lower_case_prefix$$_algorithm import $$UPPER_CASE_PREFIX$$Algorithm
from ..$$lower_case_prefix$$_problem import $$UPPER_CASE_PREFIX$$Problem


class $$UPPER_CASE_PREFIX$$Algorithm1($$UPPER_CASE_PREFIX$$Algorithm):
    """
    Construct an instance of $$UPPER_CASE_PREFIX$$Algorithm1 estimator

    Add reference to correponding paper here.

    INPUT:

    - ``problem`` -- an instance of the $$UPPER_CASE_PREFIX$$Problem class
    """

    def __init__(self, problem: $$UPPER_CASE_PREFIX$$Problem, **kwargs):
        super().__init__(problem, **kwargs)

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        pass

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        pass
