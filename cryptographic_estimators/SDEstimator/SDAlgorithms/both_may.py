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
from ...SDEstimator.sd_helper import _gaussian_elimination_complexity, _mem_matrix, _indyk_motwani_complexity, binom, \
    log2, inf, ceil
from types import SimpleNamespace
from ..sd_constants import *
from ..SDWorkfactorModels import BothMayScipyModel


class BothMay(SDAlgorithm):
    def __init__(self, problem: SDProblem, **kwargs):
        """
        Complexity estimate of Both-May algorithm in depth 2 using Indyk-Motwani and / or MitM for NN search


        For further reference see [BM18]_.

            +-------------------+---------+-------------------+-------------------+
            | <--+ n - k - l+-->|<-+ l +->|<----+ k / 2 +---->|<----+ k / 2 +---->|
            |     w - w2 - 2p   |    w2   |         p         |         p         |
            +-------------------+---------+-------------------+-------------------+

        INPUT:

        - ``problem`` -- SDProblem object including all necessary parameters

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import BothMay
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: BothMay(SDProblem(n=100,k=50,w=10))
            Both-May estimator in depth 2 for syndrome decoding problem with (n,k,w) = (100,50,10) over Finite Field of size 2

        """
        super(BothMay, self).__init__(problem, **kwargs)
        self._name = "Both-May"
        self.initialize_parameter_ranges()
        self.scipy_model = BothMayScipyModel

    def initialize_parameter_ranges(self):
        """
        initialize the parameter ranges for p, p1, p2, l to start the optimisation 
        process.
        """
        self.set_parameter_ranges("p", 0, 20)
        self.set_parameter_ranges("p1", 0, 15)
        self.set_parameter_ranges("l", 0, 160)
        self.set_parameter_ranges("w1", 0, 5)
        self.set_parameter_ranges("w2", 0, 4)

    @optimal_parameter
    def l(self):
        """
        Return the optimal parameter $l$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import BothMay
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = BothMay(SDProblem(n=100,k=50,w=10))
            sage: A.l()
            2
        """
        return self._get_optimal_parameter("l")

    @optimal_parameter
    def p(self):
        """
        Return the optimal parameter $p$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import BothMay
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = BothMay(SDProblem(n=100,k=50,w=10))
            sage: A.p()
            2
        """
        return self._get_optimal_parameter("p")

    @optimal_parameter
    def p1(self):
        """
        Return the optimal parameter $p1$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import BothMay
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = BothMay(SDProblem(n=100,k=50,w=10))
            sage: A.p1()
            1
        """
        return self._get_optimal_parameter("p1")

    @optimal_parameter
    def w1(self):
        """
        Return the optimal parameter $w1$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import BothMay
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = BothMay(SDProblem(n=100,k=50,w=10))
            sage: A.w1()
            0
        """
        return self._get_optimal_parameter("w1")

    @optimal_parameter
    def w2(self):
        """
        Return the optimal parameter $w2$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import BothMay
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = BothMay(SDProblem(n=100,k=50,w=10))
            sage: A.w2()
            0
        """
        return self._get_optimal_parameter("w2")

    def _are_parameters_invalid(self, parameters: dict):
        """
        return if the parameter set `parameters` is invalid

        """
        n, k, w = self.problem.get_parameters()
        par = SimpleNamespace(**parameters)
        k1 = k // 2
        if par.p > w // 2 or k1 < par.p or par.w1 >= min(w, par.l + 1) \
                or par.w2 > min(w - 2 * par.p, par.l, 2 * par.w1) or par.p1 < (par.p + 1) // 2 or par.p1 > w \
                or n - k - par.l < w - par.w2 - 2 * par.p or par.p1 > k1:
            return True
        return False

    def _valid_choices(self):
        """
        Generator which yields on each call a new set of valid parameters based on the `_parameter_ranges` and already
        set parameters in `_optimal_parameters`

        """
        new_ranges = self._fix_ranges_for_already_set_parameters()
        n, k, w = self.problem.get_parameters()

        for p in range(new_ranges["p"]["min"], min(w // 2, new_ranges["p"]["max"])+1, 2):
            for l in range(new_ranges["l"]["min"], min(n - k - (w - 2 * p), new_ranges["l"]["max"])+1):
                for w1 in range(new_ranges["w1"]["min"], new_ranges["w1"]["max"]+1):
                    for w2 in range(new_ranges["w2"]["min"], new_ranges["w2"]["max"]+1, 2):
                        for p1 in range(max(new_ranges["p1"]["min"], (p + 1) // 2), new_ranges["p1"]["max"]+1):
                            indices = {"p": p, "w1": w1, "w2": w2, "p1": p1,
                                       "l": l, "r": self._optimal_parameters["r"]}
                            if self._are_parameters_invalid(indices):
                                continue
                            yield indices

    def _time_and_memory_complexity(self, parameters: dict, verbose_information=None):
        """
        Computes the expected runtime and memory consumption for a given parameter set.
        """
        n, k, w = self.problem.get_parameters()
        par = SimpleNamespace(**parameters)
        k1 = k // 2

        solutions = self.problem.nsolutions
        memory_bound = self.problem.memory_bound

        reps = (binom(par.p, par.p / 2) * binom(k1 - par.p, par.p1 - par.p / 2)) ** 2 * binom(par.w2, par.w2 / 2) \
            * binom(par.l - par.w2, par.w1 - par.w2 / 2)
        reps = 1 if reps == 0 else reps
        L1 = binom(k1, par.p1)

        if self._is_early_abort_possible(log2(L1)):
            return inf, inf

        L12 = max(1, L1 ** 2 * binom(par.l, par.w1) // 2 ** par.l)

        memory = log2((2 * L1 + L12) + _mem_matrix(n, k, par.r))
        if memory > memory_bound:
            return inf, inf

        Tp = max(
            log2(binom(n, w)) - log2(binom(n - k - par.l, w - par.w2 - 2 * par.p)) - 2 * log2(binom(k1, par.p)) - log2(
                binom(par.l, par.w2)) - solutions, 0)
        Tg = _gaussian_elimination_complexity(n, k, par.r)

        first_level_nn = _indyk_motwani_complexity(
            L1, par.l, par.w1, self._hmap)
        second_level_nn = _indyk_motwani_complexity(
            L12, n - k - par.l, w - 2 * par.p - par.w2, self._hmap)
        T_tree = 2 * first_level_nn + second_level_nn
        T_rep = int(ceil(2 ** max(0, par.l - log2(reps))))

        time = Tp + log2(Tg + T_rep * T_tree)
        if verbose_information is not None:
            verbose_information[VerboseInformation.CONSTRAINTS.value] = [par.l]
            verbose_information[VerboseInformation.PERMUTATIONS.value] = Tp
            verbose_information[VerboseInformation.TREE.value] = log2(
                T_rep * T_tree)
            verbose_information[VerboseInformation.GAUSS.value] = log2(Tg)
            verbose_information[VerboseInformation.REPRESENTATIONS.value] = reps
            verbose_information[VerboseInformation.LISTS.value] = [
                log2(L1), log2(L12)]

        return time, memory

    def __repr__(self):
        """
        """
        rep = "Both-May estimator in depth 2 for " + str(self.problem)
        return rep
