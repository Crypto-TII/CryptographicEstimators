from ..SEEstimator.se_algorithm import SEAlgorithm
from ..SEEstimator.se_problem import SEProblem
from ..base_estimator import BaseEstimator


class SEEstimator(BaseEstimator):
	excluded_algorithms_by_default = []

	def __init__(self, **kwargs): # Add estimator parameters
		if not kwargs.get("excluded_algorithms"):
			kwargs["excluded_algorithms"] = []

		kwargs["excluded_algorithms"] += self.excluded_algorithms_by_default
		super(SEEstimator, self).__init__(SEAlgorithm, SEProblem(**kwargs), **kwargs)
