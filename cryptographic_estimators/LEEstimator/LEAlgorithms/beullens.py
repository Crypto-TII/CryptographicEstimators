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
from ...PEEstimator.pe_helper import median_size_of_random_orbit
from ..le_helper import cost_to_find_random_2dim_subcodes_with_support_w
from math import log2, inf, ceil, log, comb as binom


class Beullens(LEAlgorithm):

    def __init__(self, problem: LEProblem, **kwargs):
        """
        Complexity estimate of Beullens algorithm

        Estimates are adapted versions of the scripts derived in [Beu20]_ with the code accessible at
        https://github.com/WardBeullens/LESS_Attack

        INPUT:

        - ``problem`` -- LEProblem object including all necessary parameters
        - ``sd_parameters`` -- dictionary of parameters for SDFqEstimator used as a subroutine (default: {})

        EXAMPLES::

            sage: from cryptographic_estimators.LEEstimator.LEAlgorithms import Beullens
            sage: from cryptographic_estimators.LEEstimator import LEProblem
            sage: Beullens(LEProblem(n=100,k=50,q=3))
            Beullens estimator for permutation equivalence problem with (n,k,q) = (100,50,3)

        """
        super().__init__(problem, **kwargs)
        self._name = "Beullens"
        n, k, _ = self.problem.get_parameters()
        self.set_parameter_ranges('w', 0, n-k+1)

    @optimal_parameter
    def w(self):
        """
        Return the optimal parameter $w$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.LEEstimator.LEAlgorithms import Beullens
            sage: from cryptographic_estimators.LEEstimator import LEProblem
            sage: A = Beullens(LEProblem(n=100,k=50,q=3))
            sage: A.w()
            34

        """
        return self._get_optimal_parameter("w")

    def _time_and_memory_complexity(self, parameters, verbose_information=None):
        """
        Return time and memory complexity of Beulens algorithm for given parameters

        INPUT:

        -  ``parameters`` -- dictionary including parameters
        -  ``verbose_information`` -- if set to a dictionary with additional information will be returned.

        """
        n, k, q = self.problem.get_parameters()
        w = parameters["w"]

        search_space_size = log2(binom(n, w)) + log2(q) * (2 * (w - 2) - 2 * (n - k))
        if search_space_size < 0:
            return inf, inf

        size_of_orbit = median_size_of_random_orbit(n, w, q) + log2(q - 1) * (w - 1)
        if size_of_orbit > log2(q) * (2 * (n - k)) - log2(ceil(4 * log2(n))):
            return inf, inf

        list_size = (search_space_size + log2(2 * log2(n))) / 2
        list_computation = cost_to_find_random_2dim_subcodes_with_support_w(n, k, w) \
                           - search_space_size + list_size + 1

        normal_form_cost = 1 + log2(q) + list_size

        if verbose_information is not None:
            verbose_information[VerboseInformation.LISTS_SIZE.value] = list_size
            verbose_information[VerboseInformation.LISTS.value] = list_computation
            verbose_information[VerboseInformation.NORMAL_FORM.value] = normal_form_cost

        return max(list_computation, normal_form_cost) + log2(n), list_size + log2(n)

    def _compute_time_complexity(self, parameters: dict):
        return self._time_and_memory_complexity(parameters)[0]

    def _compute_memory_complexity(self, parameters: dict):
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
