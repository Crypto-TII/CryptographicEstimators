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

from ..SDFqEstimator.sdfq_algorithm import SDFqAlgorithm
from ..SDFqEstimator.sdfq_problem import SDFqProblem
from ..base_estimator import BaseEstimator
from math import inf


class SDFqEstimator(BaseEstimator):
    """ 

    INPUT:

    - ``n`` -- code length
    - ``k`` -- code dimension
    - ``w`` -- error weight
    - ``q`` -- base field size
    - ``excluded_algorithms`` -- a list/tuple of excluded algorithms (default: None)
    - ``nsolutions`` -- no. of solutions

    """
    excluded_algorithms_by_default = []

    def __init__(self, n: int, k: int, w: int, q: int, memory_bound=inf, **kwargs):
        if not kwargs.get("excluded_algorithms"):
            kwargs["excluded_algorithms"] = []

        kwargs["excluded_algorithms"] += self.excluded_algorithms_by_default
        super(SDFqEstimator, self).__init__(SDFqAlgorithm, SDFqProblem(
            n, k, w, q, memory_bound=memory_bound, **kwargs), **kwargs)

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

            sage: from cryptographic_estimators.SDFqEstimator import SDFqEstimator
            sage: A = SDFqEstimator(n=100,k=50,w=10,q=5)
            sage: A.table()
            +-------------+---------------+
            |             |    estimate   |
            +-------------+------+--------+
            | algorithm   | time | memory |
            +-------------+------+--------+
            | Prange      | 29.9 |   13.5 |
            | Stern       | 24.3 |   23.9 |
            | LeeBrickell | 25.4 |   13.5 |
            +-------------+------+--------+

        TESTS::

            sage: from cryptographic_estimators.SDFqEstimator import SDFqEstimator
            sage: A = SDFqEstimator(961,771,48,31)
            sage: A.table(precision=3, show_all_parameters=1) # long time
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
