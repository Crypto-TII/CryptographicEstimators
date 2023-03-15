from ...PEEstimator.pe_algorithm import PEAlgorithm
from ...PEEstimator.pe_problem import PEProblem
from math import log, log2


class SSA(PEAlgorithm):

    def __init__(self, problem: PEProblem, **kwargs):
        """
        Complexity estimate of Support Splitting Algorithm [Sen06]_
        https://hal.inria.fr/inria-00073037/document

        rough Estimate according to https://eprint.iacr.org/2022/967.pdf

        INPUT:

        - ``problem`` -- PEProblem object including all necessary parameters
        """

        super().__init__(problem, **kwargs)
        self._name = "SSA"

    def _compute_time_complexity(self, parameters: dict):
        """

        """
        n, _, q, h = self.problem.get_parameters()
        return log2(n ** 3 + n ** 2 * q ** h * log(h))

    def _compute_memory_complexity(self, parameters: dict):
        """

        """
        n, k, q, h = self.problem.get_parameters()

        return log2(n*h+n*k+n*(n-k))

    def _time_and_memory_complexity(self, parameters: dict, verbose_information=None):
        """

        INPUT:
        -  ``parameters`` -- dictionary including parameters
        -  ``verbose_information`` -- unused

        EXAMPLES::
            sage: from cryptographic_estimators.PEEstimator.PEAlgorithms import SSA
            sage: from cryptographic_estimators.PEEstimator import PEProblem
            sage: A = SSA(PEProblem(n=100,k=50,q=3))
            sage: A._time_and_memory_complexity({})
            (94.50375226997703, 13.872674880270605)

        """
        return self._compute_time_complexity(parameters), \
               self._compute_memory_complexity(parameters)

    def __repr__(self):
        rep = "Support Splliting Algorithm estimator for " + str(self.problem)
        return rep
