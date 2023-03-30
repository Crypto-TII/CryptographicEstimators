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


from ...base_algorithm import optimal_parameter
from ...SDEstimator.sd_algorithm import SDAlgorithm
from ...SDEstimator.sd_problem import SDProblem
from ...SDEstimator.sd_helper import _gaussian_elimination_complexity, _mem_matrix, _list_merge_complexity, min_max, \
    binom, log2, inf
from types import SimpleNamespace
from ..sd_constants import *
from ..SDWorkfactorModels.dumer import DumerScipyModel


class Dumer(SDAlgorithm):
    def __init__(self, problem: SDProblem, **kwargs):
        """
        Complexity estimate of Dumer's ISD algorithm

        The algorithm was introduced in [Dum91]_.

        expected weight distribution::

            +--------------------------+------------------+-------------------+
            | <-----+ n - k - l +----->|<-- (k + l)/2 +-->|<--+ (k + l)/2 +-->|
            |           w - 2p         |       p          |        p          |
            +--------------------------+------------------+-------------------+
        INPUT:

        - ``problem`` -- SDProblem object including all necessary parameters


        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import Dumer
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: Dumer(SDProblem(n=100,k=50,w=10))
            Dumer estimator for syndrome decoding problem with (n,k,w) = (100,50,10) over Finite Field of size 2

        """
        super(Dumer, self).__init__(problem, **kwargs)
        self._name = "Dumer"
        self.initialize_parameter_ranges()
        self.scipy_model = DumerScipyModel

    def initialize_parameter_ranges(self):
        """
        initialize the parameter ranges for p, l to start the optimisation 
        process.
        """
        n, k, w = self.problem.get_parameters()
        s = self.full_domain
        self.set_parameter_ranges("p", 0, min_max(w // 2, 20, s))
        self.set_parameter_ranges("l", 0, min_max(n - k, 400, s))

    @optimal_parameter
    def l(self):
        """
        Return the optimal parameter $l$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import Dumer
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = Dumer(SDProblem(n=100,k=50,w=10))
            sage: A.l()
            8
        """
        return self._get_optimal_parameter("l")

    @optimal_parameter
    def p(self):
        """
        Return the optimal parameter $p$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import Dumer
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = Dumer(SDProblem(n=100,k=50,w=10))
            sage: A.p()
            2
        """
        return self._get_optimal_parameter("p")

    def _are_parameters_invalid(self, parameters: dict):
        """
        return if the parameter set `parameters` is invalid

        """
        n, k, w = self.problem.get_parameters()
        par = SimpleNamespace(**parameters)
        k1 = (k + par.l) // 2
        if par.p > w // 2 or k1 < par.p or n - k - par.l < w - 2 * par.p:
            return True
        return False

    def _time_and_memory_complexity(self, parameters, verbose_information=None):
        """
        Computes the expected runtime and memory consumption for a given parameter set.
        """
        n, k, w = self.problem.get_parameters()
        par = SimpleNamespace(**parameters)
        k1 = (k + par.l) // 2

        memory_bound = self.problem.memory_bound

        L1 = binom(k1, par.p)
        if self._is_early_abort_possible(log2(L1)):
            return inf, inf

        memory = log2(2 * L1 + _mem_matrix(n, k, par.r))
        solutions = self.problem.nsolutions

        if memory > memory_bound:
            return inf, memory_bound + 1

        Tp = max(
            log2(binom(n, w)) - log2(binom(n - k - par.l, w - 2 * par.p)) - log2(binom(k1, par.p) ** 2) - solutions, 0)
        Tg = _gaussian_elimination_complexity(n, k, par.r)
        time = Tp + log2(Tg + _list_merge_complexity(L1, par.l, self._hmap))

        if verbose_information is not None:
            verbose_information[VerboseInformation.PERMUTATIONS.value] = Tp
            verbose_information[VerboseInformation.GAUSS.value] = log2(Tg)
            verbose_information[VerboseInformation.LISTS.value] = [
                log2(L1), 2 * log2(L1) - par.l]

        return time, memory

    def __repr__(self):
        """
        """
        rep = "Dumer estimator for " + str(self.problem)
        return rep
