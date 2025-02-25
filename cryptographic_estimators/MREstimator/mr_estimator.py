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


from .mr_algorithm import MRAlgorithm
from .mr_problem import MRProblem
from ..base_estimator import BaseEstimator
from math import inf
import pytest


class MREstimator(BaseEstimator):
    excluded_algorithms_by_default = []
    def __init__(self, q: int, m: int, n: int, k: int, r: int, memory_bound=inf, **kwargs):
        """Construct an instance of MREstimator.

        Args:
            q (int): Order of the finite field.
            m (int): Number of rows of the input matrices.
            n (int): Number of columns of the input matrices.
            k (int): Length of the solution vector.
            r (int): Target rank.
            memory_bound (float, optional): Maximum allowed memory to use for solving the problem. Defaults to inf.
            **kwargs: Additional keyword arguments.
                excluded_algorithm (list): A list/tuple of excluded algorithms (default: None)

        Examples:
            >>> from cryptographic_estimators.MREstimator import MREstimator
            >>> MRE = MREstimator(q=16, m=15, n=15, k=78, r=6)
        """

        super(MREstimator, self).__init__(
            MRAlgorithm,
            MRProblem(q, m, n, k, r, memory_bound=memory_bound, **kwargs),
            **kwargs
        )

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
            >>> from cryptographic_estimators.MREstimator import MREstimator
            >>> MRE = MREstimator(q=7, m=9, n=10, k=15, r=4)
            >>> MRE.table(show_all_parameters=1)
            +---------------+---------------------------------------------------------------------------------------+
            |               |                                        estimate                                       |
            +---------------+-------+--------+----------------------------------------------------------------------+
            | algorithm     |  time | memory |                              parameters                              |
            +---------------+-------+--------+----------------------------------------------------------------------+
            | SupportMinors |  38.8 |   12.1 | {'a': 1, 'lv': 0, 'b': 1, 'nprime': 8, 'variant': 'block_wiedemann'} |
            | KernelSearch  |  33.2 |   12.1 |                          {'a': 1, 'lv': 0}                           |
            | BigK          | 132.5 |   12.1 |                          {'a': 0, 'lv': 0}                           |
            | Minors        |  37.2 |   12.1 |                          {'a': 2, 'lv': 0}                           |
            | BruteForce    |  37.1 |   12.1 |                          {'a': 1, 'lv': 0}                           |
            +---------------+-------+--------+----------------------------------------------------------------------+

        Tests:
            >>> from cryptographic_estimators.MREstimator import MREstimator
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms import Minors, BigK
            >>> MR = MREstimator(q=2, m=64, n=64, k=44, r=44, excluded_algorithms=[Minors, BigK])
            >>> MR.table(show_all_parameters=1)
            +---------------+----------------------------------------------------------------------------------------+
            |               |                                        estimate                                        |
            +---------------+------+--------+------------------------------------------------------------------------+
            | algorithm     | time | memory |                               parameters                               |
            +---------------+------+--------+------------------------------------------------------------------------+
            | SupportMinors | 73.1 |   17.5 | {'a': 0, 'lv': 43, 'b': 1, 'nprime': 46, 'variant': 'block_wiedemann'} |
            | KernelSearch  | 60.4 |   17.5 |                           {'a': 0, 'lv': 0}                            |
            | BruteForce    | 60.4 |   17.5 |                           {'a': 0, 'lv': 0}                            |
            +---------------+------+--------+------------------------------------------------------------------------+

            >>> MRE = MREstimator(q=16, m=15, n=15, k=78, r=6)
            >>> MRE.table(show_all_parameters=1)
            +---------------+---------------------------------------------------------------------------------------+
            |               |                                        estimate                                       |
            +---------------+-------+--------+----------------------------------------------------------------------+
            | algorithm     |  time | memory |                              parameters                              |
            +---------------+-------+--------+----------------------------------------------------------------------+
            | SupportMinors | 144.0 |   16.1 | {'a': 5, 'lv': 0, 'b': 1, 'nprime': 8, 'variant': 'block_wiedemann'} |
            | KernelSearch  | 147.7 |   16.1 |                          {'a': 4, 'lv': 3}                           |
            | BigK          | 154.7 |   16.1 |                          {'a': 5, 'lv': 3}                           |
            | Minors        | 144.7 |   16.1 |                          {'a': 5, 'lv': 0}                           |
            | BruteForce    | 143.8 |   16.1 |                          {'a': 5, 'lv': 0}                           |
            +---------------+-------+--------+----------------------------------------------------------------------+

            >>> MRE = MREstimator(q=16, m=16, n=16, k=142, r=4)
            >>> MRE.table(show_all_parameters=1)
            +---------------+---------------------------------------------------------------------------------------+
            |               |                                        estimate                                       |
            +---------------+-------+--------+----------------------------------------------------------------------+
            | algorithm     |  time | memory |                              parameters                              |
            +---------------+-------+--------+----------------------------------------------------------------------+
            | SupportMinors | 165.9 |   17.2 | {'a': 8, 'lv': 0, 'b': 2, 'nprime': 8, 'variant': 'block_wiedemann'} |
            | KernelSearch  | 159.4 |   17.2 |                          {'a': 8, 'lv': 0}                           |
            | BigK          | 230.8 |   17.2 |                          {'a': 0, 'lv': 0}                           |
            | Minors        | 169.4 |   17.2 |                          {'a': 9, 'lv': 0}                           |
            | BruteForce    | 169.4 |   17.2 |                          {'a': 9, 'lv': 0}                           |
            +---------------+-------+--------+----------------------------------------------------------------------+

            >>> if skip_long_doctests:
            ...     pytest.skip()
            >>> MRE = MREstimator(q=16, m=19, n=19, k=109, r=8)
            >>> MRE.table(show_all_parameters=1)
            +---------------+----------------------------------------------------------------------------------------+
            |               |                                        estimate                                        |
            +---------------+-------+--------+-----------------------------------------------------------------------+
            | algorithm     |  time | memory |                               parameters                              |
            +---------------+-------+--------+-----------------------------------------------------------------------+
            | SupportMinors | 209.6 |   21.5 | {'a': 5, 'lv': 0, 'b': 2, 'nprime': 14, 'variant': 'block_wiedemann'} |
            | KernelSearch  | 207.4 |   17.3 |                           {'a': 5, 'lv': 0}                           |
            | BigK          | 431.1 |   17.3 |                           {'a': 0, 'lv': 0}                           |
            | Minors        | 216.3 |   17.3 |                           {'a': 6, 'lv': 0}                           |
            | BruteForce    | 216.3 |   17.3 |                           {'a': 6, 'lv': 0}                           |
            +---------------+-------+--------+-----------------------------------------------------------------------+

            >>> MRE = MREstimator(q=16, m=19, n=19, k=167, r=6)
            >>> MRE.table(show_all_parameters=1)
            +---------------+----------------------------------------------------------------------------------------+
            |               |                                        estimate                                        |
            +---------------+-------+--------+-----------------------------------------------------------------------+
            | algorithm     |  time | memory |                               parameters                              |
            +---------------+-------+--------+-----------------------------------------------------------------------+
            | SupportMinors | 236.3 |   18.9 | {'a': 8, 'lv': 0, 'b': 2, 'nprime': 11, 'variant': 'block_wiedemann'} |
            | KernelSearch  | 231.7 |   17.9 |                           {'a': 8, 'lv': 0}                           |
            | BigK          | 351.8 |   17.9 |                           {'a': 0, 'lv': 0}                           |
            | Minors        | 242.2 |   17.9 |                           {'a': 9, 'lv': 0}                           |
            | BruteForce    | 242.2 |   17.9 |                           {'a': 9, 'lv': 0}                           |
            +---------------+-------+--------+-----------------------------------------------------------------------+

            >>> MRE = MREstimator(q=16, m=21, n=21, k=189, r=7)
            >>> MRE.table(show_all_parameters=1)
            +---------------+----------------------------------------------------------------------------------------+
            |               |                                        estimate                                        |
            +---------------+-------+--------+-----------------------------------------------------------------------+
            | algorithm     |  time | memory |                               parameters                              |
            +---------------+-------+--------+-----------------------------------------------------------------------+
            | SupportMinors | 274.5 |   49.0 | {'a': 6, 'lv': 0, 'b': 8, 'nprime': 15, 'variant': 'block_wiedemann'} |
            | KernelSearch  | 269.2 |   18.4 |                           {'a': 8, 'lv': 0}                           |
            | BigK          | 452.6 |   18.4 |                           {'a': 0, 'lv': 0}                           |
            | Minors        | 278.7 |   18.4 |                           {'a': 9, 'lv': 0}                           |
            | BruteForce    | 278.7 |   18.4 |                           {'a': 9, 'lv': 0}                           |
            +---------------+-------+--------+-----------------------------------------------------------------------+

            >>> MRE = MREstimator(q=16, m=22, n=22, k=254, r=6)
            >>> MRE.table(show_all_parameters=1)
            +---------------+-----------------------------------------------------------------------------------------+
            |               |                                         estimate                                        |
            +---------------+-------+--------+------------------------------------------------------------------------+
            | algorithm     |  time | memory |                               parameters                               |
            +---------------+-------+--------+------------------------------------------------------------------------+
            | SupportMinors | 301.2 |   18.9 | {'a': 11, 'lv': 0, 'b': 1, 'nprime': 11, 'variant': 'block_wiedemann'} |
            | KernelSearch  | 302.8 |   18.9 |                           {'a': 11, 'lv': 0}                           |
            | BigK          | 425.4 |   18.9 |                           {'a': 0, 'lv': 0}                            |
            | Minors        | 314.9 |   33.2 |                           {'a': 11, 'lv': 0}                           |
            | BruteForce    | 316.0 |   18.9 |                           {'a': 12, 'lv': 0}                           |
            +---------------+-------+--------+------------------------------------------------------------------------+
            """
        super(MREstimator, self).table(show_quantum_complexity=show_quantum_complexity,
                                       show_tilde_o_time=show_tilde_o_time,
                                       show_all_parameters=show_all_parameters,
                                       precision=precision, truncate=truncate)
