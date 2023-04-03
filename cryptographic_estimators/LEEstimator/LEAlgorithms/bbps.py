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

from ..le_algorithm import LEAlgorithm
from ..le_problem import LEProblem
from ..le_constants import *
from ...base_algorithm import optimal_parameter
from ...PEEstimator.pe_helper import gv_distance
from math import log2, inf, log, comb as binom, factorial
from ...SDFqEstimator.sdfq_estimator import SDFqEstimator, SDFqProblem
from ...base_constants import BASE_BIT_COMPLEXITIES, BASE_MEMORY_BOUND, BASE_NSOLUTIONS


class BBPS(LEAlgorithm):

    def __init__(self, problem: LEProblem, **kwargs):
        """
        Complexity estimate of [BBPS20]_ algorithm.

        Estimates are adapted versions of the scripts derived in [BBPS20]_ with the code accessible at
        https://github.com/paolo-santini/LESS_project

        INPUT:

        - ``problem`` -- PEProblem object including all necessary parameters
        - ``sd_parameters`` -- dictionary of parameters for SDFqEstimator used as a subroutine (default: {})

        EXAMPLES::

            sage: from cryptographic_estimators.LEEstimator.LEAlgorithms import BBPS
            sage: from cryptographic_estimators.LEEstimator import LEProblem
            sage: BBPS(LEProblem(30,20,251))
            BBPS estimator for permutation equivalence problem with (n,k,q) = (30,20,251)

        """
        super().__init__(problem, **kwargs)
        self._name = "BBPS"
        n, k, q = self.problem.get_parameters()

        self.set_parameter_ranges('w_prime', gv_distance(n, k, q), n - k + 2)
        self.set_parameter_ranges('w', gv_distance(n, k, q), n)

        self._SDFqEstimator_parameters = kwargs.get(LE_SD_PARAMETERS, {})
        self._SDFqEstimator_parameters.pop(BASE_BIT_COMPLEXITIES, None)
        self._SDFqEstimator_parameters.pop(BASE_NSOLUTIONS, None)
        self._SDFqEstimator_parameters.pop(BASE_MEMORY_BOUND, None)

    @optimal_parameter
    def w(self):
        """
        Return the optimal parameter $w$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.LEEstimator.LEAlgorithms import BBPS
            sage: from cryptographic_estimators.LEEstimator import LEProblem
            sage: A = BBPS(LEProblem(30,20,251))
            sage: A.w()
            14

        """
        return self._get_optimal_parameter("w")

    @optimal_parameter
    def w_prime(self):
        """
        Return the optimal parameter $w_prime$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.LEEstimator.LEAlgorithms import BBPS
            sage: from cryptographic_estimators.LEEstimator import LEProblem
            sage: A = BBPS(LEProblem(30,20,251))
            sage: A.w_prime()
            10

        """
        return self._get_optimal_parameter("w_prime")

    def _are_parameters_invalid(self, parameters: dict):
        w = parameters["w"]
        w_prime = parameters["w_prime"]
        n, k, q = self.problem.get_parameters()

        if w < w_prime + 1 or w > 2 * w_prime - 1 or w_prime > n - k:
            return True
        return False

    def _time_and_memory_complexity(self, parameters, verbose_information=None):
        """
        Return time complexity of BBPS algorithm

        INPUT:

        -  ``parameters`` -- dictionary including parameters
        -  ``verbose_information`` -- if set to a dictionary within `Nw_prime`, c_isd` and `lists` will be returned.

        """
        w = parameters["w"]
        w_prime = parameters["w_prime"]

        n, k, q = self.problem.get_parameters()
        Nw_prime = (log2(binom(n, w_prime)) + log2(q - 1) * (w_prime - 1) + log2(q) * (k - n))
        if Nw_prime < 0:
            return inf, inf

        pr_w_w_prime = log2(binom(w_prime, 2 * w_prime - w)) + log2(binom(n - w_prime, w - w_prime)) - log2(
            binom(n, w_prime))  # zeta probability in the paper

        L_prime = (1 + Nw_prime * 2 - pr_w_w_prime + log2((2 * log(n)))) / 4
        if L_prime > Nw_prime:
            return inf, inf

        pw = -1 + log2(binom(n, w - w_prime)) + log2(binom(n - (w - w_prime), w - w_prime)) \
             + log2(binom(n - 2 * (w - w_prime), 2 * w_prime - w)) + log2(factorial(2 * w_prime - w)) \
             + log2((q - 1)) * (w - 2 * w_prime + 1) - (log2(binom(n, w_prime)) + log2(binom(n - w_prime, w - w_prime))
                                                        + log2(binom(w_prime, 2 * w_prime - w)))

        M_second = pr_w_w_prime + L_prime * 4 - 2 + pw + log2(2 ** pr_w_w_prime - 2 / ((2 ** Nw_prime) ** 2))
        if M_second > 0:
            return inf, inf

        self.SDFqEstimator = SDFqEstimator(n=n, k=k, w=w_prime, q=q, bit_complexities=0, nsolutions=0,
                                           memory_bound=self.problem.memory_bound, **self._SDFqEstimator_parameters)
        c_isd = self.SDFqEstimator.fastest_algorithm().time_complexity()

        time = c_isd + L_prime - Nw_prime
        # accounting for sampling L_prime different elements from set of Nw_prime elements
        if L_prime > Nw_prime - 1:
            time += log2(L_prime)

        if verbose_information is not None:
            verbose_information[VerboseInformation.NW.value] = Nw_prime
            verbose_information[VerboseInformation.LISTS.value] = L_prime
            verbose_information[VerboseInformation.ISD.value] = c_isd

        return time, self.SDFqEstimator.fastest_algorithm().memory_complexity()

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
