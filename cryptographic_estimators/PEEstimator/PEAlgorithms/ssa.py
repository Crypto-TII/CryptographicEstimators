from ...PEEstimator.pe_algorithm import PEAlgorithm
from ...PEEstimator.pe_problem import PEProblem
from ...base_algorithm import optimal_parameter
from ..pe_helper import gv_distance, number_of_weight_d_codewords, isd_cost
from math import log, log2


class SSA(PEAlgorithm):

    def __init__(self, problem: PEProblem, **kwargs):
        """
        Complexity estimate of Support Splitting Algorithm

        TODO add reference to SSA paper

        rough Estimate according to <TODO add paolos paper>

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
            sage: A = SSA(PEProblem(n=100,k=50,q=3,w=10))
            sage: A.w()
            2

        """
        return self._compute_time_complexity(parameters), \
               self._compute_memory_complexity(parameters)
    def __repr__(self):
        rep = "Support Splliting Algorithm estimator for " + str(self.problem)
        return rep
