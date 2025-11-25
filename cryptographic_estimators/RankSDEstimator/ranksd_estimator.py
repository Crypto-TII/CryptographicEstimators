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


from math import inf
from .ranksd_algorithm import RankSDAlgorithm
from .ranksd_problem import RankSDProblem
from ..base_estimator import BaseEstimator


class RankSDEstimator(BaseEstimator):
    """Construct an instance of RankSDEstimator.

       Args:
           q (int): Base field order.
           m (int): Extension degree.
           n (int): Code length.
           k (int): Code dimension.
           r (int): Target rank.
           memory_bound (float, optional): Maximum allowed memory to use for solving the problem. Defaults to inf.
           **kwargs: Additional keyword arguments.
               excluded_algorithm (list): A list/tuple of excluded algorithms (default: None)

       Examples:
           >>> from cryptographic_estimators.RankSDEstimator.ranksd_estimator import RankSDEstimator
           >>> RSDE = RankSDEstimator(q=2, m=127, n=118, k=48, r=7)
    """
    excluded_algorithms_by_default = []

    def __init__(self, q: int, m: int, n: int, k: int, r: int, memory_bound=inf, **kwargs):  # Fill with parameters
        super(RankSDEstimator, self).__init__(
            RankSDAlgorithm,
            RankSDProblem(q, m, n, k, r, memory_bound=memory_bound, **kwargs),
            **kwargs
        )

    def table(self, show_quantum_complexity=0, show_tilde_o_time=0,
              show_all_parameters=0, precision=1, truncate=0, *args, **kwargs):
        """Print table describing the complexity of each algorithm and its optimal parameters.

           Args:
               show_quantum_complexity (int): Show quantum time complexity (default: 0).
               show_tilde_o_time (int): Show Ō time complexity (default: 0).
               show_all_parameters (int): Show all optimization parameters (default: 0).
               precision (int): Number of decimal digits output (default: 1).
               truncate (int): Truncate rather than round the output (default: 0).

           Examples:
               >>> from cryptographic_estimators.RankSDEstimator.ranksd_estimator import RankSDEstimator
               >>> RSDE = RankSDEstimator(q=2, m=31, n=33, k=15, r=10, w=2)
               >>> RSDE.table(show_all_parameters=1)
               +---------------------+--------------------------------------------+
               |                     |                  estimate                  |
               +---------------------+-------+--------+---------------------------+
               | algorithm           |  time | memory |         parameters        |
               +---------------------+-------+--------+---------------------------+
               | BasisEnumeration    | 206.0 |   17.6 |             {}            |
               | OJ1                 | 151.5 |   16.5 |             {}            |
               | OJ2                 | 220.7 |   15.9 |             {}            |
               | GRS                 | 162.2 |   18.2 |             {}            |
               | ImprovedGRS         | 147.2 |   18.0 |             {}            |
               | GuessingEnhancedGRS | 138.3 |   18.1 |          {'t': 1}         |
               | AnnulatorPolynomial | 174.4 |   12.4 |         {'t': 15}         |
               | MaxMinors           | 153.0 |   33.0 |     {'a': 12, 'p': 2}     |
               | SupportMinors       | 155.1 |   40.1 | {'b': 1, 'a': 11, 'p': 0} |
               +---------------------+-------+--------+---------------------------+

           Tests:

               >>> from cryptographic_estimators.RankSDEstimator.ranksd_estimator import RankSDEstimator
               >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms import BasisEnumeration,GRS,OJ1,OJ2,AnnulatorPolynomial
               >>> RSDE = RankSDEstimator(q=2, m=31, n=33, k=15, r=10, w=2, excluded_algorithms=[BasisEnumeration,GRS,OJ1,OJ2,AnnulatorPolynomial])
               >>> RSDE.table(show_all_parameters=1)
               +---------------------+--------------------------------------------+
               |                     |                  estimate                  |
               +---------------------+-------+--------+---------------------------+
               | algorithm           |  time | memory |         parameters        |
               +---------------------+-------+--------+---------------------------+
               | ImprovedGRS         | 147.2 |   18.0 |             {}            |
               | GuessingEnhancedGRS | 138.3 |   18.1 |          {'t': 1}         |
               | MaxMinors           | 153.0 |   33.0 |     {'a': 12, 'p': 2}     |
               | SupportMinors       | 155.1 |   40.1 | {'b': 1, 'a': 11, 'p': 0} |
               +---------------------+-------+--------+---------------------------+


               >>> RSDE = RankSDEstimator(q=2, m=37, n=41, k=18, r=13, w=2, excluded_algorithms=[BasisEnumeration,GRS,OJ1,OJ2,AnnulatorPolynomial])
               >>> RSDE.table(show_all_parameters=1)
               +---------------------+--------------------------------------------+
               |                     |                  estimate                  |
               +---------------------+-------+--------+---------------------------+
               | algorithm           |  time | memory |         parameters        |
               +---------------------+-------+--------+---------------------------+
               | ImprovedGRS         | 216.5 |   19.3 |             {}            |
               | GuessingEnhancedGRS | 209.5 |   19.4 |          {'t': 6}         |
               | MaxMinors           | 237.7 |   42.7 |     {'a': 15, 'p': 2}     |
               | SupportMinors       | 240.5 |   53.3 | {'b': 2, 'a': 14, 'p': 0} |
               +---------------------+-------+--------+---------------------------+


               >>> RSDE = RankSDEstimator(q=2, m=43, n=47, k=18, r=17, w=2, excluded_algorithms=[BasisEnumeration,GRS,OJ1,OJ2,AnnulatorPolynomial])
               >>> RSDE.table(show_all_parameters=1)
               +---------------------+------------------------------------+
               |                     |              estimate              |
               +---------------------+-------+--------+-------------------+
               | algorithm           |  time | memory |     parameters    |
               +---------------------+-------+--------+-------------------+
               | ImprovedGRS         | 283.6 |   20.4 |         {}        |
               | GuessingEnhancedGRS | 283.6 |   20.4 |      {'t': 0}     |
               | MaxMinors           | 308.8 |   53.8 | {'a': 15, 'p': 2} |
               | SupportMinors       |    -- |     -- |         {}        |
               +---------------------+-------+--------+-------------------+

        """
        super(RankSDEstimator, self).table(show_quantum_complexity=show_quantum_complexity,
                                           show_tilde_o_time=show_tilde_o_time,
                                           show_all_parameters=show_all_parameters,
                                           precision=precision, truncate=truncate,
                                           *args, **kwargs)
