
# Copyright 2023 


from ...LEEstimator.le_algorithm import LEAlgorithm
from ...LEEstimator.le_problem import LEProblem


class Sample(LEAlgorithm):

    def __init__(self, problem: LEProblem, **kwargs):
        super().__init__(problem, **kwargs)

    def _compute_time_complexity(self, parameters):
        pass

    def _compute_memory_complexity(self, parameters):
        pass
