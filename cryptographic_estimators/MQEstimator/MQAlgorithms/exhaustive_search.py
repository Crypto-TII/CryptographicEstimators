

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

    def time_complexity(self):
        """
        Return the time complexity of the exhaustive search algorithm

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.exhaustive_search import ExhaustiveSearch
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = ExhaustiveSearch(MQProblem(q=3, n=10, m=12), bit_complexities=False)
            sage: E.time_complexity()
            15.917197145402291

        TESTS::

            sage: E0 = ExhaustiveSearch(MQProblem(n=15, m=12, q=3))
            sage: E1 = ExhaustiveSearch(MQProblem(n=17, m=12, q=3))
            sage: E0.time_complexity() == E1.time_complexity()
            True
        """
        if self._time_complexity is not None:
            return self._time_complexity

        n, _, q = self.get_reduced_parameters()
        nsolutions = 2 ** self.problem.nsolutions
        self._time_complexity = n * log2(q)
        if self.complexity_type == ComplexityType.ESTIMATE.value:
            if q == 2:
                self._time_complexity += log2(4 * log2(n))
            else:
                self._time_complexity += log2(log(n, q))
            self._time_complexity -= log2(nsolutions + 1)
            h = self._h
            self._time_complexity += h * log2(q)
            if self.bit_complexities:
                self._time_complexity = self.problem.to_bitcomplexity_time(self._time_complexity)
        return self._time_complexity

    def memory_complexity(self):
        """
        Return the memory complexity of the exhaustive search algorithm

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.exhaustive_search import ExhaustiveSearch
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = ExhaustiveSearch(MQProblem(q=3, n=10, m=12), bit_complexities=False)
            sage: E.memory_complexity()
            10.228818690495881

        TESTS::

            sage: E0 = ExhaustiveSearch(MQProblem(n=15, m=12, q=3))
            sage: E1 = ExhaustiveSearch(MQProblem(n=17, m=12, q=3))
            sage: E0.memory_complexity() == E1.memory_complexity()
            True
        """
        if self._memory_complexity is not None:
            return self._memory_complexity

        n, m, _ = self.get_reduced_parameters()
        self._memory_complexity = 0
        if self.complexity_type == ComplexityType.ESTIMATE.value:
            self._memory_complexity = log2(m * n ** 2)
            if self.bit_complexities:
                self._memory_complexity = self.problem.to_bitcomplexity_time(self._memory_complexity)
        return self._memory_complexity


