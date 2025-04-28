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

from ..SDFqEstimator.sdfq_algorithm import SDFqAlgorithm
from ..SDFqEstimator.sdfq_problem import SDFqProblem
from ..base_estimator import BaseEstimator
from math import inf


class SDFqEstimator(BaseEstimator):
    excluded_algorithms_by_default = []
    def __init__(self, n: int, k: int, w: int, q: int, memory_bound=inf, **kwargs):
        """Initializes the SDFqEstimator class.

        Args:
            n (int): Code length.
            k (int): Code dimension.
            w (int): Error weight.
            q (int): Base field size.
            memory_bound (float, optional): Memory bound. Defaults to 'inf'.
            excluded_algorithms (list or tuple, optional): A list or tuple of excluded algorithms. Defaults to None.
            nsolutions (int, optional): Number of solutions. Defaults to None.
        """
        if not kwargs.get("excluded_algorithms"):
            kwargs["excluded_algorithms"] = []

        kwargs["excluded_algorithms"] += self.excluded_algorithms_by_default
        super(SDFqEstimator, self).__init__(SDFqAlgorithm, SDFqProblem(
            n, k, w, q, memory_bound=memory_bound, **kwargs), **kwargs)

    def table(self, show_quantum_complexity=0, show_tilde_o_time=0,
                       show_all_parameters=0, precision=1, truncate=0):
        """Print table describing the complexity of each algorithm and its optimal parameters.
    
        Args:
            show_quantum_complexity (int): Whether to show quantum time complexity (default: 0).
            show_tilde_o_time (int): Whether to show Ō time complexity (default: 0).
            show_all_parameters (int): Whether to show all optimization parameters (default: 0).
            precision (int): Number of decimal digits to output (default: 1).
            truncate (int): Whether to truncate rather than round the output (default: 0).

        Examples:
            >>> from cryptographic_estimators.SDFqEstimator import SDFqEstimator
            >>> A = SDFqEstimator(n=100,k=50,w=10,q=5)
            >>> A.table()
            +-------------+---------------+
            |             |    estimate   |
            +-------------+------+--------+
            | algorithm   | time | memory |
            +-------------+------+--------+
            | Prange      | 29.9 |   13.5 |
            | Stern       | 24.3 |   23.9 |
            | LeeBrickell | 25.4 |   13.5 |
            +-------------+------+--------+

        Tests:
            >>> from cryptographic_estimators.SDFqEstimator import SDFqEstimator
            >>> A = SDFqEstimator(961,771,48,31)
            >>> A.table(precision=3, show_all_parameters=1)
            +-------------+-------------------------------------+
            |             |               estimate              |
            +-------------+---------+--------+------------------+
            | algorithm   |    time | memory |    parameters    |
            +-------------+---------+--------+------------------+
            | Prange      | 151.310 | 19.794 |        {}        |
            | Stern       | 129.059 | 42.016 | {'p': 2, 'l': 7} |
            | LeeBrickell | 140.319 | 21.808 |     {'p': 2}     |
            +-------------+---------+--------+------------------+
        """
        super(SDFqEstimator, self).table(show_quantum_complexity=show_quantum_complexity,
                                       show_tilde_o_time=show_tilde_o_time,
                                       show_all_parameters=show_all_parameters,
                                       precision=precision, truncate=truncate)
