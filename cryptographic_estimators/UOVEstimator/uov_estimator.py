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


import pytest
from .uov_algorithm import UOVAlgorithm
from .uov_problem import UOVProblem
from ..base_estimator import BaseEstimator
from math import inf

class UOVEstimator(BaseEstimator):
    excluded_algorithms_by_default = []
    def __init__(self, n: int, m: int, q:int, memory_bound=inf, **kwargs):
        """Construct an instance of UOVEstimator.

        Args:
            n (int): Number of variables.
            m (int): Number of polynomials.
            q (int): Order of the finite field.
            memory_bound (float, optional): Memory bound. Defaults to inf.
            **kwargs: Additional keyword arguments.
                w (int, optional): Linear algebra constant. Defaults to 2.
                theta (float or None, optional): Exponent of the conversion factor. Defaults to 2.
                    If 0 <= theta <= 2, every multiplication in GF(q) is counted as log2(q) ^ theta binary operation.
                    If theta = None, every multiplication in GF(q) is counted as 2 * log2(q) ^ 2 + log2(q) binary operation.
                h (int, optional): External hybridization parameter. Defaults to 0.
                excluded_algorithms (list or tuple, optional): Algorithms to be excluded. Defaults to [].
                memory_access (int or callable, optional): Specifies the memory access cost model. Defaults to 0.
                    Choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root
                    or deploy custom function which takes as input the logarithm of the total memory usage.
                complexity_type (int, optional): Complexity type to consider. Defaults to 0.
                    0: estimate, 1: tilde O complexity.
                bit_complexities (int, optional): Determines if complexity is given in bit operations or basic operations. Defaults to 1 (in bit).
        """
        super(UOVEstimator, self).__init__(
            UOVAlgorithm,
            UOVProblem(n=n, m=m, q=q, memory_bound=memory_bound, **kwargs),
            **kwargs
        )
        self._estimator_type = "scheme"

    def table(self, show_quantum_complexity=0, show_tilde_o_time=0,
              show_all_parameters=0, precision=1, truncate=0):
        """Print table describing the complexity of each algorithm and its optimal parameters.
    
        Args:
            show_quantum_complexity (int): Show quantum time complexity (default: 0)
            show_tilde_o_time (int): Show Ō time complexity (default: 0)
            show_all_parameters (int): Show all optimization parameters (default: 0)
            precision (int): Number of decimal digits output (default: 1)
            truncate (int): Truncate rather than round the output (default: 0)

        Examples:
            >>> from cryptographic_estimators.UOVEstimator import UOVEstimator
            >>> A = UOVEstimator(n=24, m=10, q=2)
            >>> A.table(show_tilde_o_time=1)
            +--------------------+--------------+---------------+------------------+
            |                    |              |    estimate   | tilde_o_estimate |
            +--------------------+--------------+------+--------+-------+----------+
            | algorithm          | attack_type  | time | memory |  time |   memory |
            +--------------------+--------------+------+--------+-------+----------+
            | DirectAttack       |   forgery    | 11.2 |    9.5 |   8.0 |      9.5 |
            | KipnisShamir       | key-recovery | 16.8 |   12.5 |    -- |       -- |
            | CollisionAttack    |   forgery    | 17.4 |    8.0 |    -- |       -- |
            | IntersectionAttack | key-recovery | 23.3 |   13.1 |    -- |       -- |
            +--------------------+--------------+------+--------+-------+----------+


            >>> from cryptographic_estimators.UOVEstimator import UOVEstimator
            >>> E = UOVEstimator(q=13, n=25, m=23)
            >>> E.table(show_all_parameters=True)
            +--------------------+--------------+-------------------------------------------------------------------+
            |                    |              |                              estimate                             |
            +--------------------+--------------+------+--------+---------------------------------------------------+
            | algorithm          | attack_type  | time | memory |                     parameters                    |
            +--------------------+--------------+------+--------+---------------------------------------------------+
            | DirectAttack       |   forgery    | 66.2 |   47.4 | {'D': 8, 'd': 1, 'k': 10, 'variant': 'Crossbred'} |
            | CollisionAttack    |   forgery    | 54.8 |   45.5 |             {'X': 47.968, 'Y': 35.507}            |
            | IntersectionAttack | key-recovery |   -- |     -- |                         {}                        |
            +--------------------+--------------+------+--------+---------------------------------------------------+

        Tests:
            >>> if skip_long_doctests:
            ...     pytest.skip()
            >>> from cryptographic_estimators.UOVEstimator import UOVEstimator
            >>> A = UOVEstimator(n=112, m=44, q=256, theta=None)
            >>> A.table(show_all_parameters=1) # long time
            +--------------------+--------------+---------------------------------------------------------+
            |                    |              |                         estimate                        |
            +--------------------+--------------+-------+--------+----------------------------------------+
            | algorithm          | attack_type  |  time | memory |               parameters               |
            +--------------------+--------------+-------+--------+----------------------------------------+
            | DirectAttack       |   forgery    | 145.6 |   59.5 | {'k': 2, 'variant': 'BooleanSolveFXL'} |
            | KipnisShamir       | key-recovery | 218.1 |   22.1 |                   {}                   |
            | CollisionAttack    |   forgery    | 189.3 |  181.0 |      {'X': 180.389, 'Y': 169.976}      |
            | IntersectionAttack | key-recovery | 165.7 |   76.5 |                {'k': 2}                |
            +--------------------+--------------+-------+--------+----------------------------------------+


            >>> A = UOVEstimator(n=160, m=64, q=16, theta=None)
            >>> A.table(show_all_parameters=1) # long time
            +--------------------+--------------+------------------------------------------------------------+
            |                    |              |                          estimate                          |
            +--------------------+--------------+-------+--------+-------------------------------------------+
            | algorithm          | attack_type  |  time | memory |                 parameters                |
            +--------------------+--------------+-------+--------+-------------------------------------------+
            | DirectAttack       |   forgery    | 160.7 |   44.9 | {'k': 15, 'a': 3, 'variant': 'Hashimoto'} |
            | KipnisShamir       | key-recovery | 153.7 |   22.6 |                     {}                    |
            | CollisionAttack    |   forgery    | 141.0 |  131.7 |        {'X': 132.618, 'Y': 121.747}       |
            | IntersectionAttack | key-recovery | 176.2 |   76.9 |                  {'k': 3}                 |
            +--------------------+--------------+-------+--------+-------------------------------------------+


            >>> A = UOVEstimator(n=184, m=72, q=256, theta=None)
            >>> A.table(show_all_parameters=1) # long time
            +--------------------+--------------+---------------------------------------------------------+
            |                    |              |                         estimate                        |
            +--------------------+--------------+-------+--------+----------------------------------------+
            | algorithm          | attack_type  |  time | memory |               parameters               |
            +--------------------+--------------+-------+--------+----------------------------------------+
            | DirectAttack       |   forgery    | 217.9 |   87.0 | {'k': 4, 'variant': 'BooleanSolveFXL'} |
            | KipnisShamir       | key-recovery | 348.2 |   24.2 |                   {}                   |
            | CollisionAttack    |   forgery    | 301.6 |  293.3 |      {'X': 292.034, 'Y': 282.331}      |
            | IntersectionAttack | key-recovery | 249.9 |  117.9 |                {'k': 2}                |
            +--------------------+--------------+-------+--------+----------------------------------------+


            >>> A = UOVEstimator(n=244, m=96, q=256, theta=None)
            >>> A.table(show_all_parameters=1) # long time
            +--------------------+--------------+---------------------------------------------------------+
            |                    |              |                         estimate                        |
            +--------------------+--------------+-------+--------+----------------------------------------+
            | algorithm          | attack_type  |  time | memory |               parameters               |
            +--------------------+--------------+-------+--------+----------------------------------------+
            | DirectAttack       |   forgery    | 277.9 |  108.6 | {'k': 6, 'variant': 'BooleanSolveFXL'} |
            | KipnisShamir       | key-recovery | 445.3 |   25.4 |                   {}                   |
            | CollisionAttack    |   forgery    | 397.8 |  389.5 |      {'X': 387.826, 'Y': 378.539}      |
            | IntersectionAttack | key-recovery | 311.6 |  148.3 |                {'k': 2}                |
            +--------------------+--------------+-------+--------+----------------------------------------+
        """
        super(UOVEstimator, self).table(show_quantum_complexity=show_quantum_complexity,
                                          show_tilde_o_time=show_tilde_o_time,
                                          show_all_parameters=show_all_parameters,
                                          precision=precision, truncate=truncate)
