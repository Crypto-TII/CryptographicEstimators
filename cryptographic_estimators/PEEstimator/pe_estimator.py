from ..PEEstimator.pe_algorithm import PEAlgorithm
from ..PEEstimator.pe_problem import PEProblem
from ..base_estimator import BaseEstimator


class PEEstimator(BaseEstimator):
	excluded_algorithms_by_default = []

	def __init__(self, **kwargs): # Add estimator parameters
		if not kwargs.get("excluded_algorithms"):
			kwargs["excluded_algorithms"] = []

		kwargs["excluded_algorithms"] += self.excluded_algorithms_by_default
		super(PEEstimator, self).__init__(PEAlgorithm, PEProblem(**kwargs), **kwargs)
