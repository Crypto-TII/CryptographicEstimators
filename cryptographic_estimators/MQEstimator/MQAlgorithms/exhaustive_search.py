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
from sage.functions.log import log


class ExhaustiveSearch(MQAlgorithm):
    r"""
    Construct an instance of Exhaustive Search estimator
    ExhaustiveSearch solves the MQ problem by evaluating all possible solutions until one is found.
    The formulas used in this module are generalizations of one shown in [BCCCNSY10]_

    INPUT:

    - ``problem`` -- MQProblem object including all necessary parameters
    - ``h`` -- external hybridization parameter (default: 0)
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
    - ``complexity_type`` -- complexity type to consider (0: estimate, 1: tilde O complexity, default: 0)

    EXAMPLES::

        sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.exhaustive_search import ExhaustiveSearch
        sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
        sage: E = ExhaustiveSearch(MQProblem(n=10, m=12, q=3))
        sage: E
        ExhaustiveSearch estimator for the MQ problem with 10 variables and 12 polynomials
    """

    def __init__(self, problem: MQProblem, **kwargs):
        q = problem.order_of_the_field()
        if not isinstance(q, (int, Integer)):
            raise TypeError("q must be an integer")

        super().__init__(problem, **kwargs)
        self._name = "ExhaustiveSearch"

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.exhaustive_search import ExhaustiveSearch
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = ExhaustiveSearch(MQProblem(q=3, n=10, m=12), bit_complexities=False)
            sage: E.time_complexity()
            15.917197145402291

            sage: E0 = ExhaustiveSearch(MQProblem(n=15, m=12, q=3))
            sage: E1 = ExhaustiveSearch(MQProblem(n=17, m=12, q=3))
            sage: E0.time_complexity() == E1.time_complexity()
            True
        """
        n, _, q = self.get_reduced_parameters()
        nsolutions = 2 ** self.problem.nsolutions
        time = n * log2(q)
        if q == 2:
            time += log2(4 * log2(n))
        else:
            time += log2(log(n, q))
        time -= log2(nsolutions + 1)
        h = self._h
        time += h * log2(q)
        return time

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.exhaustive_search import ExhaustiveSearch
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = ExhaustiveSearch(MQProblem(q=3, n=10, m=12), bit_complexities=False)
            sage: E.memory_complexity()
            10.228818690495881


            sage: E0 = ExhaustiveSearch(MQProblem(n=15, m=12, q=3))
            sage: E1 = ExhaustiveSearch(MQProblem(n=17, m=12, q=3))
            sage: E0.memory_complexity() == E1.memory_complexity()
            True
        """
        n, m, _ = self.get_reduced_parameters()
        return log2(m * n ** 2)


    def _compute_tilde_o_time_complexity(self, parameters: dict):
        """
        Return the Ō time complexity of the algorithm for a given set of parameters

        """
        n, _, q = self.get_reduced_parameters()
        return  n * log2(q)

    def _compute_tilde_o_memory_complexity(self, parameters: dict):
        """
        Return the Ō memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        return 0

