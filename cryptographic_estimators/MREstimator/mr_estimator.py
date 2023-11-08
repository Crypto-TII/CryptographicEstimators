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


from .mr_algorithm import MRAlgorithm
from .mr_problem import MRProblem
from .mr_constants import *
from ..base_estimator import BaseEstimator
from math import inf


class MREstimator(BaseEstimator):
    """
    Construct an instance of MREstimator

    INPUT:

    - ``excluded_algorithm`` -- A list/tuple of excluded algorithms (default: None)

    """
    excluded_algorithms_by_default = []

    def __init__(self, q: int, m: int, n: int, k: int, r: int, memory_bound=inf, **kwargs):
        super(MREstimator, self).__init__(
            MRAlgorithm,
            MRProblem(q, m, n, k, r, memory_bound=memory_bound, **kwargs),
            **kwargs
        )

    def table(self, show_quantum_complexity=0, show_tilde_o_time=0,
              show_all_parameters=0, precision=1, truncate=0):
        """
        Print table describing the complexity of each algorithm and its optimal parameters

        INPUT:

        - ``show_quantum_complexity`` -- show quantum time complexity (default: False)
        - ``show_tilde_o_time`` -- show Ō time complexity (default: False)
        - ``show_all_parameters`` -- show all optimization parameters (default: False)
        - ``precision`` -- number of decimal digits output (default: 1)
        - ``truncate`` -- truncate rather than round the output (default: False)

        EXAMPLES::

            sage: from cryptographic_estimators.MREstimator import MREstimator
            sage: MRE = MREstimator(q=7, m=9, n=10, k=15, r=4)
            sage: sage
            +---------------+---------------------------------------------------------------------------------------+
            |               |                                        estimate                                       |
            +---------------+-------+--------+----------------------------------------------------------------------+
            | algorithm     |  time | memory |                              parameters                              |
            +---------------+-------+--------+----------------------------------------------------------------------+
            | SupportMinors |  38.8 |   13.0 | {'a': 1, 'lv': 0, 'b': 1, 'nprime': 8, 'variant': 'block_wiedemann'} |
            | KernelSearch  |  32.7 |   11.5 |                          {'a': 1, 'lv': 0}                           |
            | BigK          | 131.4 |   13.1 |                          {'a': 0, 'lv': 0}                           |
            +---------------+-------+--------+----------------------------------------------------------------------+


        TESTS:

            sage: from cryptographic_estimators.MREstimator import MREstimator
            sage: MRE = MREstimator(q=16, m=15, n=15, k=78, r=6)
            sage: MRE.table(show_all_parameters=1)
            +---------------+---------------------------------------------------------------------------------------+
            |               |                                        estimate                                       |
            +---------------+-------+--------+----------------------------------------------------------------------+
            | algorithm     |  time | memory |                              parameters                              |
            +---------------+-------+--------+----------------------------------------------------------------------+
            | SupportMinors | 144.0 |   11.8 | {'a': 5, 'lv': 0, 'b': 1, 'nprime': 8, 'variant': 'block_wiedemann'} |
            | KernelSearch  | 147.0 |   14.3 |                          {'a': 4, 'lv': 3}                           |
            | BigK          | 153.5 |   13.8 |                          {'a': 5, 'lv': 3}                           |
            +---------------+-------+--------+----------------------------------------------------------------------+




        """
        super(MREstimator, self).table(show_quantum_complexity=show_quantum_complexity,
                                          show_tilde_o_time=show_tilde_o_time,
                                          show_all_parameters=show_all_parameters,
                                          precision=precision, truncate=truncate)
