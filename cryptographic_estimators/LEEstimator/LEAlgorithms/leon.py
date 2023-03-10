from ..le_algorithm import LEAlgorithm
from ..le_problem import LEProblem
from ...base_algorithm import optimal_parameter
from ...PEEstimator import Leon as PELeon
from ...PEEstimator.pe_problem import PEProblem


class Leon(LEAlgorithm):

    def __init__(self, problem: LEProblem, **kwargs):
        """
            Complexity estimate of Leons algorithm (

            TODO add reference to Leons paper

            Estimates are adapted versions of the scripts derived in <TODO add paolos paper> with the code accessible at
            <ADD GITHUB LINK>

            INPUT:

            - ``problem`` -- PEProblem object including all necessary parameters
            - ``codewords_needed_for_success`` -- Number of low word codewords needed for success (default = 100)
        """
        super().__init__(problem, **kwargs)
        self._name = "Leon"
        n, k, q = self.problem.get_parameters()
        self.PELeon = PELeon(PEProblem(n=n, k=k, q=q))

        self.set_parameter_ranges('w', 0, n)

    @optimal_parameter
    def w(self):
        """
        Return the optimal parameter $w$ used in the algorithm optimization
        """
        return self.PELeon.w()

    def _compute_time_complexity(self, parameters):
        return self.PELeon._compute_time_complexity(parameters)

    def _compute_memory_complexity(self, parameters):
        return self.PELeon._compute_memory_complexity(parameters)

    def __repr__(self):
        rep = "Leon estimator for " + str(self.problem)
        return rep
