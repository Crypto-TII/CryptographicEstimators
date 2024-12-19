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
from .mayo_algorithm import MAYOAlgorithm
from .mayo_problem import MAYOProblem
from ..base_estimator import BaseEstimator
from math import inf


class MAYOEstimator(BaseEstimator):
    def __init__(self, n: int, m: int, o: int, k: int, q: int, memory_bound=inf, **kwargs):
        """Construct an instance of MAYOEstimator.

        Args:
            n (int): Number of variables.
            m (int): Number of polynomials.
            o (int): Dimension of the oil space.
            k (int): Whipping parameter.
            q (int): Order of the finite field.
            memory_bound: Memory bound.
            **kwargs: Additional keyword arguments.
                theta: Exponent of the conversion factor (default: 2).
                    If 0 <= theta <= 2, every multiplication in GF(q) is counted as log2(q) ^ theta binary operation.
                    If theta = None, every multiplication in GF(q) is counted as 2 * log2(q) ^ 2 + log2(q) binary operation.
                w: Linear algebra constant (default: 2.81).
                w_ks: Linear algebra constant (only for kipnis-shamir algorithm) (default: 2.8).
                h: External hybridization parameter (default: 0).
                excluded_algorithms: A list/tuple of algorithms to be excluded (default: []).
                memory_access: Specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage).
                complexity_type: Complexity type to consider (0: estimate, 1: tilde O complexity, default: 0).
                bit_complexities: Determines if complexity is given in bit operations or basic operations (default 1: in bit).
        """
        super(MAYOEstimator, self).__init__(
            MAYOAlgorithm, 
            MAYOProblem(n=n, m=m, o=o, k=k, q=q, memory_bound=memory_bound, **kwargs), 
            **kwargs
        )
        self._estimator_type = "scheme"

    # TODO: Optimize MAYOEstimator class constructor (it is taking too long to create an instance)
    def table(self, show_quantum_complexity=0, show_tilde_o_time=0,
              show_all_parameters=0, precision=1, truncate=0):
        """Print table describing the complexity of each algorithm and its optimal parameters.
    
        Args:
            show_quantum_complexity (int): Show quantum time complexity (default: 0)
            show_tilde_o_time (int): Show Ō time complexity (default: 0)
            show_all_parameters (int): Show all optimization parameters (default: 0)
            precision (int): Number of decimal digits output (default: 1)
            truncate (int): Truncate rather than round the output (default: 0)
    
        Tests:
            >>> if skip_long_doctests:
            ...     pytest.skip()
            >>> from cryptographic_estimators.MAYOEstimator import MAYOEstimator
            >>> E = MAYOEstimator(n=66, m=64, o=8, k=9, q=16)
            >>> E.table(show_all_parameters=1)
            +----------------------+--------------+-------------------------------------------------------------+
            |                      |              |                           estimate                          |
            +----------------------+--------------+-------+--------+--------------------------------------------+
            | algorithm            | attack_type  |  time | memory |                 parameters                 |
            +----------------------+--------------+-------+--------+--------------------------------------------+
            | DirectAttack         |   forgery    | 130.8 |   28.5 | {'k': 16, 'a': 18, 'variant': 'Hashimoto'} |
            | KipnisShamir         | key-recovery | 222.1 |   17.1 |                     {}                     |
            | ReconciliationAttack | key-recovery | 143.2 |   48.1 |      {'k': 9, 'variant': 'las_vegas'}      |
            | IntersectionAttack   | key-recovery | 254.8 |   33.5 |      {'k': 1, 'variant': 'las_vegas'}      |
            | ClawFinding          |   forgery    | 142.1 |  132.1 |        {'X': 130.915, 'Y': 125.085}        |
            +----------------------+--------------+-------+--------+--------------------------------------------+

            >>> E = MAYOEstimator(n=78, m=64, o=18, k=4, q=16)
            >>> E.table(show_all_parameters=1)
            +----------------------+--------------+------------------------------------------------------------+
            |                      |              |                          estimate                          |
            +----------------------+--------------+-------+--------+-------------------------------------------+
            | algorithm            | attack_type  |  time | memory |                 parameters                |
            +----------------------+--------------+-------+--------+-------------------------------------------+
            | DirectAttack         |   forgery    | 153.8 |   49.4 | {'k': 11, 'a': 6, 'variant': 'Hashimoto'} |
            | KipnisShamir         | key-recovery | 190.8 |   18.7 |                     {}                    |
            | ReconciliationAttack | key-recovery | 151.2 |   48.1 |     {'k': 11, 'variant': 'las_vegas'}     |
            | IntersectionAttack   | key-recovery | 202.5 |   45.0 |      {'k': 0, 'variant': 'las_vegas'}     |
            | ClawFinding          |   forgery    | 142.1 |  132.1 |        {'X': 130.915, 'Y': 125.085}       |
            +----------------------+--------------+-------+--------+-------------------------------------------+

            >>> E = MAYOEstimator(n=90, m=56, o=8, k=10, q=16)
            >>> E.table(show_all_parameters=1)
            +----------------------+--------------+------------------------------------------------------------+
            |                      |              |                          estimate                          |
            +----------------------+--------------+-------+--------+-------------------------------------------+
            | algorithm            | attack_type  |  time | memory |                 parameters                |
            +----------------------+--------------+-------+--------+-------------------------------------------+
            | DirectAttack         |   forgery    |  93.7 |   35.9 | {'k': 3, 'a': 27, 'variant': 'Hashimoto'} |
            | KipnisShamir         | key-recovery | 319.3 |   18.0 |                     {}                    |
            | ReconciliationAttack | key-recovery | 150.3 |   43.8 |     {'k': 13, 'variant': 'las_vegas'}     |
            | IntersectionAttack   | key-recovery | 399.1 |   59.1 |      {'k': 0, 'variant': 'las_vegas'}     |
            | ClawFinding          |   forgery    | 126.0 |  116.0 |        {'X': 115.011, 'Y': 108.989}       |
            +----------------------+--------------+-------+--------+-------------------------------------------+

            >>> E = MAYOEstimator(n=64, m=60, o=10, k=21, q=16)
            >>> E.table(show_all_parameters=1)
            +----------------------+--------------+------------------------------------------------------------+
            |                      |              |                          estimate                          |
            +----------------------+--------------+-------+--------+-------------------------------------------+
            | algorithm            | attack_type  |  time | memory |                 parameters                |
            +----------------------+--------------+-------+--------+-------------------------------------------+
            | DirectAttack         |   forgery    |  98.8 |   38.6 | {'k': 3, 'a': 29, 'variant': 'Hashimoto'} |
            | KipnisShamir         | key-recovery | 198.0 |   17.3 |                     {}                    |
            | ReconciliationAttack | key-recovery | 134.6 |   49.8 |      {'k': 6, 'variant': 'las_vegas'}     |
            | IntersectionAttack   | key-recovery | 224.8 |   36.5 |      {'k': 0, 'variant': 'las_vegas'}     |
            | ClawFinding          |   forgery    | 134.0 |  124.0 |        {'X': 122.962, 'Y': 117.038}       |
            +----------------------+--------------+-------+--------+-------------------------------------------+
                    
        """
        super(MAYOEstimator, self).table(show_quantum_complexity=show_quantum_complexity,
                                          show_tilde_o_time=show_tilde_o_time,
                                          show_all_parameters=show_all_parameters,
                                          precision=precision, truncate=truncate)
