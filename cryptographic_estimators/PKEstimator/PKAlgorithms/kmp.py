from ...PKEstimator.pk_algorithm import PKAlgorithm
from ...PKEstimator.pk_problem import PKProblem
from ...base_algorithm import optimal_parameter
from math import log2, factorial

KMP_L1 = "L1"
KMP_L2 = "L2"
KMP_FINAL_LIST = "final list"


class KMP(PKAlgorithm):
    """
        Complexity estimate of the KMP algorithm

        Originally proposed in
        #Todo : Add references to KMP paper and Santini paper

        The estimates are adapted versions of the code accompanying [SANTINI ET AL], original code is accessible at
        <<GITHUB LINK>>

    """

    def __init__(self, problem: PKProblem, **kwargs):
        super().__init__(problem, **kwargs)
        self._name = "KMP"
        _, m, _, _ = self.problem.get_parameters()

        self.set_parameter_ranges("u", 0, m)

    @optimal_parameter
    def u(self):
        """
        Return the optimal parameter $u$ used in the algorithm optimization
        """
        return self._get_optimal_parameter("u")

    def _compute_time_and_memory(self, parameters, verbose_information=None):
        """
            Computes the time and memory complexity of the KMP algorithm in number of Fq additions and Fq elements resp.
        """
        u = parameters["u"]
        n, m, q, ell = self.problem.get_parameters()
        u1 = int((n - m + u) / 2)
        u2 = n - m + u - u1

        L1 = log2(factorial(n) / factorial(n - u1))
        L2 = log2(factorial(n) / factorial(n - u2))
        num_coll = log2(
            factorial(n) * factorial(n) / factorial(n - u1) / factorial(n - u2) * q ** (ell * (n - m - u1 - u2)))

        time = log2(2 ** L1 + 2 ** L2 + 2 ** num_coll) + log2(self.cost_for_list_operation)  # TODO fix according to what we agree on
        memory = min(L1, L2) + log2(self.memory_for_list_element)  # TODO fix according to how many Fq elements we need per list element

        if verbose_information is not None:
            verbose_information[KMP_L1] = L1
            verbose_information[KMP_L2] = L2
            verbose_information[KMP_FINAL_LIST] = num_coll
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
