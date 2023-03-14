from ..le_algorithm import LEAlgorithm
from ..le_problem import LEProblem
from ..le_helper import peters_isd
from ...base_algorithm import optimal_parameter
from ...PEEstimator.pe_helper import gv_distance
from math import log2, inf, log, comb as binom, factorial


class BBPS(LEAlgorithm):

    def __init__(self, problem: LEProblem, **kwargs):
        """
            Complexity estimate of Beullens algorithm

            TODO add reference to Beullens

            Estimates are adapted versions of the scripts derived in <Beullens> with the code accessible at
            <ADD GITHUB LINK>

            INPUT:

            - ``problem`` -- PEProblem object including all necessary parameters
        """
        super().__init__(problem, **kwargs)
        self._name = "Beullens"
        n, k, q = self.problem.get_parameters()

        self.set_parameter_ranges('w_prime', gv_distance(n,k,q), n - k + 2)
        self.set_parameter_ranges('w', gv_distance(n,k,q), n)

    @optimal_parameter
    def w(self):
        """
        Return the optimal parameter $w$ used in the algorithm optimization
        """
        return self._get_optimal_parameter("w")

    @optimal_parameter
    def w_prime(self):
        """
        Return the optimal parameter $w$ used in the algorithm optimization
        """
        return self._get_optimal_parameter("w_prime")

    def _time_and_memory_complexity(self, parameters, verbose_information=None):
        w = parameters["w"]
        w_prime = parameters["w_prime"]
        time=0
        if w < w_prime + 1 or w > 2 * w_prime - 1:
            return inf, inf

        n, k, q = self.problem.get_parameters()
        C_isd = peters_isd(n, k, q, w_prime)
        Nw_prime = (log2(binom(n, w_prime)) + log2(q - 1) * (w_prime - 1) + log2(q) * (k - n))
        pr_w_w_prime = log2(binom(w_prime, 2 * w_prime - w)) + log2(binom(n - w_prime, w - w_prime)) - log2(
            binom(n, w_prime))  # zeta probability in the paper
        L_prime = (1 + Nw_prime * 2 - pr_w_w_prime + log2((2 * log(n)))) / 4
        if L_prime > Nw_prime:
            return inf, inf

        max_cost = C_isd + L_prime - Nw_prime + log2(L_prime)
        if self._is_early_abort_possible(max_cost):
            return inf, inf

        pw = -1 + log2(binom(n, w - w_prime)) + log2(binom(n - (w - w_prime), w - w_prime)) \
             + log2(binom(n - 2 * (w - w_prime), 2 * w_prime - w)) + log2(factorial(2 * w_prime - w)) \
             + log2((q - 1)) * (w - 2 * w_prime + 1) - (log2(binom(n, w_prime)) + log2(binom(n - w_prime, w - w_prime))
                                                        + log2(binom(w_prime, 2 * w_prime - w)))

        M_second = pr_w_w_prime + L_prime * 4 - 2 + pw + pr_w_w_prime
        if M_second > 0:
            return inf, inf


        time = C_isd + L_prime - Nw_prime
        # accounting for sampling L_prime different elements from set of Nw_prime elements
        if L_prime > Nw_prime - 1:
            time += log2(L_prime)

        if verbose_information is not None:
            verbose_information["Nw_prime"] = Nw_prime
            # verbose_information["list_computation"] = list_computation
            # verbose_information["normal form"] = normal_form_cost

            # todo fix memory
        return time, 0


    def _compute_time_complexity(self, parameters):
        return self._time_and_memory_complexity(parameters)[0]

    def _compute_memory_complexity(self, parameters):
        return self._time_and_memory_complexity(parameters)[1]

    def _get_verbose_information(self):
        """
        returns a dictionary containing additional algorithm information
        """
        verb = dict()
        _ = self._time_and_memory_complexity(self.optimal_parameters(), verbose_information=verb)
        return verb

    def __repr__(self):
        rep = "BBPS estimator for " + str(self.problem)
        return rep