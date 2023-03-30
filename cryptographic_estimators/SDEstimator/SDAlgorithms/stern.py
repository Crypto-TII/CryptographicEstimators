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
from ...SDEstimator.sd_helper import _gaussian_elimination_complexity, _mem_matrix, _list_merge_complexity, binom, log2, min_max, inf
from types import SimpleNamespace
from ..sd_constants import *
from ..SDWorkfactorModels.stern import SternScipyModel


class Stern(SDAlgorithm):
    def __init__(self, problem: SDProblem, **kwargs):
        """
        Construct an instance of Stern's estimator [Ste88]_, [BLP08]_.

        Expected weight distribution::

            +-------------------------+---------+-------------+-------------+
            | <----+ n - k - l +----> |<-- l -->|<--+ k/2 +-->|<--+ k/2 +-->|
            |          w - 2p         |    0    |      p      |      p      |
            +-------------------------+---------+-------------+-------------+

        INPUT:

        - ``problem`` -- SDProblem object including all necessary parameters

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import Stern
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: Stern(SDProblem(n=100,k=50,w=10))
            Stern estimator for syndrome decoding problem with (n,k,w) = (100,50,10) over Finite Field of size 2
        """
        self._name = "Stern"
        super(Stern, self).__init__(problem, **kwargs)
        self.initialize_parameter_ranges()
        self.scipy_model = SternScipyModel

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

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import Stern
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = Stern(SDProblem(n=100,k=50,w=10))
            sage: A.l()
            9
        """

        return self._get_optimal_parameter("l")

    @optimal_parameter
    def p(self):
        """
        Return the optimal parameter $p$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import Stern
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = Stern(SDProblem(n=100,k=50,w=10))
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
        k1 = k // 2
        if par.p > w // 2 or k1 < par.p or n - k - par.l < w - 2 * par.p:
            return True
        return False

    def _valid_choices(self):
        """
        Generator which yields on each call a new set of valid parameters based on the `_parameter_ranges` and already
        set parameters in `_optimal_parameters`
        """
        new_ranges = self._fix_ranges_for_already_set_parameters()

        _, k, _ = self.problem.get_parameters()
        k1 = k//2
        for p in range(new_ranges["p"]["min"], min(k1, new_ranges["p"]["max"])+1, 2):
            L1 = binom(k1, p)
            l_val = int(log2(L1))
            l_search_radius = self._adjust_radius
            for l in range(max(new_ranges["l"]["min"], l_val-l_search_radius), min(new_ranges["l"]["max"], l_val+l_search_radius)+1):
                indices = {"p": p, "l": l, "r": self._optimal_parameters["r"]}
                if self._are_parameters_invalid(indices):
                    continue
                yield indices

    def _time_and_memory_complexity(self, parameters: dict, verbose_information=None):
        """
        Return time complexity of Sterns's algorithm for given set of parameters

        INPUT:
        -  ``parameters`` -- dictionary including parameters
        -  ``verbose_information`` -- if set to a dictionary `permutations` and `gauß` will be returned.
        """
        n, k, w = self.problem.get_parameters()
        par = SimpleNamespace(**parameters)
        k1 = k // 2

        memory_bound = self.problem.memory_bound

        L1 = binom(k1, par.p)
        if self._is_early_abort_possible(log2(L1)):
            return inf, inf

        memory = log2(2 * L1 + _mem_matrix(n, k, par.r))
        solutions = self.problem.nsolutions

        if memory > memory_bound:
            return inf, memory_bound + 1

        Tp = max(0, log2(binom(n, w)) - log2(binom(n - k, w - 2 * par.p)
                                             ) - log2(binom(k1, par.p) ** 2) - solutions)

        # We use Indyk-Motwani (IM) taking into account the possibility of multiple existing solutions
        # with correct weight distribution, decreasing the amount of necessary projections
        # remaining_sol denotes the number of expected solutions per permutation
        # l_part_iterations is the expected number of projections need by IM to find one of those solutions

        remaining_sol = (binom(n - k, w - 2 * par.p) * binom(k1, par.p) ** 2 * binom(n, w) // 2 ** (
            n - k)) // binom(n,
                             w)
        l_part_iterations = binom(
            n - k, w - 2 * par.p) // binom(n - k - par.l, w - 2 * par.p)

        if remaining_sol > 0:
            l_part_iterations //= max(1, remaining_sol)
            l_part_iterations = max(1, l_part_iterations)

        Tg = _gaussian_elimination_complexity(n, k, par.r)
        time = Tp + log2(Tg + _list_merge_complexity(L1,
                         par.l, self._hmap) * l_part_iterations)

        if verbose_information is not None:
            verbose_information[VerboseInformation.PERMUTATIONS.value] = Tp
            verbose_information[VerboseInformation.GAUSS.value] = log2(Tg)
            verbose_information[VerboseInformation.LISTS.value] = [
                log2(L1), 2 * log2(L1) - par.l]

        return time, memory

    def __repr__(self):
        rep = "Stern estimator for " + str(self.problem)
        return rep
