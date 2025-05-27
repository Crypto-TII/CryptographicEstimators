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
from .bike_algorithm import BIKEAlgorithm
from .bike_problem import BIKEProblem
from ..base_estimator import BaseEstimator
from math import inf
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

class BIKEEstimator(BaseEstimator):
    excluded_algorithms_by_default = []
    def __init__(self, r: int, w: int, t: int, memory_bound=inf, **kwargs):
        """Construct an instance of BIKEEstimator.

        Args:
            excluded_algorithm: A list/tuple of excluded algorithms (default: None)
        """
        super(BIKEEstimator, self).__init__(
            BIKEAlgorithm,
            BIKEProblem(r=r, w=w, t=t, memory_bound=memory_bound, **kwargs),
            **kwargs
        )
        self._estimator_type = "scheme"

    def table(self, show_quantum_complexity=0, show_tilde_o_time=0,
              show_all_parameters=0, precision=1, truncate=0, *args, **kwargs):
        """Print table describing the complexity of each algorithm and its optimal parameters.
    
        Args:
            show_quantum_complexity (int): Show quantum time complexity (default: False)
            show_tilde_o_time (int): Show Ō time complexity (default: False)
            show_all_parameters (int): Show all optimization parameters (default: False)
            precision (int): Number of decimal digits output (default: 1)
            truncate (int): Truncate rather than round the output (default: False)

        Examples:
            >>> from cryptographic_estimators.BIKEEstimator import BIKEEstimator
            >>> A = BIKEEstimator(100, 10, 10)
            >>> A.table()
            +-------------+------------------+---------------+
            |             |                  |    estimate   |
            +-------------+------------------+------+--------+
            | algorithm   |   attack_type    | time | memory |
            +-------------+------------------+------+--------+
            | SDKeyAttack |   key-recovery   | 20.2 |   15.5 |
            | SDMsgAttack | message-recovery | 21.2 |   17.4 |
            +-------------+------------------+------+--------+

            >>> from cryptographic_estimators.BIKEEstimator import BIKEEstimator
            >>> A = BIKEEstimator(150, 12, 11)
            >>> A.table(show_all_parameters=1)
            +-------------+------------------+--------------------------------------------------------------------+
            |             |                  |                              estimate                              |
            +-------------+------------------+------+--------+----------------------------------------------------+
            | algorithm   |   attack_type    | time | memory |                     parameters                     |
            +-------------+------------------+------+--------+----------------------------------------------------+
            | SDKeyAttack |   key-recovery   | 21.8 |   16.6 | {'r': 5, 'p': 1, 'l': 9, 'SD-algorithm': 'Stern'}  |
            | SDMsgAttack | message-recovery | 22.8 |   20.7 | {'r': 5, 'p': 2, 'l': 13, 'SD-algorithm': 'Stern'} |
            +-------------+------------------+------+--------+----------------------------------------------------+

        Tests:
            >>> if skip_long_doctests:
            ...     pytest.skip()
            >>> from cryptographic_estimators.BIKEEstimator import BIKEEstimator
            >>> A = BIKEEstimator(3000, 50, 45)
            >>> A.table(show_all_parameters=1) # long time
            +-------------+------------------+--------------------------------------------------------------------+
            |             |                  |                              estimate                              |
            +-------------+------------------+------+--------+----------------------------------------------------+
            | algorithm   |   attack_type    | time | memory |                     parameters                     |
            +-------------+------------------+------+--------+----------------------------------------------------+
            | SDKeyAttack |   key-recovery   | 57.0 |   33.7 | {'r': 9, 'p': 2, 'l': 41, 'SD-algorithm': 'Stern'} |
            | SDMsgAttack | message-recovery | 58.3 |   33.7 | {'r': 9, 'p': 2, 'l': 41, 'SD-algorithm': 'Stern'} |
            +-------------+------------------+------+--------+----------------------------------------------------+
        """
        super(BIKEEstimator, self).table(show_quantum_complexity=show_quantum_complexity,
                                         show_tilde_o_time=show_tilde_o_time,
                                         show_all_parameters=show_all_parameters,
                                         precision=precision, truncate=truncate,
                                         *args, **kwargs)
