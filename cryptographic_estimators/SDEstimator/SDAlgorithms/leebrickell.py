from ...SDEstimator.sd_algorithm import SDAlgorithm
from ...SDEstimator.sd_problem import SDProblem
from ...SDEstimator.sd_helper import _gaussian_elimination_complexity, _mem_matrix, binom, log2
from ...base_algorithm import optimal_parameter
from ...helper import memory_access_cost
from ..sd_constants import *
from ...SDEstimator.sd_helper import _gaussian_elimination_complexity, _mem_matrix, binom, log2, min_max, inf
from ..SDWorkfactorModels.prange import PrangeScipyModel
from types import SimpleNamespace

class LeeBrickell(SDAlgorithm):
    def __init__(self, problem: SDProblem, **kwargs):
        """
        Construct an instance of Lee-Brickells's estimator [TODO]_

        expected weight distribution::

            +--------------------------------+-------------------------------+
            | <----------+ n - k +---------> | <----------+ k +------------> |
            |               w-p              |              p                |
            +--------------------------------+-------------------------------+

        INPUT:

        - ``problem`` -- SDProblem object including all necessary parameters

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import Prange
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: Prange(SDProblem(n=100,k=50,w=10))
            Prange estimator for syndrome decoding problem with (n,k,w) = (100,50,10) over Finite Field of size 2
        """
        self._name = "LeeBrickell"
        super(LeeBrickell, self).__init__(problem, **kwargs)
        self.scipy_model = PrangeScipyModel
        self.initialize_parameter_ranges()
        _, _, _, q = self.problem.get_parameters()
        self._time_and_memory_complexity = self._time_and_memory_complexity_F2 if q == 2 else self._time_and_memory_complexity_Fq

    def initialize_parameter_ranges(self):
        """
        initialize the parameter ranges for p, l to start the optimisation 
        process.
        """
        _, _, w, _ = self.problem.get_parameters()
        s = self.full_domain
        self.set_parameter_ranges("p", 0, min_max(w // 2, 20, s))
    
    @optimal_parameter
    def p(self):
        """
        Return the optimal parameter $p$ used in the algorithm optimization

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import LeeBrickell
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = LeeBrickell(SDProblem(n=100,k=50,w=10))
            sage: A.p()
            0
        """
        return self._get_optimal_parameter("p")

    def _are_parameters_invalid(self, parameters: dict):
        """
        return if the parameter set `parameters` is invalid

        """
        n, k, w, _ = self.problem.get_parameters()
        par = SimpleNamespace(**parameters)
        if par.p > w // 2 or k < par.p or n - k < w - par.p:
            return True
        return False

    def _valid_choices(self):
        """
        Generator which yields on each call a new set of valid parameters based
        on the `_parameter_ranges` and already set parameters in
        `_optimal_parameters`
        """
        new_ranges = self._fix_ranges_for_already_set_parmeters()

        _, k, _, _ = self.problem.get_parameters()
        for p in range(new_ranges["p"]["min"], min(k, new_ranges["p"]["max"])):
            indices = {"p": p, "r": self._optimal_parameters["r"]}
            if self._are_parameters_invalid(indices):
                continue
            yield indices

    def _time_and_memory_complexity_F2(self, parameters: dict, verbose_information=None):
        """
        Return time complexity of Prange's algorithm over F2 for given set of
        parameters

        INPUT:
        -  ``parameters`` -- dictionary including parameters
        -  ``verbose_information`` -- if set to a dictionary `permutations` and `gauß` will be returned.

        """
        n, k, w, _ = self.problem.get_parameters()
        par = SimpleNamespace(**parameters)
        
        if self._are_parameters_invalid(parameters):
            return inf, inf
        
        solutions = self.problem.nsolutions
        memory = log2(_mem_matrix(n, k, par.r))

        Tp = max(log2(binom(n, w)) - log2(binom(n - k, w - par.p) - log2(binom(k, par.p))) - solutions, 0)
        Tg = log2(_gaussian_elimination_complexity(n, k, par.r))
        time = Tp + Tg
        time += memory_access_cost(memory, self.memory_access)

        if verbose_information is not None:
            verbose_information[VerboseInformation.PERMUTATIONS.value] = Tp
            verbose_information[VerboseInformation.GAUSS.value] = Tg

        return time, memory

    def _time_and_memory_complexity_Fq(self, parameters: dict, verbose_information=None):
        """
        Return time complexity of Lee-Brickell's algorithm over Fq, q > 2 for
        given set of parameters

        INPUT:
        -  ``parameters`` -- dictionary including parameters
        -  ``verbose_information`` -- if set to a dictionary `permutations`,
                                      `gauß` and `list` will be returned.

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import LeeBrickell
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: A = LeeBrickell(SDProblem(n=100,k=50,q=3,w=10))
            sage: A.p()
            0

        """
        n, k, w, q = self.problem.get_parameters()
        par = SimpleNamespace(**parameters)
        if self._are_parameters_invalid(parameters):
            return inf, inf

        solutions = self.problem.nsolutions
        memory = log2(_mem_matrix(n, k, par.r))

        Tp = max(log2(binom(n, w)) - log2(binom(n - k, w - par.p) - log2(binom(k, par.p))) - solutions, 0)
        Tg = log2(_gaussian_elimination_complexity(n, k, par.r))
        L = log2(k*k*q)
        time = Tp + Tg + L
        time += memory_access_cost(memory, self.memory_access)

        if verbose_information is not None:
            verbose_information[VerboseInformation.PERMUTATIONS.value] = Tp
            verbose_information[VerboseInformation.GAUSS.value] = Tg
            verbose_information[VerboseInformation.LISTS.value] = [L]

        return time, memory

    def __repr__(self):
        """
        """
        rep = "Prange estimator for " + str(self.problem)
        return rep
