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

from ...PEEstimator.pe_algorithm import PEAlgorithm
from ...PEEstimator.pe_problem import PEProblem
from ...base_algorithm import optimal_parameter
from ..pe_helper import gv_distance, number_of_weight_d_codewords
from ...SDFqEstimator.sdfq_estimator import SDFqEstimator
from math import log, ceil, log2


class Leon(PEAlgorithm):

    def __init__(self, problem: PEProblem, **kwargs):
        """
        Complexity estimate of Leons algorithm [Leo82]_
        Estimates are adapted versions of the scripts derived in [Beu20]_ with the code accessible at
        https://github.com/WardBeullens/LESS_Attack


        INPUT:

        - ``problem`` -- PEProblem object including all necessary parameters
        - ``codewords_needed_for_success`` -- Number of low word codewords needed for success (default = 100)
        - ``sd_parameters`` -- dictionary of parameters for SDFqEstimator used as a subroutine (default: {})

        EXAMPLES::

            sage: from cryptographic_estimators.PEEstimator.PEAlgorithms import Leon
            sage: from cryptographic_estimators.PEEstimator import PEProblem
            sage: Leon(PEProblem(n=100,k=50,q=3))
            Leon estimator for permutation equivalence problem with (n,k,q) = (100,50,3)

        """
        super().__init__(problem, **kwargs)
        self._name = "Leon"
        n, k, q, _ = self.problem.get_parameters()
        self._codewords_needed_for_success = kwargs.get("codewords_needed_for_success",
                                                        min(100, int(number_of_weight_d_codewords(n, k, q,
                                                                                                  gv_distance(n, k,
                                                                                                              q) + 3))))
        self.set_parameter_ranges('w', 0, n)

        self.SDFqEstimator = None

        self._SDFqEstimator_parameters = kwargs.get("sd_parameters", {})
        self._SDFqEstimator_parameters.pop("bit_complexities", None)
        self._SDFqEstimator_parameters.pop("nsolutions", None)
        self._SDFqEstimator_parameters.pop("memory_bound", None)

    @optimal_parameter
    def w(self):
        """
        Return the optimal parameter $w$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.PEEstimator.PEAlgorithms import Leon
            sage: from cryptographic_estimators.PEEstimator import PEProblem
            sage: A = Leon(PEProblem(n=100,k=50,q=3))
            sage: A.w()
            20

        """
        n, k, q, _ = self.problem.get_parameters()
        d = gv_distance(n, k, q)

        while number_of_weight_d_codewords(n, k, q, d) < self._codewords_needed_for_success and d < n - k:
            d += 1
        return d

    def _compute_time_complexity(self, parameters: dict):
        n, k, q, _ = self.problem.get_parameters()
        w = parameters["w"]
        N = number_of_weight_d_codewords(n, k, q, w)
        self.SDFqEstimator = SDFqEstimator(n=n, k=k, w=w, q=q, nsolutions=0, memory_bound=self.problem.memory_bound,
                                           bit_complexities=0, **self._SDFqEstimator_parameters)
        c_isd = self.SDFqEstimator.fastest_algorithm().time_complexity()
        return c_isd + log2(ceil(2 * (0.57 + log(N))))

    def _compute_memory_complexity(self, parameters: dict):
        n, k, q, _ = self.problem.get_parameters()
        return self.SDFqEstimator.fastest_algorithm().memory_complexity()

    def __repr__(self):
        rep = "Leon estimator for " + str(self.problem)
        return rep
