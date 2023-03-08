
# Copyright 2023 


from ...SEEstimator.se_algorithm import SEAlgorithm
from ...SEEstimator.se_problem import SEProblem


class Sample(SEAlgorithm):

    def __init__(self, problem: SEProblem, **kwargs):
        super().__init__(problem, **kwargs)

    def _compute_time_complexity(self, parameters):
        pass

    def _compute_memory_complexity(self, parameters):
        pass
