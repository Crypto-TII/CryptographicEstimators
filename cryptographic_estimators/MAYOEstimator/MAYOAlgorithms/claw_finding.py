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
from cryptographic_estimators.base_constants import BASE_FORGERY_ATTACK


class ClawFinding(MAYOAlgorithm):
    """
    Construct an instance of ClawFinding estimator

    Claw finding attack is a general attack which works against any signature which 
    follows the hash-and-sign paradigm. 

    INPUT:

    - ``problem`` -- MAYOProblem object including all necessary parameters
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
        self._attack_type = BASE_FORGERY_ATTACK

    @optimal_parameter
    def X(self):
        """
        Return logarithm of the optimal `X`, i.e. no. of inputs (preimages)
        Optimal value for `X` is obtained from optimizing the bit-cost expression of the attack 
        reported in MAYO specification 36 * m * X + Y * 2 ** 17 using X * Y = q ** m 

        EXAMPLES::

            sage: from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            sage: from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.claw_finding import ClawFinding
            sage: E = ClawFinding(MAYOProblem(n=80, m=60, o=18, k=12, q=16))
            sage: E.X()
            122.962

        """
        _, m, _, _, q = self.problem.get_parameters()
        X = (1 / 2) * (17 - log2(36 * m) + m * log2(q))
        X_rounded = round(X, 3)
        return X_rounded

    @optimal_parameter
    def Y(self):
        """
        Return logarithm of the optimal `Y`, i.e. logarithm of no. of hashes to compute
        Optimal value for `Y` is obtained from X * Y = q ** m using the optimal value of `X`

        EXAMPLES::

            sage: from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            sage: from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.claw_finding import ClawFinding
            sage: E = ClawFinding(MAYOProblem(n=80, m=60, o=18, k=12, q=16))
            sage: E.Y()
            117.038

        """
        X =  self.X()
        _, m, _, _, q = self.problem.get_parameters()
        Y = max(m * log2(q) - X, 0)
        Y_rounded = round(Y, 3)
        return Y_rounded

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            sage: from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.claw_finding import ClawFinding
            sage: E = ClawFinding(MAYOProblem(n=80, m=60, o=18, k=12, q=16))
            sage: E.time_complexity()
            134.0384078561605

        """
        m = self.problem.npolynomials()
        X = self.X()
        Y = self.Y()
        cost_one_hash = self.problem.cost_one_hash
        time_in_bits = log2(36 * m * 2 ** X + 2 ** Y * 2 ** cost_one_hash)
        cost_one_field_mult = self.problem.to_bitcomplexity_time(1)
        time = time_in_bits - cost_one_field_mult
        return time

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            sage: from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.claw_finding import ClawFinding
            sage: E = ClawFinding(MAYOProblem(n=80, m=60, o=18, k=12, q=16))
            sage: E.memory_complexity()
            127.038

        """
        X = self.X()
        Y = self.Y()
        n, m, _, k, q = self.problem.get_parameters()
        mem_evals = log2(m) + X
        mem_hashes = log2(256) + Y - log2(q)
        return min(mem_evals, mem_hashes)
    