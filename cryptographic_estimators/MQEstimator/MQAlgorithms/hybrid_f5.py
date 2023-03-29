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


from ...MQEstimator.mq_algorithm import MQAlgorithm
from ...MQEstimator.mq_problem import MQProblem
from ...MQEstimator.MQAlgorithms.f5 import F5
from ...base_algorithm import optimal_parameter
from ...helper import ComplexityType
from math import log2
from sage.all import Integer


class HybridF5(MQAlgorithm):
    r"""
    Construct an instance of HybridF5

    HybridF5 is an algorithm to solve systems of polynomials over a finite field proposed in [BFP09]_, [BFP12]_. The
    algorithm is a tradeoff between exhaustive search and Groebner bases computation. The idea is to fix the value of,
    say, $k$ variables and compute the Groebner bases of $q^{k}$ subsystems, where $q$ is the order of the finite
    field. The Grobner bases computation is done using F5 algorithm.

    .. SEEALSO::
        :class:`mpkc.algorithms.f5.F5` -- class to compute the complexity of F5 algorithm.

    INPUT:

    - ``problem`` -- MQProblem object including all necessary parameters
    - ``h`` -- external hybridization parameter (default: 0)
    - ``w`` -- linear algebra constant (2 <= w <= 3) (default: 2)
    - ``degrees`` -- a list/tuple of degree of the polynomials (default: [2]*m, i.e. quadratic system)

    EXAMPLES::

        sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.hybrid_f5 import HybridF5
        sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
        sage: H = HybridF5(MQProblem(q=256, n=5, m=10))
        sage: H
        HybridF5 estimator for the MQ problem with 5 variables and 10 polynomials
    """

    def __init__(self, problem: MQProblem, **kwargs):
        q = problem.order_of_the_field()
        m = problem.npolynomials()
        if not isinstance(q, (int, Integer)):
            raise TypeError("q must be an integer")

        degrees = kwargs.get('degrees', [2] * m)

        if len(degrees) != m:
            raise ValueError(f"len(degrees) must be equal to {m}")

        super().__init__(problem, **kwargs)
        if degrees == [2] * m:
            self._degrees = [2] * self.npolynomials_reduced()
        else:
            self._degrees = degrees
        self._name = "HybridF5"

        n = self.nvariables_reduced()
        self.set_parameter_ranges('k', 0, n - 1)

    def degree_of_polynomials(self):
        """
        Return a list of degree of the polynomials

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.hybrid_f5 import HybridF5
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: H = HybridF5(MQProblem(q=31, n=5, m=5), degrees=[3]*5)
            sage: H.degree_of_polynomials()
            [3, 3, 3, 3, 3]
        """
        return self._degrees

    @optimal_parameter
    def k(self):
        """
        Return the optimal k

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.hybrid_f5 import HybridF5
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: H = HybridF5(MQProblem(q=31, n=23, m=23))
            sage: H.k()
            2

        TESTS::

            sage: H = HybridF5(MQProblem(q=256, n=10, m=10))
            sage: H.k()
            1
            sage: H = HybridF5(MQProblem(q=256, n=20, m=10))
            sage: H.k()
            1
        """
        return self._get_optimal_parameter('k')

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.hybrid_f5 import HybridF5
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: H = HybridF5(MQProblem(q=256, n=10, m=10), bit_complexities=False)
            sage: H.time_complexity(k=2)
            39.98152077132876

        """
        k = parameters['k']
        n, m, q = self.get_reduced_parameters()
        w = self.linear_algebra_constant()
        degrees = self.degree_of_polynomials()
        E = F5(MQProblem(n=n-k, m=m, q=q), w=w, degrees=degrees, bit_complexities=False)
        h = self._h
        return log2(q) * k + E.time_complexity() + h * log2(q)

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity w.r.t. `k`.

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.hybrid_f5 import HybridF5
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: H = HybridF5(MQProblem(q=7, n=10, m=12), bit_complexities=False)
            sage: H.memory_complexity(k=1)
            20.659592676441402

        """
        k = parameters['k']
        n, m, q = self.get_reduced_parameters()
        w = self.linear_algebra_constant()
        degrees = self.degree_of_polynomials()
        E = F5(MQProblem(n=n - k, m=m, q=q), w=w, degrees=degrees, bit_complexities=False)
        return max(E.memory_complexity(), log2(m * n ** 2))

    def _compute_tilde_o_time_complexity(self, parameters: dict):
        """
        Return the Ō time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.hybrid_f5 import HybridF5
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: H = HybridF5(MQProblem(q=7, n=10, m=12), complexity_type=1)
            sage: H.time_complexity(k=3)
            22.23584595738985

        """
        k = parameters['k']
        n, m, q = self.get_reduced_parameters()
        w = self.linear_algebra_constant()
        degrees = self.degree_of_polynomials()
        E = F5(MQProblem(n=n - k, m=m, q=q), w=w, degrees=degrees, complexity_type=1)
        h = self._h
        return log2(q) * k + E.time_complexity() + h * log2(q)

    def _compute_tilde_o_memory_complexity(self, parameters: dict):
        """
        Return the Ō memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.hybrid_f5 import HybridF5
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: H = HybridF5(MQProblem(q=7, n=10, m=12), complexity_type=1)
            sage: H.memory_complexity(k = 3)
            12.784634845557521

        """
        k = parameters['k']
        n, m, q = self.get_reduced_parameters()
        w = self.linear_algebra_constant()
        degrees = self.degree_of_polynomials()
        E = F5(MQProblem(n=n - k, m=m, q=q), w=w, degrees=degrees, complexity_type=1)
        return max(E.memory_complexity(), log2(m * n ** 2))

    def _find_optimal_tilde_o_parameters(self):
        """
        Return the optimal parameters to achive the optimal Ō time complexity.

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.hybrid_f5 import HybridF5
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = HybridF5(MQProblem(q=7, n=10, m=12), complexity_type=1)
            sage: E.optimal_parameters()
            {'k': 3}

        """
        self._find_optimal_parameters()
