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
from ...SDEstimator.sd_helper import _gaussian_elimination_complexity, _mem_matrix, _list_merge_complexity, \
    _mitm_nn_complexity, binom, log2, ceil, inf, min_max
from scipy.special import binom as binom_sp
from scipy.optimize import fsolve
from warnings import filterwarnings
from types import SimpleNamespace
from ..sd_constants import *

filterwarnings("ignore", category=RuntimeWarning)


class BJMMpdw(SDAlgorithm):
    def __init__(self, problem: SDProblem, **kwargs):
        """
         Construct an instance of BJMM's estimator in depth 2 using partially disjoint
         weight, applying explicit MitM-NN search on second level [MMT11]_,
         [BJMM12]_, [EB22]_.

         Expected weight distribution::

             +--------------------------+--------------------+--------------------+--------+--------+
             | <-+ n - k - l1 - 2 l2 +->|<-+ (k + l1) / 2 +->|<-+ (k + l1) / 2 +->|   l2   |   l2   |
             |       w - 2 p - 2 w2     |         p          |         p          |   w2   |   w2   |
             +--------------------------+--------------------+--------------------+--------+--------+


         INPUT:

        - ``problem`` -- SDProblem object including all necessary parameters

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import BJMMpdw
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: BJMMpdw(SDProblem(n=100,k=50,w=10))
            BJMM estimator with partially disjoint weight distributions in depth 2 for syndrome decoding problem with (n,k,w) = (100,50,10) over Finite Field of size 2

        """
        super(BJMMpdw, self).__init__(problem, **kwargs)
        self._name = "BJMM-pdw"
        self.initialize_parameter_ranges()

    def initialize_parameter_ranges(self):
        """
        initialize the parameter ranges for p, p1, w2 to start the optimisation 
        process.
        """
        _, _, w = self.problem.get_parameters()
        s = self.full_domain
        self.set_parameter_ranges("p", 0, min_max(30, w, s))
        self.set_parameter_ranges("p1", 0, min_max(25, w, s))
        self.set_parameter_ranges("w2", 0, min_max(5, w, s))

    @optimal_parameter
    def p(self):
        """
        Return the optimal parameter $p$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import BJMMpdw
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = BJMMpdw(SDProblem(n=100,k=50,w=10))
            sage: A.p()
            2
        """
        return self._get_optimal_parameter("p")

    @optimal_parameter
    def p1(self):
        """
        Return the optimal parameter $p1$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import BJMMpdw
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = BJMMpdw(SDProblem(n=100,k=50,w=10))
            sage: A.p1()
            1
        """
        return self._get_optimal_parameter("p1")

    @optimal_parameter
    def w2(self):
        """
        Return the optimal parameter $w2$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import BJMMdw
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = BJMMdw(SDProblem(n=100,k=50,w=10))
            sage: A.w2()
            0
        """
        return self._get_optimal_parameter("w2")

    def _are_parameters_invalid(self, parameters: dict):
        """
        return if the parameter set `parameters` is invalid

        """
        _, k, w = self.problem.get_parameters()
        par = SimpleNamespace(**parameters)

        if par.p % 2 == 1 or par.p > w // 2 or k < par.p or \
                par.p1 < par.p // 2 or par.p1 > w or \
                par.w2 > w // 2 - par.p:
            return True
        return False

    def _valid_choices(self):
        """
        Generator which yields on each call a new set of valid parameters based on the `_parameter_ranges` and already
        set parameters in `_optimal_parameters`

        """
        new_ranges = self._fix_ranges_for_already_set_parameters()
        _, _, w = self.problem.get_parameters()

        for p in range(new_ranges["p"]["min"], min(w // 2, new_ranges["p"]["max"]) + 1, 2):
            for p1 in range(max(new_ranges["p1"]["min"], (p + 1) // 2), min(w, new_ranges["p1"]["max"]) + 1):
                for w2 in range(new_ranges["w2"]["min"], min(w - p1, new_ranges["w2"]["max"]) + 1):
                    indices = {"p": p, "p1": p1, "w2": w2,
                               "r": self._optimal_parameters["r"]}
                    if self._are_parameters_invalid(indices):
                        continue
                    yield indices

    def _choose_first_constraint_such_that_representations_cancel_out_exactly(self, parameters: dict):
        """
        tries to find an optimal l1 value fulfilling its contraints
        """
        _, k, _ = self.problem.get_parameters()
        par = SimpleNamespace(**parameters)

        try:
            def f(x): return log2((binom(par.p, par.p // 2) *
                                   binom_sp((k + x) / 2 - par.p, par.p1 - par.p // 2))) * 2 - x
            l1_val = int(fsolve(f, 0)[0])

            if f(l1_val) < 0 or f(l1_val) > 1:
                return -1
        except ValueError:
            return -1

        return l1_val

    def _choose_second_constraint_such_that_list_size_remains_constant(self, parameters: dict, list_size: float):
        """
        tries to find an optimal l2 value fulfilling its contraints
        """
        par = SimpleNamespace(**parameters)

        try:
            def f(x): return log2(list_size) + 2 * \
                log2(binom_sp(x, par.w2)) - 2 * x
            l2_val = int(fsolve(f, 0)[0])
            if f(l2_val) < 0 or f(l2_val) > 1:
                return -1
        except ValueError:
            return -1

        return l2_val

    def _time_and_memory_complexity(self, parameters: dict, verbose_information=None):
        """
        Computes the expected runtime and memory consumption for a given parameter set.
        """
        n, k, w = self.problem.get_parameters()
        par = SimpleNamespace(**parameters)
        if len(parameters.keys()) == 1:
            return inf, inf

        local_time, local_mem = inf, inf
        solutions = self.problem.nsolutions
        memory_bound = self.problem.memory_bound
        l1_search_radius = max(1, self._adjust_radius // 2)
        l2_search_radius = max(1, self._adjust_radius // 2)

        l1_start_value = self._choose_first_constraint_such_that_representations_cancel_out_exactly(
            parameters)
        if l1_start_value == -1:
            return inf, inf

        for l1 in range(max(0, l1_start_value - l1_search_radius), l1_start_value + l1_search_radius):
            if 2*l1 >= n-k or n-k-2*l1 < w:
                continue

            k1 = (k + l1) // 2

            if k1 - par.p < 0 or k1 - par.p < par.p1 - par.p // 2:
                continue
            reps = (binom(par.p, par.p // 2) *
                    binom(k1 - par.p, par.p1 - par.p // 2)) ** 2

            L1 = binom(k1, par.p1)
            if self._is_early_abort_possible(log2(L1)):
                return inf, inf

            L12 = max(L1 ** 2 // 2 ** l1, 1)

            memory = log2((2 * L1 + L12) + _mem_matrix(n, k, par.r))
            if memory > memory_bound:
                continue

            l2_start_value = self._choose_second_constraint_such_that_list_size_remains_constant(
                parameters, L12)
            if l2_start_value == -1:
                continue

            l2_min, l2_max = par.w2, (n - k - l1 -
                                      (w - 2 * par.p - 2 * par.w2)) // 2
            l2_range = [l2_start_value - l2_search_radius,
                        l2_start_value + l2_search_radius]
            for l2 in range(max(l2_min, l2_range[0]), min(l2_max, l2_range[1])):
                Tp = max(
                    log2(binom(n, w)) - log2(binom(n - k - l1 - 2 * l2, w - 2 * par.p - 2 * par.w2)) - 2 * log2(
                        binom(k1, par.p)) - 2 * log2(binom(l2, par.w2)) - solutions, 0)
                Tg = _gaussian_elimination_complexity(n, k, par.r)

                T_tree = 2 * _list_merge_complexity(L1, l1, self._hmap) + _mitm_nn_complexity(L12, 2 * l2, 2 * par.w2,
                                                                                              self._hmap)
                T_rep = int(ceil(2 ** max(l1 - log2(reps), 0)))

                time = Tp + log2(Tg + T_rep * T_tree)
                if time < local_time:
                    local_time = time
                    local_mem = memory
                    if verbose_information is not None:
                        verbose_information[VerboseInformation.CONSTRAINTS.value] = [
                            l1, 2 * l2]
                        verbose_information[VerboseInformation.PERMUTATIONS.value] = Tp
                        verbose_information[VerboseInformation.TREE.value] = log2(
                            T_rep * T_tree)
                        verbose_information[VerboseInformation.GAUSS.value] = log2(
                            Tg)
                        verbose_information[VerboseInformation.REPRESENTATIONS.value] = reps
                        verbose_information[VerboseInformation.LISTS.value] = [
                            log2(L1), log2(L12), 2 * log2(L12)]

        return local_time, local_mem

    def __repr__(self):
        """
        """
        rep = "BJMM estimator with partially disjoint weight distributions in depth 2 for " + \
            str(self.problem)
        return rep
