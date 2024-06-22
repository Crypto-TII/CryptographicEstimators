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
from ...helper import ComplexityType
from ...SDEstimator.sd_algorithm import SDAlgorithm
from ...SDEstimator.sd_problem import SDProblem
from ...SDEstimator.sd_helper import _gaussian_elimination_complexity, _mem_matrix, _list_merge_complexity, \
    _indyk_motwani_complexity, min_max, binom, log2, ceil, inf
from types import SimpleNamespace
from ..sd_constants import *
from ..SDWorkfactorModels.may_ozerov import MayOzerovScipyModel
from typing import Union


class MayOzerov(SDAlgorithm):
    def __init__(self, problem: SDProblem, **kwargs):
        """
        Complexity estimate of May-Ozerov algorithm in depth 2 and 3

        Introduced in [MO15]_.

        expected weight distribution::

            +--------------------------+-------------------+-------------------+
            | <-----+ n - k - l +----->|<--+ (k + l)/2 +-->|<--+ (k + l)/2 +-->|
            |           w - 2p         |        p          |        p          |
            +--------------------------+-------------------+-------------------+
        INPUT:

        - ``problem`` -- SDProblem object including all necessary parameters

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import MayOzerov
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: MayOzerov(SDProblem(n=100,k=50,w=10))
            May-Ozerov estimator for syndrome decoding problem with (n,k,w) = (100,50,10) over Finite Field of size 2
        """
        super(MayOzerov, self).__init__(problem, **kwargs)
        self._name = "May-Ozerov"
        self.initialize_parameter_ranges()
        self.limit_depth = kwargs.get("limit_depth", False)
        self.MayOzerov_depth_2 = MayOzerovD2(problem, **kwargs)
        self.MayOzerov_depth_3 = MayOzerovD3(problem, **kwargs)

    def initialize_parameter_ranges(self):
        self.set_parameter_ranges("depth", 2, 3)

    @optimal_parameter
    def depth(self):
        """
        Return the optimal parameter $depth$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import BJMM
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = BJMM(SDProblem(n=100,k=50,w=10))
            sage: A.depth()
            2
        """
        if self.complexity_type == ComplexityType.TILDEO.value:
            return 3
        return self._get_optimal_parameter("depth")

    @property
    def complexity_type(self):
        """
        returns the optimization type (bit security or asymptotic)
        """
        return super().complexity_type

    @complexity_type.setter
    def complexity_type(self, new_type: Union[str, int]):
        """
        sets the complexity type.
        """
        super(MayOzerov, self.__class__).complexity_type.fset(self, new_type)
        self.MayOzerov_depth_2.complexity_type = new_type
        self.MayOzerov_depth_3.complexity_type = new_type

    def reset(self):
        """
        resets all internal variables to restart the optimization process
        """
        super().reset()
        self.MayOzerov_depth_2.reset()
        self.MayOzerov_depth_3.reset()

    def _find_optimal_parameters(self):
        """
        Finds optimal parameters for depth 2 and 3
        """
        self.MayOzerov_depth_2._find_optimal_parameters()
        if self.limit_depth:
            self._optimal_parameters["depth"] = 2
            return

        self.MayOzerov_depth_3._find_optimal_parameters()
        if self.MayOzerov_depth_2.time_complexity() > self.MayOzerov_depth_3.time_complexity():
            self._optimal_parameters["depth"] = 3
        else:
            self._optimal_parameters["depth"] = 2

    def _time_and_memory_complexity(self, parameters: dict, verbose_information=None):
        """
        computes and returns the time and memory complexity for either the depth 2 or 3 algorithm
        """
        if "depth" not in parameters:
            raise ValueError("Depth must be specified for BJMM")

        if parameters["depth"] == 2 and self.MayOzerov_depth_2._do_valid_parameters_in_current_ranges_exist():
            return self.MayOzerov_depth_2._time_and_memory_complexity(
                self.MayOzerov_depth_2.optimal_parameters(), verbose_information)
        elif parameters["depth"] == 3 and self.MayOzerov_depth_3._do_valid_parameters_in_current_ranges_exist():
            return self.MayOzerov_depth_3._time_and_memory_complexity(
                self.MayOzerov_depth_3.optimal_parameters(), verbose_information)
        elif parameters["depth"] not in [2, 3]:
            raise ValueError("BJMM only implemented in depth 2 and 3")
        else:
            return inf, inf

    def get_optimal_parameters_dict(self):
        """
        Returns the optimal parameters dictionary

        """
        a = dict()
        a.update(self._optimal_parameters)
        if self.depth() == 2:
            a.update(self.MayOzerov_depth_2.get_optimal_parameters_dict())
        else:
            a.update(self.MayOzerov_depth_3.get_optimal_parameters_dict())
        return a

    def _tilde_o_time_and_memory_complexity(self, parameters: dict):
        """
        computes the time and memory complexity for the depth 3 algorithm
        """
        return self.MayOzerov_depth_3._tilde_o_time_and_memory_complexity(parameters)

    def __repr__(self):
        """
        """
        rep = "May-Ozerov estimator for " + str(self.problem)
        return rep


class MayOzerovD2(SDAlgorithm):
    def __init__(self, problem: SDProblem, **kwargs):
        """
        Complexity estimate of May-Ozerov algorithm in depth 2.

        [MO15] May, A., Ozerov, I.: On computing nearest neighbors with applications to decoding of binary linear codes.
        In: Annual International Conference on the Theory and Applications of Cryptographic Techniques. pp. 203-228 . Springer (2015)

        expected weight distribution::

            +--------------------------+-------------------+-------------------+
            | <-----+ n - k - l +----->|<--+ (k + l)/2 +-->|<--+ (k + l)/2 +-->|
            |           w - 2p         |        p          |        p          |
            +--------------------------+-------------------+-------------------+
        INPUT:

        - ``problem`` -- SDProblem object including all necessary parameters

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import MayOzerov
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = MayOzerov(SDProblem(n=100,k=50,w=10))
            sage: A.MayOzerov_depth_2
            May-Ozerov estimator in depth 2 for syndrome decoding problem with (n,k,w) = (100,50,10) over Finite Field of size 2
        """
        super(MayOzerovD2, self).__init__(problem, **kwargs)
        self._name = "May-OzerovD2"
        self.initialize_parameter_ranges()

    def initialize_parameter_ranges(self):
        """
        initialize the parameters p, l, p1
        """
        n, k, w = self.problem.get_parameters()
        s = self.full_domain
        self.set_parameter_ranges("p", 0, min_max(30, w // 2, s))
        self.set_parameter_ranges("l", 0, min_max(300, n - k, s))
        self.set_parameter_ranges("p1", 0, min_max(25, w // 2, s))

    @optimal_parameter
    def l(self):
        """
        Return the optimal parameter $l$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import MayOzerov
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = MayOzerov(SDProblem(n=100,k=50,w=10))
            sage: A.MayOzerov_depth_2.l()
            2
        """
        return self._get_optimal_parameter("l")

    @optimal_parameter
    def p(self):
        """
        Return the optimal parameter $p$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import MayOzerov
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = MayOzerov(SDProblem(n=100,k=50,w=10))
            sage: A.MayOzerov_depth_2.p()
            2
        """
        return self._get_optimal_parameter("p")

    @optimal_parameter
    def p1(self):
        """
        Return the optimal parameter $p1$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import MayOzerov
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = MayOzerov(SDProblem(n=100,k=50,w=10))
            sage: A.MayOzerov_depth_2.p1()
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
        if par.l >= n - k - (w - 2 * par.p) or par.p1 < (
                par.p + 1) // 2 or par.p > w // 2 or k1 < par.p or k1 - par.p < par.p1 - par.p / 2 or par.p1 < par.p // 2:
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
                for p1 in range(max(new_ranges["p1"]["min"], (p + 1) // 2), new_ranges["p1"]["max"]+1):
                    indices = {"p": p, "p1": p1, "l": l,
                               "r": self._optimal_parameters["r"]}
                    if self._are_parameters_invalid(indices):
                        continue
                    yield indices

    def _time_and_memory_complexity(self, parameters: dict, verbose_information=None):
        """
        Computes the expected runtime and memory consumption.

        """
        n, k, w = self.problem.get_parameters()
        par = SimpleNamespace(**parameters)
        k1 = (k + par.l) // 2

        solutions = self.problem.nsolutions
        memory_bound = self.problem.memory_bound
        L1 = binom(k1, par.p1)

        if self._is_early_abort_possible(log2(L1)):
            return inf, inf

        reps = (binom(par.p, par.p // 2) *
                binom(k1 - par.p, par.p1 - par.p // 2)) ** 2

        if log2(reps) > par.l + 1:
            return inf, inf

        L12 = max(1, L1 ** 2 // 2 ** par.l)

        memory = log2((2 * L1 + L12) + _mem_matrix(n, k, par.r))
        if memory > memory_bound:
            return inf, inf

        Tp = max(
            log2(binom(n, w)) - log2(binom(n - k - par.l, w - 2 * par.p)) - 2 * log2(binom(k1, par.p)) - solutions, 0)
        Tg = _gaussian_elimination_complexity(n, k, par.r)
        T_tree = 2 * _list_merge_complexity(L1, par.l, self._hmap) + _indyk_motwani_complexity(L12, n - k - par.l,
                                                                                               w - 2 * par.p,
                                                                                               self._hmap)

        T_rep = int(ceil(2 ** max(par.l - log2(reps), 0)))
        time = Tp + log2(Tg + T_rep * T_tree)

        if verbose_information is not None:
            verbose_information[VerboseInformation.CONSTRAINTS.value] = [par.l]
            verbose_information[VerboseInformation.PERMUTATIONS.value] = Tp
            verbose_information[VerboseInformation.TREE.value] = log2(
                T_rep * T_tree)
            verbose_information[VerboseInformation.GAUSS.value] = log2(Tg)
            verbose_information[VerboseInformation.REPRESENTATIONS.value] = reps
            verbose_information[VerboseInformation.LISTS.value] = [log2(L1), log2(L12),
                                                                   2 * log2(L12) + log2(
                                                                       binom(n - k - par.l, w - 2 * par.p)) - (
                n - par.l)]

        return time, memory

    def __repr__(self):
        """
        """
        rep = "May-Ozerov estimator in depth 2 for " + str(self.problem)
        return rep


class MayOzerovD3(SDAlgorithm):
    def __init__(self, problem: SDProblem, **kwargs):
        """
        Complexity estimate of May-Ozerov algorithm in depth 3.

        [MO15] May, A., Ozerov, I.: On computing nearest neighbors with applications to decoding of binary linear codes.
        In: Annual International Conference on the Theory and Applications of Cryptographic Techniques. pp. 203-228 . Springer (2015)

        expected weight distribution::

            +--------------------------+-------------------+-------------------+
            | <-----+ n - k - l +----->|<--+ (k + l)/2 +-->|<--+ (k + l)/2 +-->|
            |           w - 2p         |        p          |        p          |
            +--------------------------+-------------------+-------------------+
        INPUT:

        - ``problem`` -- SDProblem object including all necessary parameters

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import MayOzerov
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = MayOzerov(SDProblem(n=100,k=50,w=10))
            sage: A.MayOzerov_depth_3
            May-Ozerov estimator in depth 3 for syndrome decoding problem with (n,k,w) = (100,50,10) over Finite Field of size 2
        """
        super(MayOzerovD3, self).__init__(problem, **kwargs)
        self._name = "May-OzerovD3"
        self.initialize_parameter_ranges()
        self.scipy_model = MayOzerovScipyModel

    def initialize_parameter_ranges(self):
        """
        initialize the parameter ranges for p, p1, p2, l to start the optimisation 
        process.
        """
        n, k, w = self.problem.get_parameters()
        s = self.full_domain
        self.set_parameter_ranges("p", 0, min_max(20, w // 2, s))
        self.set_parameter_ranges("l", 0, min_max(200, n - k, s))
        self.set_parameter_ranges("p2", 0, min_max(20, w // 2, s))
        self.set_parameter_ranges("p1", 0, min_max(10, w // 2, s))

    @optimal_parameter
    def l(self):
        """
        Return the optimal parameter $l$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import MayOzerov
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = MayOzerov(SDProblem(n=100,k=50,w=10))
            sage: A.MayOzerov_depth_3.l()
            11
        """
        return self._get_optimal_parameter("l")

    @optimal_parameter
    def p(self):
        """
        Return the optimal parameter $p$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import MayOzerov
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = MayOzerov(SDProblem(n=100,k=50,w=10))
            sage: A.MayOzerov_depth_3.p()
            2
        """
        return self._get_optimal_parameter("p")

    @optimal_parameter
    def p1(self):
        """
        Return the optimal parameter $p1$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import MayOzerov
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = MayOzerov(SDProblem(n=100,k=50,w=10))
            sage: A.MayOzerov_depth_3.p1()
            1
        """
        return self._get_optimal_parameter("p1")

    @optimal_parameter
    def p2(self):
        """
        Return the optimal parameter $p2$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import MayOzerov
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = MayOzerov(SDProblem(n=100,k=50,w=10))
            sage: A.MayOzerov_depth_3.p2()
            2
        """
        return self._get_optimal_parameter("p2")

    def _are_parameters_invalid(self, parameters: dict):
        """
        return if the parameter set `parameters` is invalid

        """
        n, k, w = self.problem.get_parameters()
        par = SimpleNamespace(**parameters)
        k1 = (k + par.l) // 2
        if par.p > w // 2 or k1 < par.p or par.l > n - k or n - k - par.l < w - 2 * par.p or \
                k1 - par.p < par.p2 - par.p / 2 or par.p2 < par.p / 2 or 2 * par.p > w or \
                k1 - par.p2 < par.p1 - par.p2 / 2 or par.p1 < par.p2 / 2 or par.p % 2 != 0 or par.p2 % 2 != 0:
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
                k1 = (k+l)//2
                for p2 in range(max(new_ranges["p2"]["min"], p // 2 + ((p // 2) % 2)), new_ranges["p2"]["max"], 2):
                    for p1 in range(max(new_ranges["p1"]["min"], (p2 + 1) // 2), min(new_ranges["p1"]["max"], k1 - p2 // 2)):
                        indices = {"p": p, "p1": p1, "p2": p2,
                                   "l": l, "r": self._optimal_parameters["r"]}
                        if self._are_parameters_invalid(indices):
                            continue
                        yield indices

    def _time_and_memory_complexity(self, parameters: dict, verbose_information=None):
        """
        Computes the expected runtime and memory consumption
        """
        n, k, w = self.problem.get_parameters()
        par = SimpleNamespace(**parameters)
        k1 = (k + par.l) // 2

        solutions = self.problem.nsolutions
        memory_bound = self.problem.memory_bound
        L1 = binom(k1, par.p1)

        if self._is_early_abort_possible(log2(L1)):
            return inf, inf

        reps1 = (binom(par.p2, par.p2 // 2) *
                 binom(k1 - par.p2, par.p1 - par.p2 // 2)) ** 2
        l1 = int(ceil(log2(reps1)))

        if l1 > par.l:
            return inf, inf
        L12 = max(1, L1 ** 2 // 2 ** l1)
        reps2 = (binom(par.p, par.p // 2) *
                 binom(k1 - par.p, par.p2 - par.p // 2)) ** 2

        L1234 = max(1, L12 ** 2 // 2 ** (par.l - l1))
        if log2(reps2) > par.l+1:
            return inf, inf
        memory = log2((2 * L1 + L12 + L1234) + _mem_matrix(n, k, par.r))
        if memory > memory_bound:
            return inf, inf

        Tp = max(log2(binom(n, w)) - log2(binom(n - k - par.l, w - 2 * par.p)) - 2 * log2(binom(k1, par.p)) - solutions,
                 0)
        Tg = _gaussian_elimination_complexity(n, k, par.r)
        T_tree = 4 * _list_merge_complexity(L1, l1, self._hmap) + 2 * _list_merge_complexity(L12, par.l - l1,
                                                                                             self._hmap) \
            + _indyk_motwani_complexity(L1234, n -
                                        k - par.l, w - 2 * par.p, self._hmap)
        T_rep = int(
            ceil(2 ** (max(par.l - log2(reps2), 0) + 3 * max(l1 - log2(reps1), 0))))
        time = Tp + log2(Tg + T_rep * T_tree)

        if verbose_information is not None:
            verbose_information[VerboseInformation.CONSTRAINTS.value] = [
                l1, par.l - l1]
            verbose_information[VerboseInformation.REPRESENTATIONS.value] = Tp
            verbose_information[VerboseInformation.TREE.value] = log2(
                T_rep * T_tree)
            verbose_information[VerboseInformation.GAUSS.value] = log2(Tg)
            verbose_information[VerboseInformation.REPRESENTATIONS.value] = [
                reps1, reps2]
            verbose_information[VerboseInformation.LISTS.value] = [log2(L1), log2(L12), log2(L1234),
                                                                   2 * log2(L1234) + log2(
                                                                       binom(n - k - par.l, w - 2 * par.p)) - (
                n - par.l)]
            return verbose_information

        return time, memory

    def __repr__(self):
        """
        """
        rep = "May-Ozerov estimator in depth 3 for " + str(self.problem)
        return rep
