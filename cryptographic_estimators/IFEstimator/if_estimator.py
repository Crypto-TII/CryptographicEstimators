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


from .if_algorithm import IFAlgorithm
from .if_problem import IFProblem
from ..base_estimator import BaseEstimator
from math import inf


class IFEstimator(BaseEstimator):
    """
    Construct an instance of Integer Factoring Estimator.
    """
    excluded_algorithms_by_default = []

    def __init__(self, n: int, memory_bound=inf, **kwargs):  # Fill with parameters
        """
        Args:
        - n (int): bit length of RSA integer to be factored
        - memory_bound (int, optional): maximum allowed memory to use for solving the problem (default: infinity)

        """
        super(IFEstimator, self).__init__(
            IFAlgorithm,
            IFProblem(n, memory_bound=memory_bound, **kwargs),
            **kwargs
        )

    def table(self, show_quantum_complexity=0, show_tilde_o_time=0,
              show_all_parameters=0, precision=1, truncate=0, parameters_inside=False,
              *args, **kwargs):
        """Print table describing the complexity of each algorithm and its optimal parameters

        Args:
            - show_quantum_complexity (int, optional) -- show quantum time complexity (default: False)
            - show_tilde_o_time (int, optional) -- show Ō time complexity (default: False)
            - show_all_parameters (int, optional) -- show all optimization parameters (default: False)
            - precision (int, optional) -- number of decimal digits output (default: 1)
            - truncate (int, optional) -- truncate rather than round the output (default: False)
            - parameters_inside (bool): Shows the Problem parameters in the top left corner

        Examples:
            >>> from cryptographic_estimators.IFEstimator import *
            >>> A = IFEstimator(n=4096)
            >>> A.table(show_tilde_o_time=1)
            +---------------+-----------------+------------------+
            |               |     estimate    | tilde_o_estimate |
            +---------------+--------+--------+--------+---------+
            | algorithm     |   time | memory |   time |  memory |
            +---------------+--------+--------+--------+---------+
            | TrialDivision | 2070.0 |   2037 | 2047.0 |    2037 |
            | Lenstra       |  285.0 |   14.6 |  261.0 |    14.6 |
            | GNFS          |  144.6 |   85.5 |  156.5 |    85.5 |
            +---------------+--------+--------+--------+---------+

        Tests:
            >>> from cryptographic_estimators.IFEstimator import *
            >>> A = IFEstimator(n=2048)
            >>> A.table(show_tilde_o_time=1, precision=0)
            +---------------+---------------+------------------+
            |               |    estimate   | tilde_o_estimate |
            +---------------+------+--------+-------+----------+
            | algorithm     | time | memory |  time |   memory |
            +---------------+------+--------+-------+----------+
            | TrialDivision | 1045 |   1014 |  1023 |     1014 |
            | Lenstra       |  199 |     14 |   177 |       14 |
            | GNFS          |  105 |     65 |   117 |       65 |
            +---------------+------+--------+-------+----------+
        """
        super(IFEstimator, self).table(show_quantum_complexity=show_quantum_complexity,
                                       show_tilde_o_time=show_tilde_o_time,
                                       show_all_parameters=show_all_parameters,
                                       precision=precision, truncate=truncate,
                                       parameters_inside=parameters_inside, *args, **kwargs)
