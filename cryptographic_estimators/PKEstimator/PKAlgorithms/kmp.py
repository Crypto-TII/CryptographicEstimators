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
from math import log2, factorial


class KMP(PKAlgorithm):
    """
    Complexity estimate of the KMP algorithm

    Originally proposed in [KMP19]_ . The estimates are adapted versions of the code accompanying [SBC22]_, original
    code is accessible at https://github.com/secomms/pkpattack

    EXAMPLES::

        sage: from cryptographic_estimators.PKEstimator.PKAlgorithms import KMP
        sage: from cryptographic_estimators.PKEstimator import PKProblem
        sage: KMP(PKProblem(n=100,m=50,q=31,ell=2))
        KMP estimator for the permuted kernel problem with (n,m,q,ell) = (100,50,31,2)

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

        EXAMPLES::

            sage: from cryptographic_estimators.PKEstimator.PKAlgorithms import KMP
            sage: from cryptographic_estimators.PKEstimator import PKProblem
            sage: A = KMP(PKProblem(n=100,m=50,q=31,ell=2))
            sage: A.u()
            24

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
            verbose_information[VerboseInformation.KMP_L1.value] = log2(L1)
            verbose_information[VerboseInformation.KMP_L2.value] = log2(L2)
            verbose_information[VerboseInformation.KMP_FINAL_LIST.value] = log2(num_coll)

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
