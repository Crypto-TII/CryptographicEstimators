# ****************************************************************************
# Copyright 2023 Technology Innovation Institute
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ****************************************************************************


from ..MQEstimator.mq_algorithm import MQAlgorithm
from ..MQEstimator.mq_problem import MQProblem
from ..base_estimator import BaseEstimator
from math import inf


class MQEstimator(BaseEstimator):
    """
    Construct an instance of MQEstimator

    INPUT:

    - ``n`` -- number of variables
    - ``m`` -- number of polynomials
    - ``q`` -- order of the finite field (default: None)
    - ``w`` -- linear algebra constant (default: 2)
    - ``theta`` -- bit complexity exponent (default: 2)
    - ``h`` -- external hybridization parameter (default: 0)
    - ``nsolutions`` -- number of solutions in logarithmic scale (default: max(expected_number_solutions, 0))
    - ``excluded_algorithms`` -- a list/tuple of excluded algorithms (default: None)
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
    - ``complexity_type`` -- complexity type to consider (0: estimate, 1: tilde O complexity, default 0)
    - ``bit_complexities`` -- state complexity as bit rather than field operations (default 1, only relevant for complexity_type 0)

        TESTS::

            sage: from cryptographic_estimators.MQEstimator import MQEstimator
            sage: E = MQEstimator(q=2, m=42, n=41, memory_bound=45)
            sage: E.table() # long time
            +------------------+---------------+
            |                  |    estimate   |
            +------------------+------+--------+
            | algorithm        | time | memory |
            +------------------+------+--------+
            | Bjorklund        | 80.3 |   31.5 |
            | BooleanSolveFXL  | 46.3 |   16.1 |
            | Crossbred        | 39.8 |   37.9 |
            | DinurFirst       | 57.7 |   37.9 |
            | DinurSecond      | 42.8 |   33.6 |
            | ExhaustiveSearch | 44.4 |   16.1 |
            | F5               | 62.9 |   57.0 |
            | HybridF5         | 48.6 |   16.1 |
            | Lokshtanov       | 93.9 |   42.4 |
            +------------------+------+--------+

            sage: E = MQEstimator(n=15, m=15, q=2)
            sage: E.table(precision=3, truncate=1)
            +------------------+-----------------+
            |                  |     estimate    |
            +------------------+--------+--------+
            | algorithm        |   time | memory |
            +------------------+--------+--------+
            | Bjorklund        | 42.451 | 15.316 |
            | BooleanSolveFXL  | 20.339 | 11.720 |
            | Crossbred        | 17.672 | 16.785 |
            | DinurFirst       | 32.111 | 19.493 |
            | DinurSecond      | 20.349 | 15.801 |
            | ExhaustiveSearch | 17.966 | 11.720 |
            | F5               | 27.747 | 23.158 |
            | HybridF5         | 21.076 | 11.720 |
            | Lokshtanov       | 67.123 | 16.105 |
            +------------------+--------+--------+

    """

    def __init__(self, n: int, m: int, q=None, memory_bound=inf, **kwargs):
        super(MQEstimator, self).__init__(MQAlgorithm, MQProblem(
            n=n, m=m, q=q, memory_bound=memory_bound, **kwargs), **kwargs)

    def table(self, show_quantum_complexity=0, show_tilde_o_time=0, show_all_parameters=0, precision=1, truncate=0):
        """
        Print table describing the complexity of each algorithm and its optimal parameters

        INPUT:

        - ``show_quantum_complexity`` -- show quantum time complexity (default: true)
        - ``show_tilde_o_time`` -- show Ō time complexity (default: true)
        - ``show_all_parameters`` -- show all optimization parameters (default: true)
        - ``precision`` -- number of decimal digits output (default: 1)
        - ``truncate`` -- truncate rather than round the output (default: false)

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator import MQEstimator
            sage: E = MQEstimator(q=3, m=42, n=41, memory_bound=45)
            sage: E.table() # long time
            +------------------+----------------+
            |                  |    estimate    |
            +------------------+-------+--------+
            | algorithm        |  time | memory |
            +------------------+-------+--------+
            | BooleanSolveFXL  |  68.8 |   26.1 |
            | Crossbred        |  60.4 |   44.5 |
            | ExhaustiveSearch |  67.1 |   17.1 |
            | F5               |  78.3 |   71.9 |
            | HybridF5         |  67.8 |   26.7 |
            | Lokshtanov       | 174.5 |   44.9 |
            +------------------+-------+--------+

        TESTS::

            sage: from cryptographic_estimators.MQEstimator import MQEstimator
            sage: E = MQEstimator(q=16, m=42, n=41, complexity_type=1)
            sage: E.table(show_tilde_o_time=1, show_all_parameters=1) # long time
            +------------------+-------------------------------------------------------+-------------------------------------------------------+
            |                  |                        estimate                       |                    tilde_o_estimate                   |
            +------------------+-------+--------+--------------------------------------+-------+--------+--------------------------------------+
            | algorithm        |  time | memory |              parameters              |  time | memory |              parameters              |
            +------------------+-------+--------+--------------------------------------+-------+--------+--------------------------------------+
            | BooleanSolveFXL  | 107.8 |   71.5 | {'k': 7, 'variant': 'deterministic'} |  98.4 |   70.4 | {'k': 7, 'variant': 'deterministic'} |
            | Crossbred        |  93.6 |   89.7 |      {'D': 16, 'd': 7, 'k': 32}      |  87.8 |   87.7 |      {'D': 16, 'd': 7, 'k': 32}      |
            | ExhaustiveSearch | 167.4 |   18.1 |                  {}                  | 164.0 |    0.0 |                  {}                  |
            | F5               | 120.5 |  111.9 |                  {}                  | 111.1 |  109.9 |                  {}                  |
            | HybridF5         | 104.6 |   72.4 |               {'k': 6}               |  95.2 |   70.4 |               {'k': 6}               |
            | Lokshtanov       | 626.3 |  164.4 |           {'delta': 1/41}            | 147.6 |   16.4 |            {'delta': 0.9}            |
            +------------------+-------+--------+--------------------------------------+-------+--------+--------------------------------------+


            sage: E = MQEstimator(q=2, m=42, n=41)
            sage: E.table(show_tilde_o_time=1, show_all_parameters=1) # long time
            +------------------+---------------------------------------------------+-------------------------------------------------------------------+
            |                  |                      estimate                     |                          tilde_o_estimate                         |
            +------------------+------+--------+-----------------------------------+------+--------+---------------------------------------------------+
            | algorithm        | time | memory |             parameters            | time | memory |                     parameters                    |
            +------------------+------+--------+-----------------------------------+------+--------+---------------------------------------------------+
            | Bjorklund        | 80.3 |   31.5 |         {'lambda_': 13/41}        | 32.9 |   32.9 |                {'lambda_': 0.19677}               |
            | BooleanSolveFXL  | 46.3 |   16.1 | {'k': 40, 'variant': 'las_vegas'} | 43.2 |   16.1 |         {'k': 40, 'variant': 'las_vegas'}         |
            | Crossbred        | 39.8 |   37.9 |     {'D': 6, 'd': 1, 'k': 15}     | 38.0 |   37.9 |             {'D': 6, 'd': 1, 'k': 15}             |
            | DinurFirst       | 57.7 |   37.9 | {'kappa': 13/40, 'lambda_': 7/40} | 28.5 |   28.5 | {'kappa': 0.3057, 'lambda_': 0.18665241123894338} |
            | DinurSecond      | 42.8 |   33.6 |             {'n1': 7}             | 33.4 |   25.8 |             {'n1': 7.592592592592592}             |
            | ExhaustiveSearch | 44.4 |   16.1 |                 {}                | 41.0 |    0.0 |                         {}                        |
            | F5               | 62.9 |   57.0 |                 {}                | 57.5 |   57.0 |                         {}                        |
            | HybridF5         | 48.6 |   16.1 |             {'k': 40}             | 43.2 |   16.1 |                     {'k': 40}                     |
            | Lokshtanov       | 93.9 |   42.4 |          {'delta': 1/41}          | 35.9 |    5.1 |                 {'delta': 0.8765}                 |
            +------------------+------+--------+-----------------------------------+------+--------+---------------------------------------------------+
        """

        super(MQEstimator, self).table(show_quantum_complexity=show_quantum_complexity,
                                       show_tilde_o_time=show_tilde_o_time,
                                       show_all_parameters=show_all_parameters,
                                       precision=precision, truncate=truncate)
