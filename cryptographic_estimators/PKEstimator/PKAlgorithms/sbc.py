from ...PKEstimator.pk_algorithm import PKAlgorithm
from ...PKEstimator.pk_problem import PKProblem
from ...base_algorithm import optimal_parameter
from math import log2, factorial, inf, comb as binomial
from ..pk_helper import gauss_binomial, cost_for_finding_subcode
from ...SDFqEstimator.sdfq_estimator import SDFqEstimator

SBC_ISD = "ISD cost"
SBC_U = "u"


class SBC(PKAlgorithm):
    """
        Complexity estimate of the SBC algorithm

        Originally proposed in
        #Todo : Add references to KMP paper and Santini paper

        The estimates are adapted versions of the code accompanying [SANTINI ET AL], original code is accessible at
        <<GITHUB LINK>>

    """

    def __init__(self, problem: PKProblem, **kwargs):
        super().__init__(problem, **kwargs)
        self._name = "SBC"
        n, m, _, _ = self.problem.get_parameters()

        self.set_parameter_ranges("d", 1, m)
        self.set_parameter_ranges("w", 1, n)
        self.set_parameter_ranges("w1", 1, n)

        self.SDFqEstimator = None
        self.SDFqEstimator_parameters = kwargs.get("sd_parameters", {})
        self.SDFqEstimator_parameters.pop("nsolutions", None)
        self.SDFqEstimator_parameters.pop("memory_bound", None)
        self.SDFqEstimator_parameters.pop("bit_complexities", None)

    @optimal_parameter
    def d(self):
        """
        Return the optimal parameter $d$ used in the algorithm optimization
        """
        return self._get_optimal_parameter("d")

    @optimal_parameter
    def w(self):
        """
        Return the optimal parameter $w$ used in the algorithm optimization
        """
        return self._get_optimal_parameter("w")

    @optimal_parameter
    def w1(self):
        """
        Return the optimal parameter $u$ used in the algorithm optimization
        """
        return self._get_optimal_parameter("w1")

    def _compute_time_and_memory(self, parameters, verbose_information=None):
        """
            Computes the time and memory complexity of the SBC algorithm in number of Fq additions and Fq elements resp.
        """
        d = parameters["d"]
        w = parameters["w"]
        w1 = parameters["w1"]

        time = inf
        memory = inf
        best_u = 0
        n, m, q, ell = self.problem.get_parameters()

        if w1 > w or w < d or n - w < m - d or (d == 1 and w > n - m):
            return inf, inf

        N_w = log2(binomial(n, w)) + log2((q ** d - 1) ** (w - d)) + gauss_binomial(m, d, q) - gauss_binomial(n, d,
                                                                                                              q)  # number of expected subcodes

        if N_w < 0:  # continue only if at least one subcode exists in expectation
            return inf, inf

        if d == 1:
            self.SDFqEstimator = SDFqEstimator(n=n, k=m, w=w, q=q, bit_complexities=0, nsolutions=N_w,
                                               memory_bound=self.problem.memory_bound, **self.SDFqEstimator_parameters)
            c_isd = self.SDFqEstimator.fastest_algorithm().time_complexity()
        else:
            self.SDFqEstimator = None
            c_isd = cost_for_finding_subcode(q, n, m, d, w, N_w)

        w2 = w - w1
        T_K = factorial(n) // factorial(n - w1) + factorial(n) // factorial(n - w2) \
              + factorial(n) ** 2 // q ** (d * ell) // (factorial(n - w1) * factorial(n - w2))

        if self._is_early_abort_possible(log2(T_K)):
            return inf, inf
        L = min(factorial(n) // factorial(n - w1), factorial(n) // factorial(n - w2))
        size_K = max(1, factorial(n) // factorial(n - w) // q ** (d * ell))
        for u in range(1, m):

            T_L = factorial(n) // factorial(m + w - u) + size_K + factorial(n) // q ** (ell * (u - d)) / factorial(
                m + w - u) * size_K
            L = max(L, min(factorial(n) / factorial(m + w - u), size_K))

            T_test = factorial(n - w) // q ** ((u - d) * ell) // factorial(m - u) * size_K

            local_time = log2(2 ** c_isd + (T_K + T_L + T_test) * self.cost_for_list_operation)

            local_memory = log2(L) + log2(self.memory_for_list_element)

            if local_time < time:
                best_u = u
                time = local_time
                memory = local_memory

        if verbose_information is not None:
            verbose_information[SBC_ISD] = c_isd
            verbose_information[SBC_U] = best_u

        return time, memory

    def _compute_time_complexity(self, parameters):
        return self._compute_time_and_memory(parameters)[0]

    def _compute_memory_complexity(self, parameters):
        return self._compute_time_and_memory(parameters)[1]

    def _get_verbose_information(self):
        """
        returns a dictionary containing additional algorithm information
        """
        verb = dict()
        _ = self._compute_time_and_memory(self.optimal_parameters(), verbose_information=verb)
        return verb
