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


from cryptographic_estimators.MQEstimator.mq_algorithm import MQAlgorithm
from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
from cryptographic_estimators.helper import is_power_of_two
from math import log2


class MHT(MQAlgorithm):
    def __init__(self, problem: MQProblem, **kwargs):
        """Construct an instance of MHT estimator.

        The MHT is an algorithm to solve the MQ problem when  $m  (m + 3) / 2 \\leq n$ [MHT13]_.

        Args:
            problem (MQProblem): MQProblem object including all necessary parameters.
            w (float, optional): Linear algebra constant (2 <= w <= 3). Defaults to 2.81.
            memory_access (int, optional): Specifies the memory access cost model. Defaults to 0 (choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage).
            complexity_type (int, optional): Complexity type to consider (0: estimate, 1: tilde O comp).

        Examples:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.mht import MHT
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = MHT(MQProblem(n=183, m=12, q=4), w=2.8)
            >>> E
            MHT estimator for the MQ problem with 183 variables and 12 polynomials

        Tests:
            >>> E.problem.nvariables() == E.nvariables_reduced()
            True
        """

        n, m, q = problem.get_problem_parameters()
        if not isinstance(q,int):
            raise TypeError("q must be an integer")

        if m * (m + 3) / 2 > n:
            raise ValueError(
                "The parameter n should be grater than or equal to m * (m + 3) / 2"
            )

        super().__init__(problem, **kwargs)
        self._name = "MHT"
        self._n_reduced = n
        self._m_reduced = m

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.

        Tests:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.mht import MHT
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = MHT(MQProblem(n=183, m=12, q=4), w=2.8)
            >>> E.time_complexity()
            26.628922047916475
        """
        n, m, _ = self.problem.get_problem_parameters()
        w = self.linear_algebra_constant()
        if is_power_of_two(self.problem.order_of_the_field()):
            time = 0
        else:
            time = m
        time += log2(m * n**w)
        return time

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.

        Tests:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.mht import MHT
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = MHT(MQProblem(n=183, m=12, q=4), w=2.8)
            >>> E.memory_complexity()
            19.61636217728924
        """
        n, m, q = self.problem.get_problem_parameters()
        return log2(m * n**2)

    def _compute_tilde_o_time_complexity(self, parameters: dict):
        """Return the Ō time complexity of the algorithm for a given set of parameters."""
        _, m, _ = self.get_reduced_parameters()
        if is_power_of_two(self.problem.order_of_the_field()):
            time = 0
        else:
            time = m
        return time

    def _compute_tilde_o_memory_complexity(self, parameters: dict):
        """Return the Ō memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): A dictionary including the parameters.
        """
        return 0
