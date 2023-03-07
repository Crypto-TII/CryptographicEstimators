from ..base_algorithm import BaseAlgorithm
from .pe_problem import PEProblem


class PEAlgorithm(BaseAlgorithm):
    def __init__(self, problem: PEProblem, **kwargs):
        """
        Base class for PE algorithms complexity estimator

        INPUT:

        - ``problem`` -- PEProblem object including all necessary parameters

        """
        super(PEAlgorithm, self).__init__(problem, **kwargs)

    def __repr__(self):
        """
        """
        pass
