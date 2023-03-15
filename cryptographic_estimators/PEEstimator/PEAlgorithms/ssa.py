from ...PEEstimator.pe_algorithm import PEAlgorithm
from ...PEEstimator.pe_problem import PEProblem
from math import log, log2


class SSA(PEAlgorithm):

    def __init__(self, problem: PEProblem, **kwargs):
        """
        Complexity estimate of Support Splitting Algorithm [Sen06]_
        Rough Estimate according to [BBPS20]_

        INPUT:

        - ``problem`` -- PEProblem object including all necessary parameters

        EXAMPLES::

            sage: from cryptographic_estimators.PEEstimator.PEAlgorithms import SSA
            sage: from cryptographic_estimators.PEEstimator import PEProblem
            sage: SSA(PEProblem(n=100,k=50,q=3))
            Support Splitting Algorithm estimator for permutation equivalence problem with (n,k,q) = (100,50,3)

        """

        super().__init__(problem, **kwargs)
        self._name = "SSA"

    def _compute_time_complexity(self, parameters: dict):
        n, _, q, h = self.problem.get_parameters()
        return log2(n ** 3 + n ** 2 * q ** h * log(h))

    def _compute_memory_complexity(self, parameters: dict):
        n, k, q, h = self.problem.get_parameters()

        return log2(n*h+n*k+n*(n-k))

    def _time_and_memory_complexity(self, parameters: dict, verbose_information=None):
        """

        INPUT:
        -  ``parameters`` -- dictionary including parameters
        -  ``verbose_information`` -- unused

        """
        return self._compute_time_complexity(parameters), \
               self._compute_memory_complexity(parameters)

    def __repr__(self):
        rep = "Support Splitting Algorithm estimator for " + str(self.problem)
        return rep
