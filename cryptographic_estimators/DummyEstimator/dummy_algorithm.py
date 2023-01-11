from ..base_algorithm import BaseAlgorithm


class DummyAlgorithm(BaseAlgorithm):
    def __init__(self, problem, **kwargs):
        """
        Base class for MQ algorithms complexity estimator

        INPUT:

        - ``problem`` -- DummyProblem object including all necessary parameters
        - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
        - ``complexity_type`` -- complexity type to consider (0: estimate, 1: tilde O complexity, default: 0)

        """
        super(DummyAlgorithm, self).__init__(problem, **kwargs)

    def __repr__(self):
        par1, par2 = self.problem.get_parameters()
        return f"{self._name} estimator for the dummy problem with parameters {par1} and {par2} "
