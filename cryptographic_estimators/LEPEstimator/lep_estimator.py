from ..LEPEstimator.lep_algorithm import LEPAlgorithm
from ..LEPEstimator.lep_problem import LEPProblem
from ..base_estimator import BaseEstimator


class LEPEstimator(BaseEstimator):
	excluded_algorithms_by_default = []

	def __init__(self, **kwargs): # Add estimator parameters
		if not kwargs.get("excluded_algorithms"):
			kwargs["excluded_algorithms"] = []

		kwargs["excluded_algorithms"] += self.excluded_algorithms_by_default
		super(LEPEstimator, self).__init__(LEPAlgorithm, LEPProblem(**kwargs), **kwargs)
