from ...PEEstimator.pe_algorithm import PEAlgorithm
from ...PEEstimator.pe_problem import PEProblem
from ...base_algorithm import optimal_parameter
from ..pe_helper import gv_distance, number_of_weight_d_codewords
from ...SDFqEstimator.sdfq_estimator import SDFqEstimator
from math import log, ceil, log2


class Leon(PEAlgorithm):

    def __init__(self, problem: PEProblem, **kwargs):
        """
        Complexity estimate of Leons algorithm [Leo82]_
        Estimates are adapted versions of the scripts derived in [Beu20]_ with the code accessible at
        https://github.com/WardBeullens/LESS_Attack


        INPUT:

        - ``problem`` -- PEProblem object including all necessary parameters
        - ``codewords_needed_for_success`` -- Number of low word codewords needed for success (default = 100)
        - ``sd_parameters`` -- dictionary of parameters for SDFqEstimator used as a subroutine (default: {})

        """
        super().__init__(problem, **kwargs)
        self._name = "Leon"
        self._codewords_needed_for_success = kwargs.get("codewords_needed_for_success", 100)
        n, _, _, _ = self.problem.get_parameters()
        self.set_parameter_ranges('w', 0, n)

        self.SDFqEstimator = None

        self._SDFqEstimator_parameters = kwargs.get("sd_parameters", {})
        self._SDFqEstimator_parameters.pop("bit_complexities", None)
        self._SDFqEstimator_parameters.pop("nsolutions", None)
        self._SDFqEstimator_parameters.pop("memory_bound", None)

    @optimal_parameter
    def w(self):
        """
        Return the optimal parameter $w$ used in the algorithm optimization

        EXAMPLES::
            sage: from cryptographic_estimators.PEEstimator.PEAlgorithms import Leon
            sage: from cryptographic_estimators.PEEstimator import PEProblem
            sage: A = Leon(PEProblem(n=100,k=50,q=3))
            sage: A.w()
            20

        """
        n, k, q, _ = self.problem.get_parameters()
        d = gv_distance(n, k, q)

        while number_of_weight_d_codewords(n, k, q, d) < self._codewords_needed_for_success:
            d += 1
        return d

    def _compute_time_complexity(self, parameters: dict):
        n, k, q, _ = self.problem.get_parameters()
        w = parameters["w"]
        N = number_of_weight_d_codewords(n, k, q, w)
        self.SDFqEstimator = SDFqEstimator(n=n, k=k, w=w, q=q, nsolutions=0, memory_bound=self.problem.memory_bound,
                                           bit_complexities=0, **self._SDFqEstimator_parameters)
        c_isd = self.SDFqEstimator.fastest_algorithm().time_complexity()
        return c_isd + log2(ceil(2 * (0.57 + log(N))))

    def _compute_memory_complexity(self, parameters: dict):
        n, k, q, _ = self.problem.get_parameters()
        return self.SDFqEstimator.fastest_algorithm().memory_complexity()


    def _time_and_memory_complexity(self, parameters: dict, verbose_information=None):
        """

        INPUT:
        -  ``parameters`` -- dictionary including parameters
        -  ``verbose_information`` -- unused

        EXAMPLES::
            sage: from cryptographic_estimators.PEEstimator.PEAlgorithms import Leon
            sage: from cryptographic_estimators.PEEstimator import PEProblem
            sage: A = Leon(PEProblem(n=100,k=50,q=3))
            sage: A._time_and_memory_complexity({"w": 20})
            (36.42124342248697, 25.270887705262858)

        """
        return self._compute_time_complexity(parameters),\
               self._compute_memory_complexity(parameters)

    def __repr__(self):
        """

        """
        rep = "Leon estimator for " + str(self.problem)
        return rep
