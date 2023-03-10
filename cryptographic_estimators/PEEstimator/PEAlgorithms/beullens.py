from ...PEEstimator.pe_algorithm import PEAlgorithm
from ...PEEstimator.pe_problem import PEProblem
from ...base_algorithm import optimal_parameter
from ..pe_helper import median_size_of_random_orbit, hamming_ball, isd_cost
from math import log, ceil, log2, inf, comb as binomial


class Beullens(PEAlgorithm):

    def __init__(self, problem: PEProblem, **kwargs):
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
        n, _, _, _ = self.problem.get_parameters()
        self.set_parameter_ranges('w', 0, n)

    @optimal_parameter
    def w(self):
        """
        Return the optimal parameter $w$ used in the algorithm optimization
        """
        return self._get_optimal_parameter("w")

    def _time_and_memory_complexity(self, parameters, verbose_information=None):
        n, k, q, _ = self.problem.get_parameters()
        w = parameters["w"]

        search_space_size = hamming_ball(n, q, w) - log2(q) * (n - k) - log2(q - 1)
        if search_space_size < 1:
            return inf, inf

        size_of_orbit = median_size_of_random_orbit(n, w, q)
        if size_of_orbit > log2(q) * (n - k) - log2(ceil(4 * log(n, 2))):
            return inf, inf

        list_size = (search_space_size + log2(2 * log2(n))) / 2
        list_computation = isd_cost(n, k, q, w) - search_space_size + list_size + 1
        # Todo exchange with call to SD estimator (remember to set correct number of solutions)
        normal_form_cost = 2 * list_size

        if verbose_information is not None:
            verbose_information["list size"] = list_size
            verbose_information["list_computation"] = list_computation
            verbose_information["normal form"] = normal_form_cost

        return max(list_computation, normal_form_cost) + log2(n), list_size + log2(n)

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
        rep = "Beullens estimator for " + str(self.problem)
        return rep
