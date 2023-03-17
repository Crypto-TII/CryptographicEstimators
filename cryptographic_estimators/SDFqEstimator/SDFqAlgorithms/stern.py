from ...base_algorithm import optimal_parameter
from ...SDFqEstimator.sdfq_algorithm import SDFqAlgorithm
from ...SDFqEstimator.sdfq_problem import SDFqProblem
from ...SDFqEstimator.sdfq_helper import _mem_matrix, binom, log2, min_max, inf
from types import SimpleNamespace
from ..sdfq_constants import *
#from ..SDFqWorkfactorModels.stern import SternScipyModel


class Stern(SDFqAlgorithm):
    def __init__(self, problem: SDFqProblem, **kwargs):
        """
        Construct an instance of Stern's estimator [Ste1988]_, [BLP2008]_.  TODO [Peters]
        Expected weight distribution::
            +-------------------------+---------+-------------+-------------+
            | <----+ n - k - l +----> |<-- l -->|<--+ k/2 +-->|<--+ k/2 +-->|
            |          w - 2p         |    0    |      p      |      p      |
            +-------------------------+---------+-------------+-------------+

        INPUT:
        - ``problem`` -- SDProblem object including all necessary parameters

        TEST::
            sage: from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import Stern
            sage: from cryptographic_estimators.SDFqEstimator import SDFqProblem
            sage: Stern(SDFqProblem(n=961,k=771,w=48,q=31)).time_complexity()
            129.05902980703917

        EXAMPLES::
            sage: from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import Stern
            sage: from cryptographic_estimators.SDFqEstimator import SDFqProblem
            sage: Stern(SDFqProblem(n=100,k=50,w=10,q=3))
            Stern estimator for syndrome decoding problem with (n,k,w) = (100,50,10) over Finite Field of size 3

        """
        self._name = "Stern"
        super(Stern, self).__init__(problem, **kwargs)
        self.initialize_parameter_ranges()

    def initialize_parameter_ranges(self):
        """
        Initialize the parameter ranges for p, l to start the optimisation
        process.
        """
        n, k, w, _ = self.problem.get_parameters()
        s = self.full_domain
        self.set_parameter_ranges("p", 0, min_max(max(w // 2, 1), 30, s))
        self.set_parameter_ranges("l", 0, min_max(n - k, 400, s))

    @optimal_parameter
    def l(self):
        """
        Return the optimal parameter $l$ used in the algorithm optimization

        EXAMPLES::
            sage: from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import Stern
            sage: from cryptographic_estimators.SDFqEstimator import SDFqProblem
            sage: A = Stern(SDFqProblem(n=100,k=50,w=10,q=3))
            sage: A.l()
            7

        """

        return self._get_optimal_parameter("l")

    @optimal_parameter
    def p(self):
        """
        Return the optimal parameter $p$ used in the algorithm optimization

        EXAMPLES::
            sage: from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import Stern
            sage: from cryptographic_estimators.SDFqEstimator import SDFqProblem
            sage: A = Stern(SDFqProblem(n=100,k=50,w=10,q=3))
            sage: A.p()
            2

        """

        return self._get_optimal_parameter("p")

    def _are_parameters_invalid(self, parameters: dict):
        """
        Return if the parameter set `parameters` is invalid
        """
        n, k, w, _ = self.problem.get_parameters()
        par = SimpleNamespace(**parameters)
        k1 = k // 2
        if par.p > w or k1 < par.p or n - k - par.l < w - 2 * par.p:
            return True
        return False

    def _valid_choices(self):
        """
        Generator which yields on each call a new set of valid parameters based on the `_parameter_ranges` and already
        set parameters in `_optimal_parameters`
        """
        new_ranges = self._fix_ranges_for_already_set_parmeters()

        _, k, _, q = self.problem.get_parameters()
        k1 = k//2
        for p in range(new_ranges["p"]["min"], min(k1, new_ranges["p"]["max"])):
            l_val = int(log2(binom(k1, p)) - log2(q-1)*p)
            l_search_radius = self._adjust_radius
            for l in range(max(new_ranges["l"]["min"], l_val-l_search_radius), min(new_ranges["l"]["max"], l_val+l_search_radius)):
                indices = {"p": p, "l": l}
                if self._are_parameters_invalid(indices):
                    continue
                yield indices

    def _time_and_memory_complexity(self, parameters: dict, verbose_information=None):
        """
        Return time complexity of Sterns's algorithm over Fq for given set of
        parameters. Code originaly from
            - https://github.com/secomms/pkpattack/blob/main/cost_isd.sage
        which was adapted from:
            - https://github.com/christianepetersisdfq/blob/master/isdfq.gp

        INPUT:
        -  ``parameters`` -- dictionary including parameters
        -  ``verbose_information`` -- if set to a dictionary `permutations`,
                                      `gauß` and `list` will be returned.

        """
        n, k, w, q = self.problem.get_parameters()
        par = SimpleNamespace(**parameters)
        k1 = k // 2

        if self._are_parameters_invalid(parameters):
            return inf, inf

        memory_bound = self.problem.memory_bound

        L1 = binom(k1, par.p) * (q-1)**par.p
        L2 = binom(k-k1, par.p) * (q-1)**par.p
        if self._is_early_abort_possible(log2(L1)):
            return inf, inf

        memory = log2((L1 + L2) * par.l + _mem_matrix(n, k, 0)) + log2(n)
        solutions = self.problem.nsolutions

        if memory > memory_bound:
            return inf, inf

        Tp = max(0,
                 log2(binom(n, w)) - log2(binom(n - k - par.l, w - 2 * par.p)) - log2(binom(k1, par.p)**2) - solutions)

        Tg = (n-k)**2 * (n+k) // 2
        
        build = max(((k1 - par.p + 1) + (L2+L1)) * par.l, 1)
        cost_early_exit = max(1,int(max(q/(q-1) * (w - 2 * par.p + 1) * 2*par.p *(1 + (q - 2)/(q - 1)), 1)))
        L = L1*L2//q**par.l
        ops = build + L*cost_early_exit
        time = log2(Tg + ops) + Tp

        if verbose_information is not None:
            verbose_information[VerboseInformation.PERMUTATIONS.value] = Tp
            verbose_information[VerboseInformation.GAUSS.value] = log2(Tg)
            verbose_information[VerboseInformation.LISTS.value] = [log2(L2), log2(L), log2(ops), log2(ops + Tg), solutions]

        return time, memory

    def __repr__(self):
        rep = "Stern estimator for " + str(self.problem)
        return rep
