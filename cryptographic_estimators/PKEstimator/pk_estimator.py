from ..PKEstimator.pk_algorithm import PKAlgorithm
from ..PKEstimator.pk_problem import PKProblem
from ..base_estimator import BaseEstimator


class PKEstimator(BaseEstimator):
	excluded_algorithms_by_default = []

	def __init__(self, **kwargs): # Add estimator parameters
		if not kwargs.get("excluded_algorithms"):
			kwargs["excluded_algorithms"] = []

		kwargs["excluded_algorithms"] += self.excluded_algorithms_by_default
		super(PKEstimator, self).__init__(PKAlgorithm, PKProblem(**kwargs), **kwargs)
