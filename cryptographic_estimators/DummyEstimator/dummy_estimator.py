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


from .dummy_algorithm import DummyAlgorithm
from .dummy_problem import DummyProblem
from ..base_estimator import BaseEstimator
from math import inf


class DummyEstimator(BaseEstimator):
    """
    Construct an instance of DummyEstimator

    INPUT:

    - ``problem_parameter1`` -- First parameter of the problem
    - ``problem_parameter2`` -- Second parameter of the problem
    - ``memory_bound`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)  
    - ``nsolutions`` -- number of solutions of the problem in logarithmic scale

    """

    def __init__(self, problem_parameter1: float, problem_parameter2, memory_bound=inf, **kwargs):
        super(DummyEstimator, self).__init__(DummyAlgorithm, DummyProblem(problem_parameter1=problem_parameter1,
                                                                          problem_parameter2=problem_parameter2,
                                                                          memory_bound=memory_bound, **kwargs), **kwargs)

    def table(self, show_quantum_complexity=0, show_tilde_o_time=0,
              show_all_parameters=0, precision=1, truncate=0):
        """
        Print table describing the complexity of each algorithm and its optimal parameters

        INPUT:

        - ``show_quantum_complexity`` -- show quantum time complexity (default: false)
        - ``show_tilde_o_time`` -- show Ō time complexity (default: false)
        - ``show_all_parameters`` -- show all optimization parameters (default: false)
        - ``precision`` -- number of decimal digits output (default: 1)
        - ``truncate`` -- truncate rather than round the output (default: false)
        """
        super(DummyEstimator, self).table(show_quantum_complexity=show_quantum_complexity,
                                          show_tilde_o_time=show_tilde_o_time,
                                          show_all_parameters=show_all_parameters,
                                          precision=precision, truncate=truncate)
