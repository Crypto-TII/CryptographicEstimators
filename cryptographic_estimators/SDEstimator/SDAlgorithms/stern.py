from ...base_algorithm import optimal_parameter
from ...SDEstimator.sd_algorithm import SDAlgorithm
from ...SDEstimator.sd_problem import SDProblem
from ...SDEstimator.sd_helper import _gaussian_elimination_complexity, _mem_matrix, _list_merge_complexity, binom, log2, min_max, inf
from ...helper import memory_access_cost
from types import SimpleNamespace
from ..sd_constants import *
from ..SDWorkfactorModels.stern import SternScipyModel


class Stern(SDAlgorithm):
    def __init__(self, problem: SDProblem, **kwargs):
        """
        Construct an instance of Stern's estimator [Ste1988]_, [BLP2008]_.

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
        _, _, _, q = self.problem.get_parameters()
        self._time_and_memory_complexity = self._time_and_memory_complexity_F2 if q == 2 else self._time_and_memory_complexity_Fq

    def initialize_parameter_ranges(self):
        """
        initialize the parameter ranges for p, l to start the optimisation 
        process.
        """
        n, k, w, _ = self.problem.get_parameters()
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
        n, k, w, _ = self.problem.get_parameters()
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
        new_ranges = self._fix_ranges_for_already_set_parmeters()

        _, k, _, _ = self.problem.get_parameters()
        k1 = k//2
        for p in range(new_ranges["p"]["min"], min(k1, new_ranges["p"]["max"]), 2):
            L1 = binom(k1, p)
            l_val = int(log2(L1))
            l_search_radius = self._adjust_radius
            for l in range(max(new_ranges["l"]["min"], l_val-l_search_radius), min(new_ranges["l"]["max"], l_val+l_search_radius)):
                indices = {"p": p, "l": l, "r": self._optimal_parameters["r"]}
                if self._are_parameters_invalid(indices):
                    continue
                yield indices

    def _time_and_memory_complexity_F2(self, parameters: dict, verbose_information=None):
        """
        Return time complexity of Sterns's algorithm over F2 for given set of
        parameters

        INPUT:
        -  ``parameters`` -- dictionary including parameters
        -  ``verbose_information`` -- if set to a dictionary `permutations`,
                                      `gauß` and `list` will be returned.
        """
        n, k, w, _ = self.problem.get_parameters()
        par = SimpleNamespace(**parameters)
        k1 = k // 2

        if self._are_parameters_invalid(parameters):
            return inf, inf

        memory_bound = self.problem.memory_bound

        L1 = binom(k1, par.p)
        if self._is_early_abort_possible(log2(L1)):
            return inf, inf

        memory = log2(2 * L1 + _mem_matrix(n, k, par.r))
        solutions = self.problem.nsolutions

        if memory > memory_bound:
            return inf, memory_bound + 1

        Tp = max(0, log2(binom(n, w)) - log2(binom(n - k, w - 2 * par.p)) - \
                    log2(binom(k1, par.p) ** 2) - solutions)

        # We use Indyk-Motwani (IM) taking into account the possibility of multiple existing solutions
        # with correct weight distribution, decreasing the amount of necessary projections
        # remaining_sol denotes the number of expected solutions per permutation
        # l_part_iterations is the expected number of projections need by IM to find one of those solutions
        remaining_sol = (binom(n - k, w - 2 * par.p) * binom(k1, par.p)** 2 * binom(n, w) // 2 ** (n - k)) // binom(n, w)
        l_part_iterations = binom(n - k, w - 2 * par.p) // binom(n - k - par.l, w - 2 * par.p)

        if remaining_sol > 0:
            l_part_iterations //= max(1, remaining_sol)
            l_part_iterations = max(1, l_part_iterations)

        Tg = _gaussian_elimination_complexity(n, k, par.r)
        time = Tp + log2(Tg + _list_merge_complexity(L1, par.l, self._hmap) * l_part_iterations)

        time += memory_access_cost(memory, self.memory_access)

        if verbose_information is not None:
            verbose_information[VerboseInformation.PERMUTATIONS.value] = Tp
            verbose_information[VerboseInformation.GAUSS.value] = log2(Tg)
            verbose_information[VerboseInformation.LISTS.value] = [log2(L1), 2 * log2(L1) - par.l]

        return time, memory

    def _time_and_memory_complexity_Fq(self, parameters: dict, verbose_information=None):
        """
        Return time complexity of Sterns's algorithm over Fq for given set of
        parameters. Code originaly from
            - https://github.com/secomms/pkpattack/blob/main/cost_isd.sage
        which was adapted from:
            - https://github.com/christianepeters/isdfq/blob/master/isdfq.gp

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

        L1 = binom(k1, par.p)
        if self._is_early_abort_possible(log2(L1)):
            return inf, inf

        memory = log2(2 * L1 + _mem_matrix(n, k, par.r))
        solutions = self.problem.nsolutions

        if memory > memory_bound:
            return inf, memory_bound + 1

        Tp = max(0, log2(binom(n, w)) - log2(binom(n - k - par.l, w - 2 * par.p)) - \
                    log2(binom(k1, par.p)**2) - solutions)

        Tg = log2(_gaussian_elimination_complexity(n, k, par.r))
        
        #ops=(n-k)^2*(n+k)\
        #  + ((k1-p+1)+(Anum+Bnum)*(q-1)^p)*l\
        #  + q/(q-1.)*(w-2*p+1)*2*p*(1+(q-2)/(q-1.))*\
        #    Anum*Bnum*(q-1)^(2*p)/q^l;
        p = int(par.p)
        l = int(par.l)
        log2q=log2(q)

        # naming follows: https://eprint.iacr.org/2009/589.pdf
        # actual bit operations of the match routine
        # bit cost for comuting y, V_A and V_B
        #T1 = ((k1 - p + 1) + (2*L1)*(q-1)**p) * l
        # computation cost for each collision (after expected this number of bit operations we know if its not a solution) 
        #T2 = max(1, q/(q-1.)*(w-2*p+1)*2*p*(1+(q-2)/(q-1)))
        # number of collision Expected
        #T3 = L1**2 * (q-1)**(2*p)/(q**l)
        #if L1 == 1:
        #    T = 1
        #else:
        #    if not self._hmap:
        #        T = max(1, 2 * int(log2(L1)) * L1 +  (q-1)**(2*p) * L1 ** 2 // q ** l)
        #    else:
        #        T = 2 * L1 + ((q-1)**(2*p) * L1**2) // q**l
        #        print(log2(T), p, l, Tp, log2(L1), memory)
        #time = log2(T) + log2q + Tp + Tg
        #time += memory_access_cost(memory, self.memory_access)
        
        time = Tp + Tg + log2(_list_merge_complexity(L1, par.l, self._hmap, q=q, p=p))
        time += memory_access_cost(memory, self.memory_access)

        if verbose_information is not None:
            verbose_information[VerboseInformation.PERMUTATIONS.value] = Tp
            verbose_information[VerboseInformation.GAUSS.value] = log2(Tg)
            verbose_information[VerboseInformation.LISTS.value] = [log2(L1)]# TODO, log2((q-1)**(2*p) * L1 ** 2 // q ** l)]

        return time, memory

    def __repr__(self):
        rep = "Stern estimator for " + str(self.problem)
        return rep