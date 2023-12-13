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
from ..base_estimator import BaseEstimator
from math import inf


class MREstimator(BaseEstimator):
    """
    Construct an instance of MREstimator

    INPUT:
    - ``q`` -- order of the finite field
    - ``m`` -- number of rows of the input matrices
    - ``n`` -- number of columns of the input matrices
    - ``k`` -- length of the solution vector
    - ``r`` -- target rank
    - ``memory_bound`` -- maximum allowed memory to use for solving the problem (default: inf)
    - ``excluded_algorithm`` -- A list/tuple of excluded algorithms (default: None)

    EXAMPLES::

        sage: from cryptographic_estimators.MREstimator import MREstimator
        sage: MRE = MREstimator(q=16, m=15, n=15, k=78, r=6)

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
            sage: MRE.table(show_all_parameters=1)
            +---------------+---------------------------------------------------------------------------------------+
            |               |                                        estimate                                       |
            +---------------+-------+--------+----------------------------------------------------------------------+
            | algorithm     |  time | memory |                              parameters                              |
            +---------------+-------+--------+----------------------------------------------------------------------+
            | SupportMinors |  38.8 |   13.0 | {'a': 1, 'lv': 0, 'b': 1, 'nprime': 8, 'variant': 'block_wiedemann'} |
            | KernelSearch  |  33.2 |   11.5 |                          {'a': 1, 'lv': 0}                           |
            | BigK          | 132.5 |   13.1 |                          {'a': 0, 'lv': 0}                           |
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
            | KernelSearch  | 147.7 |   14.3 |                          {'a': 4, 'lv': 3}                           |
            | BigK          | 154.7 |   13.8 |                          {'a': 5, 'lv': 3}                           |
            +---------------+-------+--------+----------------------------------------------------------------------+

            sage: MRE = MREstimator(q=16, m=16, n=16, k=142, r=4)
            sage: MRE.table(show_all_parameters=1)
            +---------------+---------------------------------------------------------------------------------------+
            |               |                                        estimate                                       |
            +---------------+-------+--------+----------------------------------------------------------------------+
            | algorithm     |  time | memory |                              parameters                              |
            +---------------+-------+--------+----------------------------------------------------------------------+
            | SupportMinors | 165.9 |   18.0 | {'a': 8, 'lv': 0, 'b': 2, 'nprime': 8, 'variant': 'block_wiedemann'} |
            | KernelSearch  | 159.4 |   13.8 |                          {'a': 8, 'lv': 0}                           |
            | BigK          | 230.8 |   17.2 |                          {'a': 0, 'lv': 0}                           |
            +---------------+-------+--------+----------------------------------------------------------------------+

            sage: MRE = MREstimator(q=16, m=19, n=19, k=109, r=8)
            sage: MRE.table(show_all_parameters=1)
            +---------------+----------------------------------------------------------------------------------------+
            |               |                                        estimate                                        |
            +---------------+-------+--------+-----------------------------------------------------------------------+
            | algorithm     |  time | memory |                               parameters                              |
            +---------------+-------+--------+-----------------------------------------------------------------------+
            | SupportMinors | 209.6 |   23.5 | {'a': 5, 'lv': 0, 'b': 2, 'nprime': 14, 'variant': 'block_wiedemann'} |
            | KernelSearch  | 207.4 |   14.9 |                           {'a': 5, 'lv': 0}                           |
            | BigK          | 431.1 |   17.4 |                           {'a': 0, 'lv': 0}                           |
            +---------------+-------+--------+-----------------------------------------------------------------------+

            sage: MRE = MREstimator(q=16, m=19, n=19, k=167, r=6)
            sage: MRE.table(show_all_parameters=1)
            +---------------+----------------------------------------------------------------------------------------+
            |               |                                        estimate                                        |
            +---------------+-------+--------+-----------------------------------------------------------------------+
            | algorithm     |  time | memory |                               parameters                              |
            +---------------+-------+--------+-----------------------------------------------------------------------+
            | SupportMinors | 236.3 |   20.9 | {'a': 8, 'lv': 0, 'b': 2, 'nprime': 11, 'variant': 'block_wiedemann'} |
            | KernelSearch  | 231.7 |   14.6 |                           {'a': 8, 'lv': 0}                           |
            | BigK          | 351.8 |   17.9 |                           {'a': 0, 'lv': 0}                           |
            +---------------+-------+--------+-----------------------------------------------------------------------+

            sage: MRE = MREstimator(q=16, m=21, n=21, k=189, r=7)
            sage: MRE.table(show_all_parameters=1)
            +---------------+----------------------------------------------------------------------------------------+
            |               |                                        estimate                                        |
            +---------------+-------+--------+-----------------------------------------------------------------------+
            | algorithm     |  time | memory |                               parameters                              |
            +---------------+-------+--------+-----------------------------------------------------------------------+
            | SupportMinors | 274.5 |   51.0 | {'a': 6, 'lv': 0, 'b': 8, 'nprime': 15, 'variant': 'block_wiedemann'} |
            | KernelSearch  | 269.2 |   15.5 |                           {'a': 8, 'lv': 0}                           |
            | BigK          | 452.6 |   18.4 |                           {'a': 0, 'lv': 0}                           |
            +---------------+-------+--------+-----------------------------------------------------------------------+

            sage: MRE = MREstimator(q=16, m=22, n=22, k=254, r=6)
            sage: MRE.table(show_all_parameters=1)
            +---------------+-----------------------------------------------------------------------------------------+
            |               |                                         estimate                                        |
            +---------------+-------+--------+------------------------------------------------------------------------+
            | algorithm     |  time | memory |                               parameters                               |
            +---------------+-------+--------+------------------------------------------------------------------------+
            | SupportMinors | 301.2 |   17.6 | {'a': 11, 'lv': 0, 'b': 1, 'nprime': 11, 'variant': 'block_wiedemann'} |
            | KernelSearch  | 302.8 |   14.5 |                           {'a': 11, 'lv': 0}                           |
            | BigK          | 425.4 |   18.9 |                           {'a': 0, 'lv': 0}                            |
            +---------------+-------+--------+------------------------------------------------------------------------+

            """
        super(MREstimator, self).table(show_quantum_complexity=show_quantum_complexity,
                                       show_tilde_o_time=show_tilde_o_time,
                                       show_all_parameters=show_all_parameters,
                                       precision=precision, truncate=truncate)
