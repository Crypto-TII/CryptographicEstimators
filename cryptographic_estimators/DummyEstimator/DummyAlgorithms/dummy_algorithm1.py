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


from ..dummy_algorithm import DummyAlgorithm
from ..dummy_problem import DummyProblem
from ...base_algorithm import optimal_parameter
from math import log2


class DummyAlgorithm1(DummyAlgorithm):
    def __init__(self, problem: DummyProblem, **kwargs):
        """Construct an instance of DummyAlgorithm1 estimator.

        Add reference to corresponding paper here.

        Args:
            problem (DummyProblem): DummyProblem object including all necessary parameters
            **kwargs: Additional keyword arguments
                memory_access: Specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
                complexity_type: Complexity type to consider (0: estimate, 1: tilde O complexity, default: 0)

        Examples:
            >>> from cryptographic_estimators.DummyEstimator.DummyAlgorithms.dummy_algorithm1 import DummyAlgorithm1
            >>> from cryptographic_estimators.DummyEstimator.dummy_problem import DummyProblem
            >>> E = DummyAlgorithm1(DummyProblem(100, 50))
            >>> E
            dummy_algorithm1 estimator for the dummy problem with parameters 100 and 50 
        """
        super().__init__(problem, **kwargs)

        self._name = "dummy_algorithm1"
        problem_par1, problem_par2 = self.problem.get_parameters()
        self.set_parameter_ranges('optimization_parameter_1', 1, problem_par1)
        self.set_parameter_ranges(
            'optimization_parameter_2', 1, max(1, problem_par1 - problem_par2))
        self.set_parameter_ranges('optimization_parameter_3', 10, 20)

    @optimal_parameter
    def optimization_parameter_3(self):
        """Return the optimal parameter optimization_parameter_3.

        Examples:
            >>> from cryptographic_estimators.DummyEstimator.DummyAlgorithms.dummy_algorithm1 import DummyAlgorithm1
            >>> from cryptographic_estimators.DummyEstimator.dummy_problem import DummyProblem
            >>> E = DummyAlgorithm1(DummyProblem(100, 50))
            >>> E.optimization_parameter_3()
            10
        """

        # first define parameters that can be optimized independently from each other
        problem_par1, problem_par2 = self.problem.get_parameters()
        if problem_par1 - problem_par2 > 20:
            return 10
        else:
            return 20

    @optimal_parameter
    def optimization_parameter_1(self):
        """Return the optimal parameter optimization_parameter_1.

        Examples:
            >>> from cryptographic_estimators.DummyEstimator.DummyAlgorithms.dummy_algorithm1 import DummyAlgorithm1
            >>> from cryptographic_estimators.DummyEstimator.dummy_problem import DummyProblem
            >>> E = DummyAlgorithm1(DummyProblem(100, 50))
            >>> E.optimization_parameter_1()
            25
        """

        # then define all dependent parameters which need to be optimized together using the _get_optimal_parameter
        # method
        return self._get_optimal_parameter('optimization_parameter_1')

    @optimal_parameter
    def optimization_parameter_2(self):
        """Return the optimal parameter optimization_parameter_2.

        Examples:
            >>> from cryptographic_estimators.DummyEstimator.DummyAlgorithms.dummy_algorithm1 import DummyAlgorithm1
            >>> from cryptographic_estimators.DummyEstimator.dummy_problem import DummyProblem
            >>> E = DummyAlgorithm1(DummyProblem(100, 50))
            >>> E.optimization_parameter_2()
            50
        """

        return self._get_optimal_parameter('optimization_parameter_2')

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        p1 = parameters["optimization_parameter_1"]
        p2 = parameters["optimization_parameter_2"]
        p3 = parameters["optimization_parameter_3"]
        prob_par1, prob_par2 = self.problem.get_parameters()

        time = max((16 * (prob_par1 - p1 - p2) ** 2 + (prob_par2 + 2 * p3) ** 3) * 2 ** max(0, prob_par1 - p1 - p2 - p3),
                   2 ** p1 * p2 * p3)

        return log2(time)

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        p1 = parameters["optimization_parameter_1"]
        p2 = parameters["optimization_parameter_2"]
        p3 = parameters["optimization_parameter_3"]
        memory = 2 ** p1 * p2 * p3
        return log2(memory)
