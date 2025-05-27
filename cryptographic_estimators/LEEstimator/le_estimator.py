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


import pytest
from ..LEEstimator.le_algorithm import LEAlgorithm
from ..LEEstimator.le_problem import LEProblem
from ..base_estimator import BaseEstimator
from math import inf

class LEEstimator(BaseEstimator):
    excluded_algorithms_by_default = []
    def __init__(self, n: int, k: int, q: int, memory_bound=inf, **kwargs):  # Add estimator parameters
        """Construct an instance of the Linear Code Equivalence Estimator.

        Args:
            n (int): Code length
            k (int): Code dimension
            q (int): Field size
            excluded_algorithms: A list/tuple of excluded algorithms (default: None)
            nsolutions: No. of solutions
        """
        if not kwargs.get("excluded_algorithms"):
            kwargs["excluded_algorithms"] = []

        kwargs["excluded_algorithms"] += self.excluded_algorithms_by_default
        super(LEEstimator, self).__init__(
            LEAlgorithm, LEProblem(n, k, q, memory_bound=memory_bound, **kwargs), **kwargs)

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
            >>> from cryptographic_estimators.LEEstimator import LEEstimator
            >>> A = LEEstimator(n=30, k=20, q=251)
            >>> A.table(show_all_parameters=1)
            +-----------+-----------------------------------------+
            |           |                 estimate                |
            +-----------+------+--------+-------------------------+
            | algorithm | time | memory |        parameters       |
            +-----------+------+--------+-------------------------+
            | Leon      | 35.1 |   12.2 |         {'w': 9}        |
            | Beullens  | 29.7 |   14.4 |        {'w': 11}        |
            | BBPS      | 26.6 |   12.2 | {'w': 12, 'w_prime': 9} |
            +-----------+------+--------+-------------------------+

        Tests:
            >>> if skip_long_doctests:
            ...     pytest.skip()
            >>> from cryptographic_estimators.LEEstimator import LEEstimator
            >>> A = LEEstimator(n=200, k=110, q=31)
            >>> A.table(precision=3, show_all_parameters=1) # long time
            +-----------+---------------------------------------------+
            |           |                   estimate                  |
            +-----------+---------+--------+--------------------------+
            | algorithm |    time | memory |        parameters        |
            +-----------+---------+--------+--------------------------+
            | Leon      | 103.038 | 33.624 |        {'w': 58}         |
            | Beullens  | 123.109 | 42.252 |        {'w': 79}         |
            | BBPS      |  98.511 | 33.624 | {'w': 95, 'w_prime': 59} |
            +-----------+---------+--------+--------------------------+
        """
        super(LEEstimator, self).table(show_quantum_complexity=show_quantum_complexity,
                                       show_tilde_o_time=show_tilde_o_time,
                                       show_all_parameters=show_all_parameters,
                                       precision=precision, truncate=truncate,
                                       *args, **kwargs)
