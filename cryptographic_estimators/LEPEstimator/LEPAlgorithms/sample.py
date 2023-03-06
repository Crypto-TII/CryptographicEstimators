from ...LEPEstimator.lep_algorithm import LEPAlgorithm
from ...LEPEstimator.lep_problem import LEPProblem


class Sample(LEPAlgorithm):

	def __init__(self, problem: LEPProblem, **kwargs):
		super().__init__(problem, **kwargs)

	def _compute_time_complexity(self, parameters):
		pass

	def _compute_memory_complexity(self, parameters):
		pass

