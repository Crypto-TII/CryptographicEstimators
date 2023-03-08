
# Copyright 2023 


from ..base_algorithm import BaseAlgorithm
from .le_problem import LEProblem


class LEAlgorithm(BaseAlgorithm):
    def __init__(self, problem: LEProblem, **kwargs):
        """
        Base class for SD algorithms complexity estimator

        INPUT:

        - ``problem`` -- LEProblem object including all necessary parameters

        """
        super(LEAlgorithm, self).__init__(problem, **kwargs)

    def __repr__(self):
        """
        """
        pass
