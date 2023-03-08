from ...SDEstimator.sd_algorithm import SDAlgorithm
from ...SDEstimator.sd_problem import SDProblem
from ...SDEstimator.sd_helper import _gaussian_elimination_complexity, _mem_matrix, binom, log2
from ...helper import memory_access_cost, ComplexityType
from ..sd_constants import *
from ..SDWorkfactorModels.prange import PrangeScipyModel


class Prange(SDAlgorithm):
    def __init__(self, problem: SDProblem, **kwargs):
        """
        Construct an instance of Prange's estimator [Pra1962]_

        expected weight distribution::

            +--------------------------------+-------------------------------+
            | <----------+ n - k +---------> | <----------+ k +------------> |
            |                w               |              0                |
            +--------------------------------+-------------------------------+

        INPUT:

        - ``problem`` -- SDProblem object including all necessary parameters

        EXAMPLES::

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import Prange
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: Prange(SDProblem(n=100,k=50,w=10))
            Prange estimator for syndrome decoding problem with (n,k,w) = (100,50,10) over Finite Field of size 2
        """
        self._name = "Prange"
        super(Prange, self).__init__(problem, **kwargs)
        self.scipy_model = PrangeScipyModel
        
        _, _, _, q = self.problem.get_parameters()
        self._time_and_memory_complexity = self._time_and_memory_complexity_F2 if q == 2 else self._time_and_memory_complexity_Fq

    def _time_and_memory_complexity_F2(self, parameters: dict, verbose_information=None):
        """
        Return time complexity of Prange's algorithm for given set of parameters

        INPUT:
        -  ``parameters`` -- dictionary including parameters
        -  ``verbose_information`` -- if set to a dictionary `permutations` and `gauß` will be returned.
        """

        n, k, w, _ = self.problem.get_parameters()

        solutions = self.problem.nsolutions

        r = parameters["r"]
        memory = log2(_mem_matrix(n, k, r))

        Tp = max(log2(binom(n, w)) - log2(binom(n - k, w)) - solutions, 0)
        Tg = log2(_gaussian_elimination_complexity(n, k, r))
        time = Tp + Tg
        time += memory_access_cost(memory, self.memory_access)

        if verbose_information is not None:
            verbose_information[VerboseInformation.PERMUTATIONS.value] = Tp
            verbose_information[VerboseInformation.GAUSS.value] = Tg

        return time, memory

    def _time_and_memory_complexity_Fq(self, parameters: dict, verbose_information=None):
        """
        Return time complexity of Prange's algorithm for given set of parameters

        INPUT:
        -  ``parameters`` -- dictionary including parameters
        -  ``verbose_information`` -- if set to a dictionary `permutations` and `gauß` will be returned.
        """

        n, k, w, q = self.problem.get_parameters()
        solutions = self.problem.nsolutions

        r = parameters["r"]
        memory = log2(_mem_matrix(n, k, r))

        Tp = max(log2(binom(n, w)) - log2(binom(n - k, w)) - solutions, 0)
        Tg = log2(_gaussian_elimination_complexity(n, k, r))
        time = Tp + Tg*q
        time += memory_access_cost(memory, self.memory_access)

        if verbose_information is not None:
            verbose_information[VerboseInformation.PERMUTATIONS.value] = Tp
            verbose_information[VerboseInformation.GAUSS.value] = Tg

        return time, memory

    def __repr__(self):
        """
        """
        rep = "Prange estimator for " + str(self.problem)
        return rep
