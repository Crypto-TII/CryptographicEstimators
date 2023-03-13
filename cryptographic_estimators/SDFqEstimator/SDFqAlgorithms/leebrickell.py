from ...SDFqEstimator.sdfq_algorithm import SDFqAlgorithm
from ...SDFqEstimator.sdfq_problem import SDFqProblem
from ...SDFqEstimator.sdfq_helper import binom, log2, min_max, inf
from ...base_algorithm import optimal_parameter
from ..sdfq_constants import *
from ..SDFqWorkfactorModels.prange import PrangeScipyModel
from types import SimpleNamespace


class LeeBrickell(SDFqAlgorithm):
    def __init__(self, problem: SDFqProblem, **kwargs):
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
            sage: from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import LeeBrickell
            sage: from cryptographic_estimators.SDFqEstimator import SDFqProblem
            sage: A = LeeBrickell(SDFqProblem(n=100,k=50,w=10,q=5))
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
        if par.p > w or k < par.p or n - k < w - par.p:
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
            indices = {"p": p}
            if self._are_parameters_invalid(indices):
                continue
            yield indices

    def _time_and_memory_complexity(self, parameters: dict, verbose_information=None):
        """
        Return time complexity of Lee-Brickell's algorithm over Fq, q > 2 for
        given set of parameters
        NOTE: this wokrs
        INPUT:
        -  ``parameters`` -- dictionary including parameters
        -  ``verbose_information`` -- if set to a dictionary `permutations`,
                                      `gauß` and `list` will be returned.
        EXAMPLES::
            sage: from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import LeeBrickell
            sage: from cryptographic_estimators.SDFqEstimator import SDFqProblem
            sage: A = LeeBrickell(SDFqProblem(n=100,k=50,q=3,w=10))
            sage: A.p()
            2
        """
        n, k, w, q = self.problem.get_parameters()
        par = SimpleNamespace(**parameters)
        if self._are_parameters_invalid(parameters):
            return inf, inf

        solutions = self.problem.nsolutions
        L =  log2(binom(k, par.p)) + log2(q) + log2(n)# + log2((q-1)**(par.p))
        memory = log2(k * n)

        Tp = max(log2(binom(n, w)) - log2(binom(n - k, w - par.p)) - log2(binom(k, par.p)) - solutions, 0)
        Tg = log2(k*k*n)
        time = Tp + log2(2**Tg + 2**L)
        
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
