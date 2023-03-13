from ..SDFqEstimator.sdfq_algorithm import SDFqAlgorithm
from ..SDFqEstimator.sdfq_problem import SDFqProblem
from ..base_estimator import BaseEstimator
from math import inf


class SDFqEstimator(BaseEstimator):
    """ 

    INPUT:

    - ``n`` -- code length
    - ``k`` -- code dimension
    - ``w`` -- error weight
    - ``q`` -- base field size
    - ``excluded_algorithms`` -- a list/tuple of excluded algorithms (default: None)
    - ``nsolutions`` -- no. of solutions

    """
    excluded_algorithms_by_default = []

    def __init__(self, n: int, k: int, w: int, q: int, memory_bound=inf, **kwargs):  # Add problem parameters
        if not kwargs.get("excluded_algorithms"):
            kwargs["excluded_algorithms"] = []

        kwargs["excluded_algorithms"] += self.excluded_algorithms_by_default
        super(SDFqEstimator, self).__init__(SDFqAlgorithm, SDFqProblem(
            n, k, w, q, memory_bound=memory_bound, **kwargs), **kwargs)

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

        EXAMPLES:

            sage: from cryptographic_estimators.SDFqEstimator import SDFqEstimator
            sage: A = SDFqEstimator(n=100,k=50,w=10,q=5)
            sage: A.table()
            +-------------+---------------+
            |             |    estimate   |
            +-------------+------+--------+
            | algorithm   | time | memory |
            +-------------+------+--------+
            | Prange      | 36.7 |   13.9 |
            | Stern       | 24.3 |   20.5 |
            | LeeBrickell | 25.7 |   13.5 |
            +-------------+------+--------+

        TESTS:
            sage: from cryptographic_estimators.SDFqEstimator import SDFqEstimator
            sage: A = SDFqEstimator(n=100, k=42, w=13, q=4,bit_complexities=1, workfactor_accuracy=20)
            sage: A.table(show_tilde_o_time=1, precision=1) # long time

            sage: from cryptographic_estimators.SDFqEstimator import SDFqEstimator
            sage: from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import Prange
            sage: A = SDFqEstimator(961,771,48,31,excluded_algorithms=[Prange])
            sage: A.table(precision=3, show_all_parameters=1) # long time

        """
        super(SDFqEstimator, self).table(show_quantum_complexity=show_quantum_complexity,
                                       show_tilde_o_time=show_tilde_o_time,
                                       show_all_parameters=show_all_parameters,
                                       precision=precision, truncate=truncate)
