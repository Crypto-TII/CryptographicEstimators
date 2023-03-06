from ..PKPEstimator.pkp_algorithm import PKPAlgorithm
from ..PKPEstimator.pkp_problem import PKPProblem
from ..base_estimator import BaseEstimator


class PKPEstimator(BaseEstimator):
	excluded_algorithms_by_default = []

	def __init__(self, **kwargs): # Add estimator parameters
		if not kwargs.get("excluded_algorithms"):
			kwargs["excluded_algorithms"] = []

		kwargs["excluded_algorithms"] += self.excluded_algorithms_by_default
		super(PKPEstimator, self).__init__(PKPAlgorithm, PKPProblem(**kwargs), **kwargs)
