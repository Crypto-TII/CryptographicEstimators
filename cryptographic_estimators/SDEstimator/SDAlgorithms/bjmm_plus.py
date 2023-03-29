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
    binom, log2, ceil, inf, _list_merge_async_complexity
from types import SimpleNamespace
from ..sd_constants import *


class BJMM_plus(SDAlgorithm):
    def __init__(self, problem: SDProblem, **kwargs):
        """
        Complexity estimate of BJMM+ algorithm in depth 2

        This class incorporates the improvements by [EZ23]_, regarding a time-memory tradeoff which improves over the
        BJMM algorithm in terms of memory usages.

        For further reference see [MMT11]_ and [BJMM12]_.

        expected weight distribution::

            +--------------------------+-------------------+-------------------+
            | <-----+ n - k - l +----->|<--+ (k + l)/2 +-->|<--+ (k + l)/2 +-->|
            |           w - 2p         |        p          |        p          |
            +--------------------------+-------------------+-------------------+

        INPUT:

        - ``problem`` -- SDProblem object including all necessary parameters

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import BJMM_plus
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: BJMM_plus(SDProblem(n=100,k=50,w=10))
            BJMM+ estimator for syndrome decoding problem with (n,k,w) = (100,50,10) over Finite Field of size 2

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import BJMM_plus
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: BJMM_plus(SDProblem(n=1284,k=1028,w=24)).time_complexity()
            66.34605703336426
 
            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import BJMM_plus
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: BJMM_plus(SDProblem(3488,2720,64)).time_complexity()
            142.1110119263271

        """

        super(BJMM_plus, self).__init__(problem, **kwargs)
        self._name = "BJMM"
        self.initialize_parameter_ranges()
        self.limit_depth = kwargs.get("limit_depth", False)
        self.qc = False


    def initialize_parameter_ranges(self):
        """
        initialize the parameter ranges for p, p1, l to start the optimisation
        process.
        """
        n, k, w = self.problem.get_parameters()
        s = self.full_domain
        self.set_parameter_ranges("p", 0, min_max(35, w, s))
        self.set_parameter_ranges("p1", 0, min_max(35, w, s))
        self.set_parameter_ranges("l", 0, min_max(500, n - k, s))
        self.set_parameter_ranges("l1", 0, min_max(200, n - k, s))

    @optimal_parameter
    def l(self):
        """
        Return the optimal parameter $l$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import BJMM_plus
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = BJMM_plus(SDProblem(n=100,k=50,w=10))
            sage: A.l()
            8

        """
        return self._get_optimal_parameter("l")

    @optimal_parameter
    def l1(self):
        """
        Return the optimal parameter $l$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import BJMM_plus
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = BJMM_plus(SDProblem(n=100,k=50,w=10))
            sage: A.l1()
            2

        """
        return self._get_optimal_parameter("l1")

    @optimal_parameter
    def p(self):
        """
        Return the optimal parameter $p$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import BJMM_plus
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = BJMM_plus(SDProblem(n=100,k=50,w=10))
            sage: A.p()
            2
        """
        return self._get_optimal_parameter("p")

    @optimal_parameter
    def p1(self):
        """
        Return the optimal parameter $p1$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import BJMM_plus
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = BJMM_plus(SDProblem(n=100,k=50,w=10))
            sage: A.p1()
            1
        """
        return self._get_optimal_parameter("p1")

    def _are_parameters_invalid(self, parameters: dict):
        """
        return if the parameter set `parameters` is invalid

        """
        n, k, w = self.problem.get_parameters()
        par = SimpleNamespace(**parameters)
        k1 = (k + par.l) // 2
        if par.p > w // 2 or \
            k1 < par.p or \
            par.l >= n - k or\
            n - k - par.l < w - 2 * par.p or \
            k1 - par.p < par.p1 - par.p / 2 or \
            par.p1 < par.p / 2:
            return True
        return False

    def _valid_choices(self):
        """
        Generator which yields on each call a new set of valid parameters based on the `_parameter_ranges` and already
        set parameters in `_optimal_parameters`
        """
        new_ranges = self._fix_ranges_for_already_set_parameters()

        n, k, w = self.problem.get_parameters()

        for p in range(new_ranges["p"]["min"], min(w // 2, new_ranges["p"]["max"]), 2):
            for l in range(new_ranges["l"]["min"], min(n - k - (w - 2 * p), new_ranges["l"]["max"])):
                for p1 in range(max(new_ranges["p1"]["min"], (p + 1) // 2), new_ranges["p1"]["max"]):
                    L1 = int(log2(binom((k+l)//2, p1)))
                    d1 = self._adjust_radius
                    for l1 in range(max(L1-d1, 0), L1+d1):
                        indices = {"p": p, "p1": p1, "l": l, "l1": l1,
                                   "r": self._optimal_parameters["r"]}
                        if self._are_parameters_invalid(indices):
                            continue
                        yield indices

    def _time_and_memory_complexity(self, parameters: dict, verbose_information=None):
        """
        computes the expected runtime and memory consumption for the depth 2 version

        """
        n, k, w = self.problem.get_parameters()
        par = SimpleNamespace(**parameters)
        k1 = (k + par.l) // 2

        if self._are_parameters_invalid(parameters):
            return inf, inf

        solutions = self.problem.nsolutions
        memory_bound = self.problem.memory_bound

        L1 = binom(k1, par.p1)
        if self._is_early_abort_possible(log2(L1)):
            return inf, inf

        if self.qc:
            L1b = binom(k1, par.p1 - 1) * k

        if not self.qc:
            reps = (binom(par.p, par.p // 2) * binom(k1 - par.p, par.p1 - par.p // 2)) ** 2
        else:
            reps = binom(par.p, par.p // 2) * binom(k1 - par.p, par.p1 - par.p // 2) * binom(k1 - par.p + 1, par.p1 - par.p // 2)

        L12 = max(1, L1 ** 2 // 2 ** par.l1)

        qc_advantage = 0
        if self.qc:
            L12b = max(1, L1 * L1b // 2 ** par.l1)
            qc_advantage = log2(k)

        memory = log2((2 * L1 + L12) + _mem_matrix(n, k, par.r)) if not self.qc else\
                  log2(L1 + L1b + min(L12, L12b) + _mem_matrix(n, k, par.r))
        if self._is_early_abort_possible(memory):
            return inf, inf

        Tp = max(log2(binom(n, w))
                 - log2(binom(n - k - par.l, w - 2 * par.p + self.qc))
                 - log2(binom(k1, par.p))
                 - log2(binom(k1, par.p - self.qc))
                 - qc_advantage - solutions, 0)

        Tg = _gaussian_elimination_complexity(n, k, par.r)
        if not self.qc:
            T_tree = 2 * _list_merge_complexity(L1, par.l1, self._hmap) +\
                         _list_merge_complexity(L12, par.l - par.l1, self._hmap)
        else:
            T_tree = _list_merge_async_complexity(L1, L1b, par.l1, self._hmap) +\
                     _list_merge_complexity(L1, par.l1, self._hmap) +\
                     _list_merge_async_complexity(L12, L12b, self._hmap)
        T_rep = int(ceil(2 ** (par.l1 - log2(reps))))
        time = Tp + log2(Tg + T_rep * T_tree)

        if verbose_information is not None:
            verbose_information[VerboseInformation.CONSTRAINTS.value] = [par.l1, par.l - par.l1]
            verbose_information[VerboseInformation.PERMUTATIONS.value] = Tp
            verbose_information[VerboseInformation.TREE.value] = log2(T_rep * T_tree)
            verbose_information[VerboseInformation.GAUSS.value] = log2(Tg)
            verbose_information[VerboseInformation.REPRESENTATIONS.value] = reps
            verbose_information[VerboseInformation.LISTS.value] = [
                log2(L1), log2(L12), 2 * log2(L12) - (par.l - par.l1)]

        return time, memory

    def __repr__(self):
        rep = "BJMM+ estimator for " + str(self.problem)
        return rep
