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


from .regsd_algorithm import RegSDAlgorithm
from .regsd_problem import RegSDProblem
from ..base_estimator import BaseEstimator
from math import inf


class RegSDEstimator(BaseEstimator):
    excluded_algorithms_by_default = []
    def __init__(self, n: int, k: int, w: int, memory_bound=inf, **kwargs):
        """Construct an instance of RegSDEstimator.

        Args:
            n (int): Code length.
            k (int): Code dimension.
            w (int): Error weight.
            memory_bound: Memory bound.
            **kwargs: Additional keyword arguments.
                excluded_algorithms: A list/tuple of excluded algorithms (default: None).
                nsolutions: No. of solutions.
        """
        super(RegSDEstimator, self).__init__(
            RegSDAlgorithm,
            RegSDProblem(n, k, w, memory_bound=memory_bound, **kwargs),
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
            >>> from cryptographic_estimators.RegSDEstimator import RegSDEstimator
            >>> A=RegSDEstimator(n=954, k=582, w=106)
            >>> A.table(show_all_parameters=1)
            +----------------+---------------------------------------------------------------------------------------+
            |                |                                        estimate                                       |
            +----------------+-------+--------+----------------------------------------------------------------------+
            | algorithm      |  time | memory |                              parameters                              |
            +----------------+-------+--------+----------------------------------------------------------------------+
            | RegularISDPerm | 133.4 |   18.8 |                                  {}                                  |
            | RegularISDEnum | 114.8 |   31.1 |                         {'p': 6, 'ell': 20}                          |
            | RegularISDRep  | 112.7 |   60.3 |             {'p': 24, 'ell': 96, 'eps_x': 4, 'eps_y': 0}             |
            | CCJ            | 129.1 |  127.6 |                             {'ell': 118}                             |
            | CCJLin         | 148.9 |   18.4 |                                  {}                                  |
            | SDAttack       | 155.1 |  118.9 | {'r': 6, 'depth': 2, 'p': 32, 'p1': 19, 'l': 212, 'variant': 'BJMM'} |
            +----------------+-------+--------+----------------------------------------------------------------------+

        Tests:
            >>> from cryptographic_estimators.RegSDEstimator import RegSDEstimator
            >>> A=RegSDEstimator(n=2320, k=1210, w=40)
            >>> A.table(show_all_parameters=1)
            +----------------+-----------------------------------------------------------------------------------+
            |                |                                      estimate                                     |
            +----------------+------+--------+-------------------------------------------------------------------+
            | algorithm      | time | memory |                             parameters                            |
            +----------------+------+--------+-------------------------------------------------------------------+
            | RegularISDPerm | 72.0 |   21.3 |                                 {}                                |
            | RegularISDEnum | 57.4 |   28.5 |                        {'p': 4, 'ell': 15}                        |
            | RegularISDRep  | 59.0 |   41.0 |            {'p': 8, 'ell': 34, 'eps_x': 0, 'eps_y': 0}            |
            | CCJ            | 75.8 |   74.7 |                            {'ell': 67}                            |
            | CCJLin         | 83.4 |   21.3 |                                 {}                                |
            | SDAttack       | 59.0 |   27.7 | {'r': 8, 'depth': 2, 'p': 2, 'p1': 1, 'l': 20, 'variant': 'BJMM'} |
            +----------------+------+--------+-------------------------------------------------------------------+
        """
        super(RegSDEstimator, self).table(show_quantum_complexity=show_quantum_complexity,
                                          show_tilde_o_time=show_tilde_o_time,
                                          show_all_parameters=show_all_parameters,
                                          precision=precision, truncate=truncate,
                                          *args, **kwargs)
