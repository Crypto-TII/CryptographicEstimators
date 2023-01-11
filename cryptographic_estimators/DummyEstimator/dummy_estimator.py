from .dummy_algorithm import DummyAlgorithm
from .dummy_problem import DummyProblem
from ..base_estimator import BaseEstimator
from math import inf


class DummyEstimator(BaseEstimator):
    """
    Construct an instance of MQEstimator

    INPUT:
    - ``theta`` -- bit complexity exponent (default: 2)
    - ``h`` -- external hybridization parameter (default: 0)
    - ``nsolutions`` -- no. of solutions (default: 1)
    - ``excluded_algorithms`` -- a list/tuple of excluded algorithms (default: None)


    """

    def __init__(self, problem_parameter1, problem_parameter2, memory_bound=inf, **kwargs):
        super(DummyEstimator, self).__init__(DummyAlgorithm, DummyProblem(problem_parameter1=problem_parameter1,
                                                                          problem_parameter2=problem_parameter2,
                                                                          memory_bound=memory_bound, **kwargs), **kwargs)

    def table(self, show_quantum_complexity=0, show_tilde_o_time=0, show_all_parameters=0, precision=1, truncate=0):

        super(DummyEstimator, self).table(show_quantum_complexity=show_quantum_complexity,
                                         show_tilde_o_time=show_tilde_o_time,
                                         show_all_parameters=show_all_parameters,
                                         precision=precision, truncate=truncate)