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
import pytest

class MQEstimator(BaseEstimator):
    def __init__(self, n: int, m: int, q=None, memory_bound=inf, **kwargs):
        """Construct an instance of MQEstimator.

        Args:
            n (int): The number of variables.
            m (int): The number of polynomials.
            q (None, optional): The order of the finite field. Defaults to None.
            w (int, optional): The linear algebra constant. Defaults to 2.
            theta (int, optional): The bit complexity exponent. Defaults to 2.
            h (int, optional): The external hybridization parameter. Defaults to 0.
            nsolutions (int, optional): The number of solutions in logarithmic scale. Defaults to max(expected_number_solutions, 0).
            excluded_algorithms (list, tuple, optional): A list or tuple of excluded algorithms. Defaults to None.
            memory_access (int, optional): Specifies the memory access cost model (0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage). Defaults to 0.
            complexity_type (int, optional): The complexity type to consider (0: estimate, 1: tilde O complexity). Defaults to 0.
            bit_complexities (int, optional): The state complexity as bit rather than field operations. Defaults to 1, and is only relevant for complexity_type 0.
            memory_bound (float, optional): The memory bound. Defaults to inf.

        Tests:
            >>> E = MQEstimator(n=15, m=15, q=2, w=2)
            >>> E.table(precision=3, truncate=1)
            +------------------+-----------------+
            |                  |     estimate    |
            +------------------+--------+--------+
            | algorithm        |   time | memory |
            +------------------+--------+--------+
            | Bjorklund        | 39.823 | 15.316 |
            | BooleanSolveFXL  | 20.339 | 11.720 |
            | Crossbred        | 18.174 | 15.616 |
            | DinurFirst       | 32.111 | 19.493 |
            | DinurSecond      | 20.349 | 15.801 |
            | ExhaustiveSearch | 17.966 | 11.720 |
            | F5               | 27.065 | 23.158 |
            | HybridF5         | 17.906 | 11.720 |
            | Lokshtanov       | 62.854 | 16.105 |
            +------------------+--------+--------+

            >>> if skip_long_doctests:
            ...     pytest.skip()
            >>> from cryptographic_estimators.MQEstimator import MQEstimator
            >>> E = MQEstimator(q=2, m=42, n=41, memory_bound=45, w=2)
            >>> E.table()
            +------------------+---------------+
            |                  |    estimate   |
            +------------------+------+--------+
            | algorithm        | time | memory |
            +------------------+------+--------+
            | Bjorklund        | 59.8 |   40.5 |
            | BooleanSolveFXL  | 46.3 |   16.1 |
            | Crossbred        | 41.1 |   37.4 |
            | DinurFirst       | 57.7 |   37.9 |
            | DinurSecond      | 42.8 |   33.6 |
            | ExhaustiveSearch | 44.4 |   16.1 |
            | F5               | 62.4 |   57.0 |
            | HybridF5         | 45.4 |   16.1 |
            | Lokshtanov       | 87.1 |   42.4 |
            +------------------+------+--------+


        """
        super(MQEstimator, self).__init__(MQAlgorithm, MQProblem(
            n=n, m=m, q=q, memory_bound=memory_bound, **kwargs), **kwargs)

    def table(self, show_quantum_complexity=0, show_tilde_o_time=0, show_all_parameters=0, precision=1, truncate=0):
        """Print table describing the complexity of each algorithm and its optimal parameters.
    
        Args:
            show_quantum_complexity (int): Whether to show quantum time complexity (default is 0).
            show_tilde_o_time (int): Whether to show Ō time complexity (default is 0).
            show_all_parameters (int): Whether to show all optimization parameters (default is 0).
            precision (int): Number of decimal digits to output (default is 1).
            truncate (int): Whether to truncate rather than round the output (default is 0).

        Examples:

        Tests:
            >>> if skip_long_doctests:
            ...     pytest.skip()

            >>> from cryptographic_estimators.MQEstimator import MQEstimator
            >>> E = MQEstimator(q=3, m=42, n=41, memory_bound=45, w=2)
            >>> E.table()
            +------------------+----------------+
            |                  |    estimate    |
            +------------------+-------+--------+
            | algorithm        |  time | memory |
            +------------------+-------+--------+
            | BooleanSolveFXL  |  68.8 |   26.1 |
            | Crossbred        |  61.6 |   44.2 |
            | ExhaustiveSearch |  67.1 |   17.1 |
            | F5               |  77.7 |   71.9 |
            | HybridF5         |  67.3 |   26.7 |
            | Lokshtanov       | 168.8 |   44.9 |
            +------------------+-------+--------+

            >>> from cryptographic_estimators.MQEstimator import MQEstimator
            >>> E = MQEstimator(q=16, m=42, n=41, complexity_type=1, w=2)
            >>> E.table(show_tilde_o_time=1, show_all_parameters=1)
            +------------------+-------------------------------------------------------+-------------------------------------------------------+
            |                  |                        estimate                       |                    tilde_o_estimate                   |
            +------------------+-------+--------+--------------------------------------+-------+--------+--------------------------------------+
            | algorithm        |  time | memory |              parameters              |  time | memory |              parameters              |
            +------------------+-------+--------+--------------------------------------+-------+--------+--------------------------------------+
            | BooleanSolveFXL  | 107.8 |   71.5 | {'k': 7, 'variant': 'deterministic'} |  98.4 |   70.4 | {'k': 7, 'variant': 'deterministic'} |
            | Crossbred        |  95.3 |   89.7 |      {'D': 15, 'd': 6, 'k': 30}      |  88.0 |   87.7 |      {'D': 15, 'd': 6, 'k': 30}      |
            | ExhaustiveSearch | 167.4 |   18.1 |                  {}                  | 164.0 |    0.0 |                  {}                  |
            | F5               | 119.3 |  111.9 |                  {}                  | 109.9 |  109.9 |                  {}                  |
            | HybridF5         | 103.8 |   72.4 |               {'k': 6}               |  94.4 |   70.4 |               {'k': 6}               |
            | Lokshtanov       | 620.9 |  164.4 |   {'delta': 0.024390243902439025}    | 147.6 |   16.4 |            {'delta': 0.9}            |
            +------------------+-------+--------+--------------------------------------+-------+--------+--------------------------------------+

            >>> E = MQEstimator(q=2, m=42, n=41, w=2.81)
            >>> E.table(show_tilde_o_time=1, show_all_parameters=1)
            +------------------+----------------------------------------------------+-------------------------------------------------------------------+
            |                  |                      estimate                      |                          tilde_o_estimate                         |
            +------------------+------+--------+------------------------------------+------+--------+---------------------------------------------------+
            | algorithm        | time | memory |             parameters             | time | memory |                     parameters                    |
            +------------------+------+--------+------------------------------------+------+--------+---------------------------------------------------+
            | Bjorklund        | 59.8 |   40.5 |  {'lambda_': 0.0975609756097561}   | 32.9 |   32.9 |                {'lambda_': 0.19677}               |
            | BooleanSolveFXL  | 46.3 |   16.1 | {'k': 40, 'variant': 'las_vegas'}  | 43.2 |    1.6 |         {'k': 40, 'variant': 'las_vegas'}         |
            | Crossbred        | 45.6 |   29.8 |     {'D': 4, 'd': 1, 'k': 11}      | 40.1 |   29.8 |             {'D': 4, 'd': 1, 'k': 11}             |
            | DinurFirst       | 57.7 |   37.9 | {'kappa': 0.325, 'lambda_': 0.175} | 28.5 |   28.5 | {'kappa': 0.3057, 'lambda_': 0.18665241123894338} |
            | DinurSecond      | 42.8 |   33.6 |             {'n1': 7}              | 33.4 |   25.8 |             {'n1': 7.592592592592592}             |
            | ExhaustiveSearch | 44.4 |   16.1 |                 {}                 | 41.0 |    0.0 |                         {}                        |
            | F5               | 85.5 |   57.0 |                 {}                 | 80.1 |   57.0 |                         {}                        |
            | HybridF5         | 45.4 |   16.1 |             {'k': 40}              | 40.0 |   16.1 |                     {'k': 40}                     |
            | Lokshtanov       | 87.1 |   42.4 |  {'delta': 0.024390243902439025}   | 35.9 |    5.1 |                 {'delta': 0.8765}                 |
            +------------------+------+--------+------------------------------------+------+--------+---------------------------------------------------+
                    
            >>> E = MQEstimator(q=16, n=594, m=64)
            >>> E.table(show_tilde_o_time=1, show_all_parameters=1)
            +------------------+----------------------------------------------------+----------------------------------------------------+
            |                  |                      estimate                      |                  tilde_o_estimate                  |
            +------------------+-------+--------+-----------------------------------+-------+--------+-----------------------------------+
            | algorithm        |  time | memory |             parameters            |  time | memory |             parameters            |
            +------------------+-------+--------+-----------------------------------+-------+--------+-----------------------------------+
            | BooleanSolveFXL  | 149.1 |   43.8 | {'k': 13, 'variant': 'las_vegas'} | 133.6 |   40.8 | {'k': 13, 'variant': 'las_vegas'} |
            | CGMTA            | 218.3 |   71.0 |                 {}                | 192.0 |   64.0 |                 {}                |
            | Crossbred        | 148.7 |  129.2 |     {'D': 22, 'd': 1, 'k': 25}    | 137.2 |  127.2 |     {'D': 22, 'd': 1, 'k': 25}    |
            | ExhaustiveSearch | 227.5 |   19.4 |                 {}                | 224.0 |    0.0 |                 {}                |
            | F5               | 235.9 |  163.0 |                 {}                | 226.1 |  161.0 |                 {}                |
            | HybridF5         | 169.2 |   55.6 |             {'k': 21}             | 159.3 |   53.6 |             {'k': 21}             |
            | Lokshtanov       | 682.7 |  224.5 |  {'delta': 0.017857142857142856}  | 201.6 |   22.4 |           {'delta': 0.9}          |
            | Hashimoto        | 129.6 |   28.5 |         {'k': 16, 'a': 18}        |    -- |     -- |                 {}                |
            +------------------+-------+--------+-----------------------------------+-------+--------+-----------------------------------+

            >>> E = MQEstimator(q=16, n=312, m=64)
            >>> E.table(show_tilde_o_time=1, show_all_parameters=1)
            +------------------+----------------------------------------------------+----------------------------------------------------+
            |                  |                      estimate                      |                  tilde_o_estimate                  |
            +------------------+-------+--------+-----------------------------------+-------+--------+-----------------------------------+
            | algorithm        |  time | memory |             parameters            |  time | memory |             parameters            |
            +------------------+-------+--------+-----------------------------------+-------+--------+-----------------------------------+
            | BooleanSolveFXL  | 159.2 |   52.6 | {'k': 11, 'variant': 'las_vegas'} | 143.2 |   49.6 | {'k': 11, 'variant': 'las_vegas'} |
            | CGMTA            | 235.9 |   50.5 |                 {}                | 212.0 |   44.0 |                 {}                |
            | Crossbred        | 161.1 |  141.2 |     {'D': 24, 'd': 1, 'k': 27}    | 149.5 |  139.2 |     {'D': 24, 'd': 1, 'k': 27}    |
            | ExhaustiveSearch | 247.6 |   19.8 |                 {}                | 244.0 |    0.0 |                 {}                |
            | F5               | 253.4 |  175.3 |                 {}                | 243.4 |  173.3 |                 {}                |
            | HybridF5         | 182.9 |   56.8 |             {'k': 24}             | 173.0 |   54.8 |             {'k': 24}             |
            | Lokshtanov       | 699.8 |  244.6 |   {'delta': 0.01639344262295082}  | 219.6 |   24.4 |           {'delta': 0.9}          |
            | Hashimoto        | 152.6 |   49.4 |         {'k': 11, 'a': 6}         |    -- |     -- |                 {}                |
            +------------------+-------+--------+-----------------------------------+-------+--------+-----------------------------------+
        """

        super(MQEstimator, self).table(show_quantum_complexity=show_quantum_complexity,
                                       show_tilde_o_time=show_tilde_o_time,
                                       show_all_parameters=show_all_parameters,
                                       precision=precision, truncate=truncate)
