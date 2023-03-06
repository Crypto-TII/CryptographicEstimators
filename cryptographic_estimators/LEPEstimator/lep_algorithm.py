from ..base_algorithm import BaseAlgorithm
from .lep_problem import LEPProblem


class LEPAlgorithm(BaseAlgorithm):
    """
    Base class for Syndrome Decoding algorithms complexity estimator
    
    INPUT:
    
    - ``problem`` -- LEPProblem object including all necessary parameters
    """

    def __init__(self, problem: LEPProblem, **kwargs):
        super(LEPAlgorithm, self).__init__(problem, **kwargs)
    
    def __repr__(self):
        pass

