from ...PKEstimator.pk_algorithm import PKAlgorithm
from ...PKEstimator.pk_problem import PKProblem


class Sample(PKAlgorithm):

    def __init__(self, problem: PKProblem, **kwargs):
        super().__init__(problem, **kwargs)

    def _compute_time_complexity(self, parameters):
        pass

    def _compute_memory_complexity(self, parameters):
        pass
