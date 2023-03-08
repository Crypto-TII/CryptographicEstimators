from ..SDEstimator.sd_algorithm import SDAlgorithm
from ..SDEstimator.sd_problem import SDProblem
from ..SDEstimator.SDAlgorithms import BJMMd2, BJMMd3, MayOzerovD2, MayOzerovD3
from ..base_estimator import BaseEstimator
from math import inf


class SDEstimator(BaseEstimator):
    """
    Construct an instance of Syndrome Decoding Estimator

    INPUT:

    - ``n`` -- code length
    - ``k`` -- code dimension
    - ``w`` -- error weight
    - ``excluded_algorithms`` -- a list/tuple of excluded algorithms (default: None)
    - ``nsolutions`` -- no. of solutions

    TODO: Maybe we should add the optional_parameters dictionary here?

    """
    
    excluded_algorithms_by_default = [BJMMd2, BJMMd3, MayOzerovD2, MayOzerovD3]

    def __init__(self, n: int, k: int, w: int, memory_bound=inf, **kwargs):
        if not kwargs.get("excluded_algorithms"):
            kwargs["excluded_algorithms"] = []

        kwargs["excluded_algorithms"] += self.excluded_algorithms_by_default

        super(SDEstimator, self).__init__(SDAlgorithm, SDProblem(n, k, w, memory_bound=memory_bound, **kwargs), **kwargs)

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

            sage: from cryptographic_estimators.SDEstimator import SDEstimator
            sage: A = SDEstimator(n=100, k=50, w=10)
            sage: A.table()
            +---------------+---------------+
            |               |    estimate   |
            +---------------+------+--------+
            | algorithm     | time | memory |
            +---------------+------+--------+
            | BallCollision | 23.3 |   16.0 |
            | BJMMdw        | 23.4 |   14.7 |
            | BJMMpdw       | 23.3 |   14.3 |
            | BJMM          | 22.8 |   15.0 |
            | BothMay       | 22.4 |   14.7 |
            | Dumer         | 22.7 |   16.4 |
            | MayOzerov     | 22.3 |   14.8 |
            | Prange        | 28.3 |   12.7 |
            | Stern         | 22.3 |   16.0 |
            +---------------+------+--------+

        TESTS:
            sage: from cryptographic_estimators.SDEstimator import SDEstimator
            sage: A = SDEstimator(n=100, k=42, w=13, bit_complexities=1, workfactor_accuracy=20)
            sage: A.table(show_tilde_o_time=1, precision=1) # long time
            +---------------+---------------+------------------+
            |               |    estimate   | tilde_o_estimate |
            +---------------+------+--------+-------+----------+
            | algorithm     | time | memory |  time |   memory |
            +---------------+------+--------+-------+----------+
            | BallCollision | 23.8 |   15.6 |  10.8 |      3.2 |
            | BJMMdw        | 23.8 |   14.5 |    -- |       -- |
            | BJMMpdw       | 23.7 |   14.5 |    -- |       -- |
            | BJMM          | 23.3 |   14.8 |   9.5 |      7.0 |
            | BothMay       | 22.8 |   14.5 |   9.2 |      6.6 |
            | Dumer         | 23.2 |   16.0 |  10.8 |      3.2 |
            | MayOzerov     | 22.6 |   14.5 |   9.0 |      8.0 |
            | Prange        | 28.9 |   12.9 |  11.2 |      0.0 |
            | Stern         | 22.7 |   15.6 |  10.8 |      2.9 |
            +---------------+------+--------+-------+----------+

            sage: from cryptographic_estimators.SDEstimator import SDEstimator
            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import BJMMdw
            sage: A = SDEstimator(3488,2720,64,excluded_algorithms=[BJMMdw])
            sage: A.table(precision=3, show_all_parameters=1) # long time
            +---------------+--------------------------------------------------------------------------------+
            |               |                                    estimate                                    |
            +---------------+---------+---------+------------------------------------------------------------+
            | algorithm     |    time |  memory |                         parameters                         |
            +---------------+---------+---------+------------------------------------------------------------+
            | BallCollision | 151.460 |  49.814 |             {'r': 7, 'p': 4, 'pl': 0, 'l': 39}             |
            | BJMMpdw       | 143.448 |  86.221 |            {'r': 7, 'p': 12, 'p1': 8, 'w2': 0}             |
            | BJMM          | 141.886 | 104.057 | {'r': 7, 'depth': 3, 'p': 16, 'p1': 6, 'p2': 12, 'l': 197} |
            | BothMay       | 141.711 |  87.995 |   {'r': 7, 'p': 12, 'w1': 0, 'w2': 0, 'p1': 9, 'l': 79}    |
            | Dumer         | 151.380 |  58.019 |                 {'r': 7, 'l': 47, 'p': 5}                  |
            | MayOzerov     | 140.795 |  86.592 | {'r': 7, 'depth': 3, 'p': 12, 'p1': 5, 'p2': 10, 'l': 95}  |
            | Prange        | 173.388 |  21.576 |                          {'r': 7}                          |
            | Stern         | 151.409 |  49.814 |                 {'r': 7, 'p': 4, 'l': 39}                  |
            +---------------+---------+---------+------------------------------------------------------------+

        """
        super(SDEstimator, self).table(show_quantum_complexity=show_quantum_complexity,
                                       show_tilde_o_time=show_tilde_o_time,
                                       show_all_parameters=show_all_parameters,
                                       precision=precision, truncate=truncate)
