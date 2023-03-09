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
 


 


from ...LEEstimator.le_algorithm import LEAlgorithm
from ...LEEstimator.le_problem import LEProblem


class Sample(LEAlgorithm):

    def __init__(self, problem: LEProblem, **kwargs):
        super().__init__(problem, **kwargs)

    def _compute_time_complexity(self, parameters):
        pass

    def _compute_memory_complexity(self, parameters):
        pass
