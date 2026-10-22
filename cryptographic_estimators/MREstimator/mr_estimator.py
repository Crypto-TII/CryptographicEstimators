# ****************************************************************************
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
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
              show_all_parameters=0, precision=1, truncate=0, *args, **kwargs):
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
            +---------------+---------------------------------------------------------+
            |               |                         estimate                        |
            +---------------+-------+--------+----------------------------------------+
            | algorithm     |  time | memory |               parameters               |
            +---------------+-------+--------+----------------------------------------+
            | SupportMinors |  38.8 |   12.1 | {'a': 1, 'lv': 0, 'b': 1, 'nprime': 8} |
            | KernelSearch  |  34.9 |   12.1 |           {'a': 1, 'lv': 0}            |
            | BigK          | 129.7 |   12.1 |           {'a': 0, 'lv': 0}            |
            | Minors        |  40.1 |   13.2 |           {'a': 1, 'lv': 3}            |
            | BruteForce    |  38.3 |   12.1 |           {'a': 1, 'lv': 0}            |
            +---------------+-------+--------+----------------------------------------+

        Tests:
            >>> from cryptographic_estimators.MREstimator import MREstimator
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms import Minors, BigK
            >>> MR = MREstimator(q=2, m=64, n=64, k=44, r=44, excluded_algorithms=[Minors, BigK])
            >>> MR.table(show_all_parameters=1)
            +---------------+----------------------------------------------------------+
            |               |                         estimate                         |
            +---------------+------+--------+------------------------------------------+
            | algorithm     | time | memory |                parameters                |
            +---------------+------+--------+------------------------------------------+
            | SupportMinors | 64.1 |   17.5 | {'a': 0, 'lv': 43, 'b': 2, 'nprime': 45} |
            | KernelSearch  | 62.0 |   17.5 |            {'a': 0, 'lv': 0}             |
            | BruteForce    | 62.3 |   17.5 |            {'a': 0, 'lv': 0}             |
            +---------------+------+--------+------------------------------------------+

            >>> MRE = MREstimator(q=16, m=15, n=15, k=78, r=6)
            >>> MRE.table(show_all_parameters=1)
            +---------------+---------------------------------------------------------+
            |               |                         estimate                        |
            +---------------+-------+--------+----------------------------------------+
            | algorithm     |  time | memory |               parameters               |
            +---------------+-------+--------+----------------------------------------+
            | SupportMinors | 144.6 |   16.1 | {'a': 5, 'lv': 0, 'b': 1, 'nprime': 8} |
            | KernelSearch  | 149.2 |   16.1 |           {'a': 4, 'lv': 3}            |
            | BigK          | 253.2 |   16.1 |           {'a': 0, 'lv': 0}            |
            | Minors        | 145.1 |   16.1 |           {'a': 5, 'lv': 0}            |
            | BruteForce    | 145.0 |   16.1 |           {'a': 5, 'lv': 0}            |
            +---------------+-------+--------+----------------------------------------+

            >>> MRE = MREstimator(q=16, m=16, n=16, k=142, r=4)
            >>> MRE.table(show_all_parameters=1)
            +---------------+----------------------------------------------------------+
            |               |                         estimate                         |
            +---------------+-------+--------+-----------------------------------------+
            | algorithm     |  time | memory |                parameters               |
            +---------------+-------+--------+-----------------------------------------+
            | SupportMinors | 164.0 |   38.1 | {'a': 5, 'lv': 0, 'b': 6, 'nprime': 11} |
            | KernelSearch  | 160.2 |   17.2 |            {'a': 8, 'lv': 0}            |
            | BigK          | 226.8 |   17.2 |            {'a': 0, 'lv': 0}            |
            | Minors        | 170.9 |   38.6 |            {'a': 7, 'lv': 0}            |
            | BruteForce    | 195.1 |   17.2 |            {'a': 8, 'lv': 0}            |
            +---------------+-------+--------+-----------------------------------------+

            >>> if skip_long_doctests:
            ...     pytest.skip()
            >>> MRE = MREstimator(q=16, m=19, n=19, k=109, r=8)
            >>> MRE.table(show_all_parameters=1)
            +---------------+----------------------------------------------------------+
            |               |                         estimate                         |
            +---------------+-------+--------+-----------------------------------------+
            | algorithm     |  time | memory |                parameters               |
            +---------------+-------+--------+-----------------------------------------+
            | SupportMinors | 209.3 |   50.4 | {'a': 3, 'lv': 1, 'b': 9, 'nprime': 16} |
            | KernelSearch  | 208.7 |   17.3 |            {'a': 5, 'lv': 0}            |
            | BigK          | 427.1 |   17.3 |            {'a': 0, 'lv': 0}            |
            | Minors        | 218.2 |   59.5 |            {'a': 4, 'lv': 0}            |
            | BruteForce    | 229.6 |   17.3 |            {'a': 5, 'lv': 0}            |
            +---------------+-------+--------+-----------------------------------------+

            >>> MRE = MREstimator(q=16, m=19, n=19, k=167, r=6)
            >>> MRE.table(show_all_parameters=1)
            +---------------+----------------------------------------------------------+
            |               |                         estimate                         |
            +---------------+-------+--------+-----------------------------------------+
            | algorithm     |  time | memory |                parameters               |
            +---------------+-------+--------+-----------------------------------------+
            | SupportMinors | 233.5 |   52.5 | {'a': 5, 'lv': 0, 'b': 9, 'nprime': 14} |
            | KernelSearch  | 232.7 |   17.9 |            {'a': 8, 'lv': 0}            |
            | BigK          | 347.8 |   17.9 |            {'a': 0, 'lv': 0}            |
            | Minors        | 245.3 |   50.8 |            {'a': 7, 'lv': 0}            |
            | BruteForce    | 264.5 |   17.9 |            {'a': 8, 'lv': 0}            |
            +---------------+-------+--------+-----------------------------------------+

            >>> MRE = MREstimator(q=16, m=21, n=21, k=189, r=7)
            >>> MRE.table(show_all_parameters=1)
            +---------------+-----------------------------------------------------------+
            |               |                          estimate                         |
            +---------------+-------+--------+------------------------------------------+
            | algorithm     |  time | memory |                parameters                |
            +---------------+-------+--------+------------------------------------------+
            | SupportMinors | 273.9 |   76.3 | {'a': 4, 'lv': 0, 'b': 14, 'nprime': 17} |
            | KernelSearch  | 270.4 |   18.4 |            {'a': 8, 'lv': 0}             |
            | BigK          | 448.6 |   18.4 |            {'a': 0, 'lv': 0}             |
            | Minors        | 287.0 |   60.0 |            {'a': 7, 'lv': 0}             |
            | BruteForce    | 321.1 |   18.4 |            {'a': 8, 'lv': 0}             |
            +---------------+-------+--------+------------------------------------------+

            >>> MRE = MREstimator(q=16, m=22, n=22, k=254, r=6)
            >>> MRE.table(show_all_parameters=1)
            +---------------+-----------------------------------------------------------+
            |               |                          estimate                         |
            +---------------+-------+--------+------------------------------------------+
            | algorithm     |  time | memory |                parameters                |
            +---------------+-------+--------+------------------------------------------+
            | SupportMinors | 298.5 |   60.7 | {'a': 7, 'lv': 0, 'b': 10, 'nprime': 15} |
            | KernelSearch  | 304.4 |   18.9 |            {'a': 11, 'lv': 0}            |
            | BigK          | 421.4 |   18.9 |            {'a': 0, 'lv': 0}             |
            | Minors        | 314.9 |   33.2 |            {'a': 11, 'lv': 0}            |
            | BruteForce    | 324.5 |   18.9 |            {'a': 11, 'lv': 0}            |
            +---------------+-------+--------+------------------------------------------+
            """
        super(MREstimator, self).table(show_quantum_complexity=show_quantum_complexity,
                                       show_tilde_o_time=show_tilde_o_time,
                                       show_all_parameters=show_all_parameters,
                                       precision=precision, truncate=truncate,
                                       *args, **kwargs)
