
# Copyright 2023 


from ..PKEstimator.pk_algorithm import PKAlgorithm
from ..PKEstimator.pk_problem import PKProblem
from ..base_estimator import BaseEstimator


class PKEstimator(BaseEstimator):
    """
    Construct an instance of Permuted Kernel Estimator

    INPUT:

    - ``n`` -- code length
    - ``k`` -- code dimension
    - ``excluded_algorithms`` -- a list/tuple of excluded algorithms (default: None)
    - ``nsolutions`` -- no. of solutions

    """
    excluded_algorithms_by_default = []

    def __init__(self, **kwargs):  # Add estimator parameters
        if not kwargs.get("excluded_algorithms"):
            kwargs["excluded_algorithms"] = []

        kwargs["excluded_algorithms"] += self.excluded_algorithms_by_default
        super(PKEstimator, self).__init__(
              PKAlgorithm, PKProblem(**kwargs), **kwargs)

    def table(self, show_quantum_complexity=0, show_tilde_o_time=0,
              show_all_parameters=0, precision=1, truncate=0):
        """
        Print table describing the complexity of each algorithm and its optimal parameters

        INPUT:

        - ``show_quantum_complexity`` -- show quantum time complexity (default: true)
        - ``show_tilde_o_time`` -- show Ō time complexity (default: true)
        - ``show_all_parameters`` -- show all optimization parameters (default: true)
        - ``precision`` -- number of decimal digits output (default: 1)
        - ``truncate`` -- truncate rather than round the output (default: false)

        """
        super(PKEstimator, self).table(show_quantum_complexity=show_quantum_complexity,
                                       show_tilde_o_time=show_tilde_o_time,
                                       show_all_parameters=show_all_parameters,
                                       precision=precision, truncate=truncate)
