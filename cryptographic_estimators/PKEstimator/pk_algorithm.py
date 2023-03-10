from ..base_algorithm import BaseAlgorithm
from .pk_problem import PKProblem


class PKAlgorithm(BaseAlgorithm):
    def __init__(self, problem: PKProblem, **kwargs):
        """
        Base class for SD algorithms complexity estimator

        INPUT:

        - ``problem`` -- LEProblem object including all necessary parameters
        - ``cost_for_list_operation`` -- Cost in Fq additions for one list operation in the SBC and KMP algorithm (default n-m)
        - ``memory_for_list_element`` -- Memory in Fq elements for one list element in the SBC and KMP algorithm (default n-m)
        """
        super(PKAlgorithm, self).__init__(problem, **kwargs)
        n, m, _, _ = self.problem.get_parameters()
        self.cost_for_list_operation = kwargs.get("cost_for_list_operation", n - m)
        self.memory_for_list_element = kwargs.get("memory_for_list_element", n - m)

    def __repr__(self):
        """
        """

        return f"{self._name} estimator for the " + str(self.problem)
