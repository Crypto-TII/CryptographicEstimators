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
              show_all_parameters=0, precision=1, truncate=0):
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
               | OJ1                 | 160.6 |   16.5 |             {}            |
               | OJ2                 | 204.9 |   15.9 |             {}            |
               | GRS                 | 162.2 |   18.2 |             {}            |
               | ImprovedGRS         | 147.2 |   18.0 |             {}            |
               | GuessingEnhancedGRS | 138.3 |   18.1 |          {'t': 1}         |
               | HybridLinearization | 174.4 |   12.4 |         {'t': 15}         |
               | MaxMinors           | 153.0 |   33.0 |     {'a': 12, 'p': 2}     |
               | SupportMinors       | 155.1 |   40.1 | {'b': 1, 'a': 11, 'p': 0} |
               +---------------------+-------+--------+---------------------------+

           Tests:

               >>> from cryptographic_estimators.RankSDEstimator.ranksd_estimator import RankSDEstimator
               >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms import BasisEnumeration,GRS,OJ1,OJ2,HybridLinearization
               >>> RSDE = RankSDEstimator(q=2, m=31, n=33, k=15, r=10, w=2, excluded_algorithms=[BasisEnumeration,GRS,OJ1,OJ2,HybridLinearization])
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


               >>> RSDE = RankSDEstimator(q=2, m=37, n=41, k=18, r=13, w=2, excluded_algorithms=[BasisEnumeration,GRS,OJ1,OJ2,HybridLinearization])
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


               >>> RSDE = RankSDEstimator(q=2, m=43, n=47, k=18, r=17, w=2, excluded_algorithms=[BasisEnumeration,GRS,OJ1,OJ2,HybridLinearization])
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
                                           precision=precision, truncate=truncate)
