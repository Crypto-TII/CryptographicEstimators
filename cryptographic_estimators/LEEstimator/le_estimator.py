from ..LEEstimator.le_algorithm import LEAlgorithm
from ..LEEstimator.le_problem import LEProblem
from ..base_estimator import BaseEstimator


class LEEstimator(BaseEstimator):
	excluded_algorithms_by_default = []

	def __init__(self, **kwargs): # Add estimator parameters
		if not kwargs.get("excluded_algorithms"):
			kwargs["excluded_algorithms"] = []

		kwargs["excluded_algorithms"] += self.excluded_algorithms_by_default
		super(LEEstimator, self).__init__(LEAlgorithm, LEProblem(**kwargs), **kwargs)
