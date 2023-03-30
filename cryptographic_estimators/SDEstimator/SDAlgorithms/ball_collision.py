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
from ...SDEstimator.sd_helper import _gaussian_elimination_complexity, _mem_matrix, _list_merge_complexity, binom, log2, inf, min_max
from types import SimpleNamespace
from ..sd_constants import *
from ..SDWorkfactorModels.ball_collision import BallCollisionScipyModel


class BallCollision(SDAlgorithm):
    def __init__(self, problem: SDProblem, **kwargs):
        """
        Complexity estimate of the ball collision decoding algorithm

        Introduced in [BLP11]_.

        expected weight distribution::

            +------------------+---------+---------+-------------+-------------+
            | <-+ n - k - l +->|<- l/2 ->|<- l/2 ->|<--+ k/2 +-->|<--+ k/2 +-->|
            |    w - 2p - 2pl  |   pl    |   pl    |      p      |      p      |
            +------------------+---------+---------+-------------+-------------+

        INPUT:

        - ``problem`` -- SDProblem object including all necessary parameters

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import BallCollision
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: BallCollision(SDProblem(n=100,k=50,w=10))
            Ball Collision estimator for syndrome decoding problem with (n,k,w) = (100,50,10) over Finite Field of size 2

        """
        super(BallCollision, self).__init__(problem, **kwargs)
        n, k, w = self.problem.get_parameters()

        self.set_parameter_ranges("p", 0, w // 2)
        self._name="BallCollision"
        s = self.full_domain
        self.set_parameter_ranges("l", 0, min_max(300, n - k, s))
        self.set_parameter_ranges("pl", 0, min_max(10, w, s))
        self.set_parameter_ranges("r", 0, n - k)

        self.scipy_model = BallCollisionScipyModel

    @optimal_parameter
    def l(self):
        """
        Return the optimal parameter $l$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import BallCollision
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = BallCollision(SDProblem(n=100,k=50,w=10))
            sage: A.l()
            7
        """
        return self._get_optimal_parameter("l")

    @optimal_parameter
    def p(self):
        """
        Return the optimal parameter $p$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import BallCollision
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = BallCollision(SDProblem(n=100,k=50,w=10))
            sage: A.p()
            2
        """
        return self._get_optimal_parameter("p")

    @optimal_parameter
    def pl(self):
        """
        Return the optimal parameter $pl$ used in the algorithm optimization

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import BallCollision
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = BallCollision(SDProblem(n=100,k=50,w=10))
            sage: A.pl()
            0

        """
        return self._get_optimal_parameter("pl")

    def _are_parameters_invalid(self, parameters: dict):
        """
        return if the parameter set `parameters` is invalid

        """
        n, k, w = self.problem.get_parameters()
        par = SimpleNamespace(**parameters)
        k1 = k // 2
        if par.p > w // 2 or k1 < par.p or par.pl > par.l // 2 or n - k - par.l < w - 2 * par.p - 2 * par.pl or w < 2 * par.p + 2 * par.pl:
            return True
        return False

    def _valid_choices(self):
        """
        Generator which yields on each call a new set of valid parameters based on the `_parameter_ranges` and already
        set parameters in `_optimal_parameters`
        """
        new_ranges = self._fix_ranges_for_already_set_parameters()
        n, k, w = self.problem.get_parameters()
        start_p = new_ranges["p"]["min"]+(new_ranges["p"]["min"] % 2)
        for p in range(start_p, min(w // 2, new_ranges["p"]["max"])+1, 2):
            for l in range(new_ranges["l"]["min"], min(n - k - (w - 2 * p), new_ranges["l"]["max"])+1):
                for pl in range(new_ranges["pl"]["min"], min(l//2, new_ranges["pl"]["max"], (w-2*p)//2)+1):
                    indices = {"p": p, "pl": pl, "l": l,
                               "r": self._optimal_parameters["r"]}
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

        memory_bound = self.problem.memory_bound

        L1 = binom(k1, par.p)
        if self._is_early_abort_possible(log2(L1)):
            return inf, inf

        L1 *= max(1, binom(par.l // 2, par.pl))
        memory = log2(2 * L1 + _mem_matrix(n, k, par.r))
        if memory > memory_bound:
            return inf, inf
        solutions = self.problem.nsolutions
        Tp = max(log2(binom(n, w)) - log2(binom(n - k - par.l, w - 2 * par.p - 2 * par.pl))
                 - 2 * log2(binom(k1, par.p)) - 2 * log2(binom(par.l // 2, par.pl)) - solutions, 0)
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
        rep = "Ball Collision estimator for " + str(self.problem)
        return rep
