from ..SEPEstimator.sep_algorithm import SEPAlgorithm
from ..SEPEstimator.sep_problem import SEPProblem
from ..base_estimator import BaseEstimator


class SEPEstimator(BaseEstimator):
	excluded_algorithms_by_default = []

	def __init__(self, **kwargs): # Add estimator parameters
		if not kwargs.get("excluded_algorithms"):
			kwargs["excluded_algorithms"] = []

		kwargs["excluded_algorithms"] += self.excluded_algorithms_by_default
		super(SEPEstimator, self).__init__(SEPAlgorithm, SEPProblem(**kwargs), **kwargs)
