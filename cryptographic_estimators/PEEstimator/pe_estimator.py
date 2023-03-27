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


from ..PEEstimator.pe_algorithm import PEAlgorithm
from ..PEEstimator.pe_problem import PEProblem
from ..base_estimator import BaseEstimator
from math import inf


class PEEstimator(BaseEstimator):
    """
    Construct an instance of Permutation Code Equivalence Estimator

    INPUT:

    - ``n`` -- code length
    - ``k`` -- code dimension
    - ``q`` -- field size
    - ``excluded_algorithms`` -- a list/tuple of excluded algorithms (default: None)
    - ``sd_parameters`` -- dictionary of parameters for SDEstimator used as a subroutine by some algorithms (default: {})
    - ``nsolutions`` -- no. of solutions

    """
    excluded_algorithms_by_default = []

    def __init__(self, n: int, k: int, q: int, memory_bound=inf, **kwargs):  # Add estimator parameters
        if not kwargs.get("excluded_algorithms"):
            kwargs["excluded_algorithms"] = []

        kwargs["excluded_algorithms"] += self.excluded_algorithms_by_default
        super(PEEstimator, self).__init__(
            PEAlgorithm, PEProblem(n, k, q, memory_bound=memory_bound, **kwargs), **kwargs)


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

            sage: from cryptographic_estimators.PEEstimator import PEEstimator
            sage: A = PEEstimator(n=60, k=20, q=7)
            sage: A.table(precision=3, show_all_parameters=1)
            +-----------+-------------------------------+
            |           |            estimate           |
            +-----------+---------+--------+------------+
            | algorithm |    time | memory | parameters |
            +-----------+---------+--------+------------+
            | Leon      |  34.200 | 11.718 | {'w': 26}  |
            | Beullens  |  29.631 | 11.901 | {'w': 25}  |
            | SSA       | 127.480 | 14.040 |     {}     |
            +-----------+---------+--------+------------+

        TESTS::

            sage: from cryptographic_estimators.PEEstimator import PEEstimator
            sage: A = PEEstimator(n=200, k=100, q=51)
            sage: A.table(precision=3, show_all_parameters=1) # long time
            +-----------+-------------------------------+
            |           |            estimate           |
            +-----------+---------+--------+------------+
            | algorithm |    time | memory | parameters |
            +-----------+---------+--------+------------+
            | Leon      | 115.629 | 35.016 | {'w': 71}  |
            | Beullens  |  99.161 | 61.851 | {'w': 85}  |
            | SSA       | 587.237 | 18.377 |     {}     |
            +-----------+---------+--------+------------+
        """
        super(PEEstimator, self).table(show_quantum_complexity=show_quantum_complexity,
                                       show_tilde_o_time=show_tilde_o_time,
                                       show_all_parameters=show_all_parameters,
                                       precision=precision, truncate=truncate)
