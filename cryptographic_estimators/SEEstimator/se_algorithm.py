
# Copyright 2023 


from ..base_algorithm import BaseAlgorithm
from .se_problem import SEProblem


class SEAlgorithm(BaseAlgorithm):

    def __init__(self, problem: SEProblem, **kwargs):
        """
        Base class for SE algorithms complexity estimator

        INPUT:

        - ``problem`` -- SEProblem object including all necessary parameters

        """
        super(SEAlgorithm, self).__init__(problem, **kwargs)

    def __repr__(self):
        """
        """
        pass
