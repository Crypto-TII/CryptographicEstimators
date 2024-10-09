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
from ..PEEstimator.pe_algorithm import PEAlgorithm
from ..PEEstimator.pe_problem import PEProblem
from ..base_estimator import BaseEstimator
from math import inf


class PEEstimator(BaseEstimator):
    def __init__(self, n: int, k: int, q: int, memory_bound=inf, **kwargs):
        """Construct an instance of Permutation Code Equivalence Estimator.

        Args:
            n (int): Code length.
            k (int): Code dimension.
            q (int): Field size.
            memory_bound (float): Memory bound (default: inf).
            **kwargs: Additional keyword arguments.
                excluded_algorithms (list/tuple): A list/tuple of excluded algorithms (default: None).
                sd_parameters (dict): Dictionary of parameters for SDEstimator used as a subroutine by some algorithms (default: {}).
                nsolutions (int): No. of solutions.
        """
        if not kwargs.get("excluded_algorithms"):
            kwargs["excluded_algorithms"] = []

        kwargs["excluded_algorithms"] += self.excluded_algorithms_by_default
        super(PEEstimator, self).__init__(
            PEAlgorithm, PEProblem(n, k, q, memory_bound=memory_bound, **kwargs), **kwargs)


    def table(self, show_quantum_complexity=0, show_tilde_o_time=0,
              show_all_parameters=0, precision=1, truncate=0):
        """Print table describing the complexity of each algorithm and its optimal parameters.
    
        Args:
            show_quantum_complexity (int): Show quantum time complexity (default: true)
            show_tilde_o_time (int): Show Ō time complexity (default: true)
            show_all_parameters (int): Show all optimization parameters (default: true)
            precision (int): Number of decimal digits output (default: 1)
            truncate (int): Truncate rather than round the output (default: false)

        Examples:
            >>> from cryptographic_estimators.PEEstimator import PEEstimator
            >>> A = PEEstimator(n=60, k=20, q=7)
            >>> A.table(precision=3, show_all_parameters=1)
            +-----------+-------------------------------+
            |           |            estimate           |
            +-----------+---------+--------+------------+
            | algorithm |    time | memory | parameters |
            +-----------+---------+--------+------------+
            | Leon      |  33.274 | 11.718 | {'w': 25}  |
            | Beullens  |  29.631 | 11.901 | {'w': 25}  |
            | SSA       | 127.480 | 14.040 |     {}     |
            +-----------+---------+--------+------------+

        Tests:
            >>> if skip_long_doctests:
            ...     pytest.skip()
            >>> from cryptographic_estimators.PEEstimator import PEEstimator
            >>> A = PEEstimator(n=150, k=100, q=51)
            >>> A.table(precision=3, show_all_parameters=1) # long time
            +-----------+-------------------------------+
            |           |            estimate           |
            +-----------+---------+--------+------------+
            | algorithm |    time | memory | parameters |
            +-----------+---------+--------+------------+
            | Leon      |  82.588 | 34.601 | {'w': 33}  |
            | Beullens  |  72.962 | 44.308 | {'w': 41}  |
            | SSA       | 302.551 | 17.377 |     {}     |
            +-----------+---------+--------+------------+
        """
        super(PEEstimator, self).table(show_quantum_complexity=show_quantum_complexity,
                                       show_tilde_o_time=show_tilde_o_time,
                                       show_all_parameters=show_all_parameters,
                                       precision=precision, truncate=truncate)
