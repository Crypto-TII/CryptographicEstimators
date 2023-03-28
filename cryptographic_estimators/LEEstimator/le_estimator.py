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


from ..LEEstimator.le_algorithm import LEAlgorithm
from ..LEEstimator.le_problem import LEProblem
from ..base_estimator import BaseEstimator
from math import inf

class LEEstimator(BaseEstimator):
    """
    Construct an instance of the Linear Code Equivalence Estimator

    INPUT:

    - ``n`` -- code length
    - ``k`` -- code dimension
    - ``q`` -- field size
    - ``excluded_algorithms`` -- a list/tuple of excluded algorithms (default: None)
    - ``nsolutions`` -- no. of solutions

    """
    excluded_algorithms_by_default = []

    def __init__(self, n: int, k: int, q: int, memory_bound=inf, **kwargs):  # Add estimator parameters
        if not kwargs.get("excluded_algorithms"):
            kwargs["excluded_algorithms"] = []

        kwargs["excluded_algorithms"] += self.excluded_algorithms_by_default
        super(LEEstimator, self).__init__(
            LEAlgorithm, LEProblem(n, k, q, memory_bound=memory_bound, **kwargs), **kwargs)

    def table(self, show_quantum_complexity=0, show_tilde_o_time=0,
              show_all_parameters=0, precision=1, truncate=0):
        """
        Print table describing the complexity of each algorithm and its optimal parameters

        INPUT:

        - ``show_quantum_complexity`` -- show quantum time complexity (default: true)
        - ``show_tilde_o_time`` -- show Ō time complexity (default: true)
        - ``show_all_parameters`` -- show all optimization parameters (default: true)
        - ``precision`` -- number of decimal digits output (default: 1)
        - ``truncate`` -- truncate rather than round the output (default: false)

        EXAMPLES::

            sage: from cryptographic_estimators.LEEstimator import LEEstimator
            sage: A = LEEstimator(n=30, k=20, q=251)
            sage: A.table(show_all_parameters=1)
            +-----------+------------------------------------------+
            |           |                 estimate                 |
            +-----------+------+--------+--------------------------+
            | algorithm | time | memory |        parameters        |
            +-----------+------+--------+--------------------------+
            | Leon      | 34.2 |   12.2 |         {'w': 9}         |
            | Beullens  | 29.7 |   14.4 |        {'w': 11}         |
            | BBPS      | 27.6 |   12.2 | {'w': 14, 'w_prime': 10} |
            +-----------+------+--------+--------------------------+

        TESTS::

            sage: from cryptographic_estimators.LEEstimator import LEEstimator
            sage: A = LEEstimator(n=200, k=110, q=31)
            sage: A.table(precision=3, show_all_parameters=1) # long time
            +-----------+----------------------------------------------+
            |           |                   estimate                   |
            +-----------+---------+--------+---------------------------+
            | algorithm |    time | memory |         parameters        |
            +-----------+---------+--------+---------------------------+
            | Leon      | 105.356 | 33.624 |         {'w': 59}         |
            | Beullens  | 123.109 | 42.252 |         {'w': 79}         |
            | BBPS      |  97.495 | 33.624 | {'w': 102, 'w_prime': 60} |
            +-----------+---------+--------+---------------------------+

        """
        super(LEEstimator, self).table(show_quantum_complexity=show_quantum_complexity,
                                       show_tilde_o_time=show_tilde_o_time,
                                       show_all_parameters=show_all_parameters,
                                       precision=precision, truncate=truncate)
