from ..[AEstimator.[a_algorithm import [AAlgorithm
from ..[AEstimator.[a_problem import [AProblem
from ..base_estimator import BaseEstimator


class [AEstimator(BaseEstimator):
	excluded_algorithms_by_default = []

	def __init__(self, **kwargs): # Add estimator parameters
		if not kwargs.get("excluded_algorithms"):
			kwargs["excluded_algorithms"] = []

		kwargs["excluded_algorithms"] += self.excluded_algorithms_by_default
		super([AEstimator, self).__init__([AAlgorithm, [AProblem(**kwargs), **kwargs)
