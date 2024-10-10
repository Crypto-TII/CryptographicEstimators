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
              show_all_parameters=0, precision=1, truncate=0):
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
            +-----------+------------------------------------------+
            |           |                 estimate                 |
            +-----------+------+--------+--------------------------+
            | algorithm | time | memory |        parameters        |
            +-----------+------+--------+--------------------------+
            | Leon      | 35.1 |   12.2 |         {'w': 9}         |
            | Beullens  | 29.7 |   14.4 |        {'w': 11}         |
            | BBPS      | 25.3 |   12.2 | {'w': 12, 'w_prime': 10} |
            +-----------+------+--------+--------------------------+

        Tests:
            >>> if skip_long_doctests:
            ...     pytest.skip()
            >>> from cryptographic_estimators.LEEstimator import LEEstimator
            >>> A = LEEstimator(n=200, k=110, q=31)
            >>> A.table(precision=3, show_all_parameters=1) # long time
            +-----------+----------------------------------------------+
            |           |                   estimate                   |
            +-----------+---------+--------+---------------------------+
            | algorithm |    time | memory |         parameters        |
            +-----------+---------+--------+---------------------------+
            | Leon      | 103.038 | 33.624 |         {'w': 58}         |
            | Beullens  | 123.109 | 42.252 |         {'w': 79}         |
            | BBPS      |  95.960 | 33.624 | {'w': 101, 'w_prime': 59} |
            +-----------+---------+--------+---------------------------+
        """
        super(LEEstimator, self).table(show_quantum_complexity=show_quantum_complexity,
                                       show_tilde_o_time=show_tilde_o_time,
                                       show_all_parameters=show_all_parameters,
                                       precision=precision, truncate=truncate)
