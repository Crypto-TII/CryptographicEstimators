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

    def _compute_time_complexity(self, parameters):
        n, _, q, h = self.problem.get_parameters()
        return log2(n ** 3 + n ** 2 * q ** h * log(h))

    def _compute_memory_complexity(self, parameters):
        n, k, q, h = self.problem.get_parameters()

        return log2(n*h+n*k+n*(n-k))

    def __repr__(self):
        rep = "Support Splliting Algorithm estimator for " + str(self.problem)
        return rep
