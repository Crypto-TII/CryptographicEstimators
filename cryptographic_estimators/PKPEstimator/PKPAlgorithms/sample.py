from ...PKPEstimator.pkp_algorithm import PKPAlgorithm
from ...PKPEstimator.pkp_problem import PKPProblem


class Sample(PKPAlgorithm):

	def __init__(self, problem: PKPProblem, **kwargs):
		super().__init__(problem, **kwargs)

	def _compute_time_complexity(self, parameters):
		pass

	def _compute_memory_complexity(self, parameters):
		pass

