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
