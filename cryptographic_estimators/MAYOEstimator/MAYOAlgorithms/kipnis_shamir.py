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
from math import log2


class KipnisShamir(MAYOAlgorithm):
    """
    Construct an instance of KipnisShamir estimator

    First attack on the Oil and Vinegar problem, proposed by Kipnis and Shamir.
    The attack attempts to find vectors in the oil space O, by exploiting the fact
    that these vectors are more likely to be eigenvectors of some publicy-known matrices.

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

        self._name = "KipnisShamir"
        self._attack_type = "key-recovery"

        n, _, o, _, _ = self.problem.get_parameters()
        if n <= 2 * o:
            raise ValueError('n should be greater than 2 * o')

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            sage: from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.kipnis_shamir import KipnisShamir
            sage: E = KipnisShamir(MAYOProblem(n=24, m=20, o=8, k=9, q=16))
            sage: E.time_complexity()
            50.007820003461546

        """
        n, _, o, _, q = self.problem.get_parameters()
        time = (n - 2 * o) * log2(q)
        return time + log2(n) * 2.8

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            sage: from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.kipnis_shamir import KipnisShamir
            sage: E = KipnisShamir(MAYOProblem(n=24, m=20, o=8, k=9, q=16))
            sage: E.memory_complexity()
            14.169925001442312

        """
        n, _, o, _, _ = self.problem.get_parameters()
        return log2(o * (n ** 2))
    