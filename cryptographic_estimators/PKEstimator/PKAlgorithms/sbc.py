# ****************************************************************************
# Copyright 2023 Technology Innovation Institute
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ****************************************************************************

from ..pk_algorithm import PKAlgorithm
from ..pk_problem import PKProblem
from ..pk_constants import *
from ...base_algorithm import optimal_parameter
from math import factorial, inf, comb as binomial, log2
from ..pk_helper import gauss_binomial, cost_for_finding_subcode
from ...SDFqEstimator.sdfq_estimator import SDFqEstimator


class SBC(PKAlgorithm):
    """
    Complexity estimate of the SBC algorithm

    The estimates are adapted versions of the code accompanying [SBC22]_, original code is accessible at
    https://github.com/secomms/pkpattack

    EXAMPLES::

        sage: from cryptographic_estimators.PKEstimator.PKAlgorithms import SBC
        sage: from cryptographic_estimators.PKEstimator import PKProblem
        sage: SBC(PKProblem(n=20,m=10,q=7,ell=2))
        SBC estimator for the permuted kernel problem with (n,m,q,ell) = (20,10,7,2)

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

        EXAMPLES::

            sage: from cryptographic_estimators.PKEstimator.PKAlgorithms import SBC
            sage: from cryptographic_estimators.PKEstimator import PKProblem
            sage: A = SBC(PKProblem(n=20,m=10,q=7,ell=2))
            sage: A.d()
            3

        """
        return self._get_optimal_parameter("d")

    @optimal_parameter
    def w(self):
        """
        Return the optimal parameter $w$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.PKEstimator.PKAlgorithms import SBC
            sage: from cryptographic_estimators.PKEstimator import PKProblem
            sage: A = SBC(PKProblem(n=20,m=10,q=7,ell=2))
            sage: A.w()
            11

        """
        return self._get_optimal_parameter("w")

    @optimal_parameter
    def w1(self):
        """
        Return the optimal parameter $w1$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.PKEstimator.PKAlgorithms import SBC
            sage: from cryptographic_estimators.PKEstimator import PKProblem
            sage: A = SBC(PKProblem(n=20,m=10,q=7,ell=2))
            sage: A.w1()
            5

        """
        return self._get_optimal_parameter("w1")

    def _are_parameters_invalid(self, parameters: dict):
        d = parameters["d"]
        w = parameters["w"]
        w1 = parameters["w1"]

        n, m, q, ell = self.problem.get_parameters()

        if w1 > w or w < d or n - w < m - d or (d == 1 and w > n - m):
            return True
        return False

    def _compute_time_and_memory(self, parameters: dict, verbose_information=None):
        """
        Computes the time and memory complexity of the SBC algorithm in number of Fq additions and Fq elements resp.

        INPUT:

        -  ``parameters`` -- dictionary including parameters
        -  ``verbose_information`` -- if set to a dictionary `L1`, `L1`, and `final_list` will be returned.

        """
        d = parameters["d"]
        w = parameters["w"]
        w1 = parameters["w1"]

        time = inf
        memory = inf
        best_u = 0
        n, m, q, ell = self.problem.get_parameters()



        N_w = log2(binomial(n, w)) + log2((q ** d - 1)) * (w - d) + gauss_binomial(m, d, q) - gauss_binomial(n, d,
                                                                                                             q)  # number of expected subcodes

        if N_w < 0:  # continue only if at least one subcode exists in expectation
            return inf, inf

        if d == 1:
            self.SDFqEstimator = SDFqEstimator(n=n, k=m, w=w, q=q, bit_complexities=0, nsolutions=N_w,
                                               memory_bound=self.problem.memory_bound, **self.SDFqEstimator_parameters)
            c_isd = self.SDFqEstimator.fastest_algorithm().time_complexity()
        else:
            self.SDFqEstimator = None
            c_isd = cost_for_finding_subcode(n, m, d, w, N_w)

        w2 = w - w1
        T_K = factorial(n) // factorial(n - w1) + factorial(n) // factorial(n - w2) \
              + factorial(n) ** 2 // q ** (d * ell) // (factorial(n - w1) * factorial(n - w2))

        if self._is_early_abort_possible(log2(T_K)):
            return inf, inf
        L = min(factorial(n) // factorial(n - w1), factorial(n) // factorial(n - w2))
        size_K = max(1, factorial(n) // factorial(n - w) // q ** (d * ell))
        for u in range(1, m):

            if u > d:
                T_L = factorial(n) // factorial(m + w - u) + size_K + factorial(n) // factorial(m + w - u) * size_K \
                      // q ** (ell * (u - d))
            else:
                T_L = factorial(n) // factorial(m + w - u) + size_K + factorial(n) * q ** (ell * (d - u)) // factorial(
                    m + w - u) * size_K
            L = max(L, min(factorial(n) // factorial(m + w - u), size_K))

            T_test = factorial(n - w) // q ** ((u - d) * ell) // factorial(m - u) * size_K

            local_time = log2(2 ** c_isd + (T_K + T_L + T_test) * self.cost_for_list_operation)

            local_memory = log2(L) + log2(self.memory_for_list_element)

            if local_time < time:
                best_u = u
                time = local_time
                memory = local_memory

        if verbose_information is not None:
            verbose_information[VerboseInformation.SBC_ISD] = c_isd
            verbose_information[VerboseInformation.SBC_U] = best_u

        return time, memory

    def _compute_time_complexity(self, parameters: dict):
        return self._compute_time_and_memory(parameters)[0]

    def _compute_memory_complexity(self, parameters: dict):
        return self._compute_time_and_memory(parameters)[1]

    def _get_verbose_information(self):
        """
        returns a dictionary containing additional algorithm information
        """
        verb = dict()
        _ = self._compute_time_and_memory(self.optimal_parameters(), verbose_information=verb)
        return verb
