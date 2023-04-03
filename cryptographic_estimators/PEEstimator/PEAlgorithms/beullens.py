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

from ..pe_algorithm import PEAlgorithm
from ..pe_problem import PEProblem
from ..pe_constants import *
from ...base_algorithm import optimal_parameter
from ..pe_helper import median_size_of_random_orbit, hamming_ball
from math import log, ceil, log2, inf
from ...base_constants import BASE_MEMORY_BOUND, BASE_NSOLUTIONS, BASE_BIT_COMPLEXITIES
from ...SDFqEstimator.sdfq_estimator import SDFqEstimator


class Beullens(PEAlgorithm):

    def __init__(self, problem: PEProblem, **kwargs):
        """
        Complexity estimate of Beullens algorithm

        Estimates are adapted versions of the scripts derived in [Beu20]_ with the code accessible at
        https://github.com/WardBeullens/LESS_Attack

        INPUT:

        - ``problem`` -- PEProblem object including all necessary parameters
        - ``sd_parameters`` -- dictionary of parameters for SDFqEstimator used as a subroutine (default: {})

        EXAMPLES::

            sage: from cryptographic_estimators.PEEstimator.PEAlgorithms import Beullens
            sage: from cryptographic_estimators.PEEstimator import PEProblem
            sage: Beullens(PEProblem(n=100,k=50,q=3))
            Beullens estimator for permutation equivalence problem with (n,k,q) = (100,50,3)

        """
        super().__init__(problem, **kwargs)
        self._name = "Beullens"
        n, k, _, _ = self.problem.get_parameters()
        self.set_parameter_ranges('w', 0, n - k)

        self.SDFqEstimator = None

        self._SDFqEstimator_parameters = kwargs.get(PE_SD_PARAMETERS, {})
        self._SDFqEstimator_parameters.pop(BASE_BIT_COMPLEXITIES, None)
        self._SDFqEstimator_parameters.pop(BASE_NSOLUTIONS, None)
        self._SDFqEstimator_parameters.pop(BASE_MEMORY_BOUND, None)

    @optimal_parameter
    def w(self):
        """
        Return the optimal parameter $w$ used in the algorithm optimization

        EXAMPLES::
            sage: from cryptographic_estimators.PEEstimator.PEAlgorithms import Beullens
            sage: from cryptographic_estimators.PEEstimator import PEProblem
            sage: A = Beullens(PEProblem(n=100,k=50,q=31))
            sage: A.w()
            42

        """
        return self._get_optimal_parameter("w")

    def _time_and_memory_complexity(self, parameters: dict, verbose_information=None):
        """

        INPUT:
        -  ``parameters`` -- dictionary including parameters
        -  ``verbose_information`` -- if set to a dictionary `lists`,
                                      `list_cost` and `norm_factor` will be returned.

        """
        n, k, q, _ = self.problem.get_parameters()
        w = parameters["w"]

        search_space_size = hamming_ball(n, q, w) - log2(q) * (n - k) - log2(q - 1)
        if search_space_size < 1:
            return inf, inf

        size_of_orbit = median_size_of_random_orbit(n, w, q)
        if size_of_orbit > log2(q) * (n - k) - log2(ceil(4 * log(n, 2))):
            return inf, inf

        list_size = (search_space_size + log2(2 * log2(n))) / 2

        self.SDFqEstimator = SDFqEstimator(n=n, k=k, w=w, q=q, bit_complexities=0, nsolutions=0,
                                           memory_bound=self.problem.memory_bound, **self._SDFqEstimator_parameters)
        c_isd = self.SDFqEstimator.fastest_algorithm().time_complexity()
        m_isd = self.SDFqEstimator.fastest_algorithm().memory_complexity()
        list_computation = c_isd - search_space_size + list_size + 1

        normal_form_cost = 1 + list_size

        if verbose_information is not None:
            verbose_information[VerboseInformation.LISTS_SIZE.value] = list_size
            verbose_information[VerboseInformation.LIST_COMPUTATION.value] = list_computation
            verbose_information[VerboseInformation.NORMAL_FORM.value] = normal_form_cost

        return max(list_computation, normal_form_cost + log2(n)), max(m_isd, list_size + log2(n))

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
