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


from ..mayo_algorithm import MAYOAlgorithm
from ..mayo_problem import MAYOProblem
from ...MQEstimator.mq_estimator import MQEstimator
from ...MQEstimator.MQAlgorithms.lokshtanov import Lokshtanov
from ...base_constants import BASE_EXCLUDED_ALGORITHMS
from ...base_algorithm import optimal_parameter
from math import log2, e


class ClawFinding(MAYOAlgorithm):
    """
    Construct an instance of ClawFinding estimator

    -----

    INPUT:

    - ``problem`` -- DummyProblem object including all necessary parameters
    - ``w`` -- linear algebra constant (default: Obtained from MAYOAlgorithm)
    - ``h`` -- external hybridization parameter (default: 0)
    - ``nsolutions`` -- number of solutions in logarithmic scale (default: expected_number_solutions))
    - ``excluded_algorithms`` -- a list/tuple of MQ algorithms to be excluded (default: [Lokshtanov])
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
    - ``complexity_type`` -- complexity type to consider (0: estimate, default: 0)
    - ``bit_complexities`` -- determines if complexity is given in bit operations or basic operations (default 1: in bit)

    """

    def __init__(self, problem: MAYOProblem, **kwargs):
        super().__init__(problem, **kwargs)

        self._name = "ClawFinding"
        self._attack_type = "----"
        self._alpha = 1.25
        self._log2_of_alpha = log2(self._alpha)
        q = problem.order_of_the_field()
        self._gray_code_eval_cost = kwargs.get("gray_code_eval_cost", log2(q))

    @optimal_parameter
    def X(self):
        """
        Return the optimal `X`, i.e. no. of inputs (preimages)

        EXAMPLES::

            

        """
        n, m, _, k, q = self.problem.get_parameters()
        log2_of_alpha = self._log2_of_alpha
        r = self._gray_code_eval_cost
        X = 9.25  +  (1 / 2) * (-log2(3 * m * r)  + log2_of_alpha + m * log2(q))
        X_rounded = round(X, 3)
        return X_rounded
    
    @optimal_parameter
    def Y(self):
        """
        Return logarithm of the optimal `Y`, i.e. logarithm of no. of hashes to compute

        EXAMPLES::

            

        """
        X =  self.X()
        log2_of_alpha = self._log2_of_alpha
        n, m, _, k, q = self.problem.get_parameters()
        Y = max(log2(log2_of_alpha) + m * log2(q) - X, 0)
        Y_rounded = round(Y, 3)
        return Y_rounded

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            

        """
        n, m, _, k, q = self.problem.get_parameters()
        X = self.X()
        Y = self.Y()
        alpha = self._alpha
        r = self._gray_code_eval_cost
        cost_one_hash = self.problem.cost_one_hash
        time_temp = int(6 * (3 / 2) * m * r * 2 ** X) + int(2 ** cost_one_hash * 2 ** Y)
        time_in_bits = log2(time_temp)
        time_in_bits += log2(1/(1 - e ** (-alpha)))
        cost_one_field_mult = self.problem.to_bitcomplexity_time(1)
        time = time_in_bits - cost_one_field_mult
        return time

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            

        """
        X = self.X()
        Y = self.Y()
        n, m, _, k, q = self.problem.get_parameters()
        mem_evals = log2(log2(q)) + log2(m) + X
        mem_hashes = log2(256) + Y
        return min(mem_evals, mem_hashes)
    