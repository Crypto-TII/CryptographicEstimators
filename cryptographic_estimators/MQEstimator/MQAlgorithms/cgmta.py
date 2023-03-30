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
from ...helper import ComplexityType
from math import log2
from sage.all import Integer
from sage.functions.other import sqrt, floor
from sage.functions.other import binomial


class CGMTA(MQAlgorithm):
    r"""
    Construct an instance of CGMT-A estimator

    CGMT-A is an algorithm to solve the MQ problem over any finite field. It works when there is an integer $k$ such
    that $m - 2k < 2k^2 \leq n - 2k$ [CGMT02]_.

    NOTE::

        In this module the compleixties are computed
        for k=  min(m / 2, floor(sqrt(n / 2 - sqrt(n / 2)))).


    INPUT:

    - ``problem`` -- MQProblem object including all necessary parameters
    - ``h`` -- external hybridization parameter (default: 0)
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
    - ``complexity_type`` -- complexity type to consider (0: estimate, 1: tilde O complexity, default: 0)

    EXAMPLES::

        sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.cgmta import CGMTA
        sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
        sage: E = CGMTA(MQProblem(n=41, m=10, q=3))
        sage: E
        CGMT-A estimator for the MQ problem with 41 variables and 10 polynomials

    TESTS::

        sage: E.problem.nvariables() == E.nvariables_reduced()
        True

    """

    def __init__(self, problem: MQProblem, **kwargs):
        n, m, q = problem.get_problem_parameters()
        if not isinstance(q, (int, Integer)):
            raise TypeError("q must be an integer")

        if m > n:
            raise ValueError("m must be <= n")

        super().__init__(problem, **kwargs)
        self._k = min(m / 2, floor(sqrt(n / 2 - sqrt(n / 2))))

        if 2 * self._k ** 2 > n - 2 * self._k or m - 2 * self._k >= 2 * self._k ** 2:
            raise ValueError(
                f'The condition m - 2k < 2k^2 <= n - 2k must be satisfied')

        self._name = "CGMT-A"
        self._n_reduced = n
        self._m_reduced = m

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters


        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.cgmta import CGMTA
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = CGMTA(MQProblem(n=41, m=10, q=3), bit_complexities=False)
            sage: E.time_complexity()
            23.137080884841787

        """
        n, m, q = self.problem.get_problem_parameters()
        k = self._k
        time = (m - k) * log2(q)
        time += log2(2 * k * binomial(n - k, 2))
        return time

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.cgmta import CGMTA
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = CGMTA(MQProblem(n=41, m=10, q=3), bit_complexities=False)
            sage: E.memory_complexity()
            7.339850002884624
        """
        q = self.problem.order_of_the_field()
        k = self._k
        memory = k * log2(q)
        memory += log2(2 * k)
        return memory

    def _compute_tilde_o_time_complexity(self, parameters: dict):
        """
        Return the Ō time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters
        """
        _, m, q = self.problem.get_problem_parameters()
        k = self._k
        return (m - k) * log2(q)

    def _compute_tilde_o_memory_complexity(self, parameters: dict):
        """
        Return the Ō memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters
        """
        q = self.problem.order_of_the_field()
        k = self._k
        return  k * log2(q)


