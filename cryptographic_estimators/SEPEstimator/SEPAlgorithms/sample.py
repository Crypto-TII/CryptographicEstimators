from ...SEPEstimator.sep_algorithm import SEPAlgorithm
from ...SEPEstimator.sep_problem import SEPProblem


class Sample(SEPAlgorithm):

	def __init__(self, problem: SEPProblem, **kwargs):
		super().__init__(problem, **kwargs)

	def _compute_time_complexity(self, parameters):
		pass

	def _compute_memory_complexity(self, parameters):
		pass

