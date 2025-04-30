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
from ..PEEstimator.pe_algorithm import PEAlgorithm
from ..PEEstimator.pe_problem import PEProblem
from ..base_estimator import BaseEstimator
from math import inf


class PEEstimator(BaseEstimator):
    def __init__(self, n: int, k: int, q: int, memory_bound=inf, **kwargs):
        """Construct an instance of Permutation Code Equivalence Estimator.

        Args:
            n (int): Code length.
            k (int): Code dimension.
            q (int): Field size.
            memory_bound (float): Memory bound (default: inf).
            **kwargs: Additional keyword arguments.
                excluded_algorithms (list/tuple): A list/tuple of excluded algorithms (default: None).
                sd_parameters (dict): Dictionary of parameters for SDEstimator used as a subroutine by some algorithms (default: {}).
                nsolutions (int): No. of solutions.
        """
        if not kwargs.get("excluded_algorithms"):
            kwargs["excluded_algorithms"] = []

        kwargs["excluded_algorithms"] += self.excluded_algorithms_by_default
        super(PEEstimator, self).__init__(
            PEAlgorithm, PEProblem(n, k, q, memory_bound=memory_bound, **kwargs), **kwargs)


    def table(self, show_quantum_complexity=0, show_tilde_o_time=0,
              show_all_parameters=0, precision=1, truncate=0, *args, **kwargs):
        """Print table describing the complexity of each algorithm and its optimal parameters.
    
        Args:
            show_quantum_complexity (int): Show quantum time complexity (default: true)
            show_tilde_o_time (int): Show Ō time complexity (default: true)
            show_all_parameters (int): Show all optimization parameters (default: true)
            precision (int): Number of decimal digits output (default: 1)
            truncate (int): Truncate rather than round the output (default: false)

        Examples:
            >>> from cryptographic_estimators.PEEstimator import PEEstimator
            >>> A = PEEstimator(n=60, k=20, q=7)
            >>> A.table(precision=3, show_all_parameters=1)
            +-----------+-------------------------------+
            |           |            estimate           |
            +-----------+---------+--------+------------+
            | algorithm |    time | memory | parameters |
            +-----------+---------+--------+------------+
            | Leon      |  33.274 | 11.718 | {'w': 25}  |
            | Beullens  |  29.631 | 11.901 | {'w': 25}  |
            | SSA       | 127.480 | 14.040 |     {}     |
            +-----------+---------+--------+------------+

        Tests:
            >>> if skip_long_doctests:
            ...     pytest.skip()
            >>> from cryptographic_estimators.PEEstimator import PEEstimator
            >>> A = PEEstimator(n=150, k=100, q=51)
            >>> A.table(precision=3, show_all_parameters=1) # long time
            +-----------+-------------------------------+
            |           |            estimate           |
            +-----------+---------+--------+------------+
            | algorithm |    time | memory | parameters |
            +-----------+---------+--------+------------+
            | Leon      |  82.588 | 34.601 | {'w': 33}  |
            | Beullens  |  72.962 | 44.308 | {'w': 41}  |
            | SSA       | 302.551 | 17.377 |     {}     |
            +-----------+---------+--------+------------+
        """
        super(PEEstimator, self).table(show_quantum_complexity=show_quantum_complexity,
                                       show_tilde_o_time=show_tilde_o_time,
                                       show_all_parameters=show_all_parameters,
                                       precision=precision, truncate=truncate,
                                       *args, **kwargs)
