from ...SDFqEstimator.sdfq_algorithm import SDFqAlgorithm
from ...SDFqEstimator.sdfq_problem import SDFqProblem
from ...SDFqEstimator.sdfq_helper import _gaussian_elimination_complexity, _mem_matrix, binom, log2
from ...helper import memory_access_cost, ComplexityType
from ..sdfq_constants import *
from ..SDFqWorkfactorModels.prange import PrangeScipyModel


class Prange(SDFqAlgorithm):
    def __init__(self, problem: SDFqProblem, **kwargs):
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
            sage: from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import Prange
            sage: from cryptographic_estimators.SDFqEstimator import SDFqProblem
            sage: Prange(SDFqProblem(n=100,k=50,w=10,q=3))
            Prange estimator for syndrome decoding over q problem with (n,k,w) = (100,50,10) over Finite Field of size 3
        """
        self._name = "Prange"
        super(Prange, self).__init__(problem, **kwargs)
        self.scipy_model = PrangeScipyModel

    def _time_and_memory_complexity(self, parameters: dict, verbose_information=None):
        """
        Return time complexity of Prange's algorithm for given set of parameters
        INPUT:
        -  ``parameters`` -- dictionary including parameters
        -  ``verbose_information`` -- if set to a dictionary `permutations` and `gauß` will be returned.
        """

        n, k, w, q = self.problem.get_parameters()
        solutions = self.problem.nsolutions

        r = parameters["r"]
        memory = log2(_mem_matrix(n, k, r) * n)

        Tp = max(log2(binom(n, w)) - log2(binom(n - k, w)) - solutions, 0)
        Tg = log2(_gaussian_elimination_complexity(n, k, r)*(n-k))
        time = Tp + Tg
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
