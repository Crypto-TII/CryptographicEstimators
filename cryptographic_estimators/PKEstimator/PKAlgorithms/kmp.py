from ..pk_algorithm import PKAlgorithm
from ..pk_problem import PKProblem
from ..pk_constants import *
from ...base_algorithm import optimal_parameter
from math import log2, factorial



class KMP(PKAlgorithm):
    """
        Complexity estimate of the KMP algorithm

        Originally proposed in
        #Todo : Add references to KMP paper and Santini paper
        #santini: https://eprint.iacr.org/2022/1749.pdf

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

    def _compute_time_and_memory(self, parameters: dict, verbose_information=None):
        """
        Computes the time and memory complexity of the KMP algorithm in number of Fq additions and Fq elements resp.

        INPUT:
        -  ``parameters`` -- dictionary including parameters
        -  ``verbose_information`` -- if set to a dictionary `L1`, `L1`, and `final_list` will be returned.

        """
        u = parameters["u"]
        n, m, q, ell = self.problem.get_parameters()
        u1 = int((n - m + u) / 2)
        u2 = n - m + u - u1

        L1 = factorial(n) // factorial(n - u1)
        L2 = factorial(n) // factorial(n - u2)
        num_coll = factorial(n) * factorial(n) // factorial(n - u1) \
                   // factorial(n - u2) * q ** (ell * (n - m - u1 - u2))

        time = log2(L1 + L2 + num_coll) + log2(self.cost_for_list_operation)
        memory = log2(L1 + L2) + log2(self.memory_for_list_element)

        if verbose_information is not None:
            verbose_information[VerboseInformation.KMP_L1] = L1
            verbose_information[VerboseInformation.KMP_L2] = L2
            verbose_information[VerboseInformation.KMP_FINAL_LIST] = num_coll

        return time, memory

    def _compute_time_complexity(self, parameters: dict):
        """

        INPUT:
        -  ``parameters`` -- dictionary including parameters

        """
        return self._compute_time_and_memory(parameters)[0]

    def _compute_memory_complexity(self, parameters: dict):
        """

        INPUT:
        -  ``parameters`` -- dictionary including parameters

        """
        return self._compute_time_and_memory(parameters)[1]

    def _get_verbose_information(self):
        """
        returns a dictionary containing additional algorithm information
        """
        verb = dict()
        _ = self._compute_time_and_memory(self.optimal_parameters(), verbose_information=verb)
        return verb
