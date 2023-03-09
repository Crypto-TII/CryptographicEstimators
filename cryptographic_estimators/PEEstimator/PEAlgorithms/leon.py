from ...PEEstimator.pe_algorithm import PEAlgorithm
from ...PEEstimator.pe_problem import PEProblem
from ...base_algorithm import optimal_parameter
from ..pe_helper import gv_distance, number_of_weight_d_codewords, isd_cost
from math import log, ceil, log2

class Leon(PEAlgorithm):

    def __init__(self, problem: PEProblem, **kwargs):
        """
            Complexity estimate of Leons algorithm

            TODO add reference to Leons paper

            Estimates are adapted versions of the scripts derived in <TODO add paolos paper> with the code accessible at
            <ADD GITHUB LINK>

            INPUT:

            - ``problem`` -- PEProblem object including all necessary parameters
            - ``codewords_needed_for_success`` -- Number of low word codewords needed for success (default = 100)
        """
        super().__init__(problem, **kwargs)
        self._name = "Leon"
        self._codewords_needed_for_success = kwargs.get("codewords_needed_for_success", 100)
        n, _, _ = self.problem.get_parameters()
        self.set_parameter_ranges('w', 0, n)

    @optimal_parameter
    def w(self):
        """
        Return the optimal parameter $w$ used in the algorithm optimization
        """
        n, k, q = self.problem.get_parameters()
        d = gv_distance(n, k, q)

        while number_of_weight_d_codewords(n, k, q, d) < self._codewords_needed_for_success:
            d += 1
        return d

    def _compute_time_complexity(self, parameters):
        n, k, q = self.problem.get_parameters()
        w=parameters["w"]
        N = number_of_weight_d_codewords(n, k, q, w)

        # todo exchange against call to Fq SD estimator
        return isd_cost(n, k, q, parameters["w"])+log2(ceil(2*(0.57+log(N))))

    def _compute_memory_complexity(self, parameters):
        n, k, q = self.problem.get_parameters()
        # todo add memory of ISD estimator call here
        return 0

    def __repr__(self):
        rep = "Leon estimator for " + str(self.problem)
        return rep
