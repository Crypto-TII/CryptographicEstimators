
# Copyright 2023 


from ..base_algorithm import BaseAlgorithm
from .pk_problem import PKProblem


class PKAlgorithm(BaseAlgorithm):
    def __init__(self, problem: PKProblem, **kwargs):
        """
        Base class for SD algorithms complexity estimator

        INPUT:

        - ``problem`` -- LEProblem object including all necessary parameters

        """
        super(PKAlgorithm, self).__init__(problem, **kwargs)

    def __repr__(self):
        """
        """
        pass
