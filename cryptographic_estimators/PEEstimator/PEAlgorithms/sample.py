
# Copyright 2023 


from ...PEEstimator.pe_algorithm import PEAlgorithm
from ...PEEstimator.pe_problem import PEProblem


class Sample(PEAlgorithm):

    def __init__(self, problem: PEProblem, **kwargs):
        super().__init__(problem, **kwargs)

    def _compute_time_complexity(self, parameters):
        pass

    def _compute_memory_complexity(self, parameters):
        pass
