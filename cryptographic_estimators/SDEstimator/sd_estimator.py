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

# ****************************************************************************
# Copyright 2023 Technology Innovation Institute

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


from ..SDEstimator.sd_algorithm import SDAlgorithm
from ..SDEstimator.sd_problem import SDProblem
from ..SDEstimator.SDAlgorithms import BJMMd2, BJMMd3, MayOzerovD2, MayOzerovD3
from ..base_estimator import BaseEstimator
from math import inf


class SDEstimator(BaseEstimator):
    """
    Construct an instance of Syndrome Decoding Estimator

    INPUT:

    - ``n`` -- code length
    - ``k`` -- code dimension
    - ``w`` -- error weight
    - ``excluded_algorithms`` -- a list/tuple of excluded algorithms (default: None)
    - ``nsolutions`` -- no. of solutions

    TODO: Maybe we should add the optional_parameters dictionary here?

    """

    excluded_algorithms_by_default = [BJMMd2, BJMMd3, MayOzerovD2, MayOzerovD3]

    def __init__(self, n: int, k: int, w: int, memory_bound=inf, **kwargs):
        if not kwargs.get("excluded_algorithms"):
            kwargs["excluded_algorithms"] = []

        kwargs["excluded_algorithms"] += self.excluded_algorithms_by_default

        super(SDEstimator, self).__init__(SDAlgorithm, SDProblem(
            n, k, w, memory_bound=memory_bound, **kwargs), **kwargs)

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

        EXAMPLES:

            sage: from cryptographic_estimators.SDEstimator import SDEstimator
            sage: A = SDEstimator(n=100, k=50, w=10)
            sage: A.table()
            +---------------+---------------+
            |               |    estimate   |
            +---------------+------+--------+
            | algorithm     | time | memory |
            +---------------+------+--------+
            | BallCollision | 23.3 |   16.0 |
            | BJMMdw        | 23.4 |   14.7 |
            | BJMMpdw       | 23.3 |   14.3 |
            | BJMM          | 22.8 |   15.0 |
            | BJMM_plus     | 22.8 |   15.0 |
            | BothMay       | 22.4 |   14.7 |
            | Dumer         | 22.7 |   16.4 |
            | MayOzerov     | 22.3 |   14.8 |
            | Prange        | 28.3 |   12.7 |
            | Stern         | 22.3 |   16.0 |
            +---------------+------+--------+

        TESTS:

            sage: from cryptographic_estimators.SDEstimator import SDEstimator
            sage: A = SDEstimator(n=100, k=42, w=13, bit_complexities=1, workfactor_accuracy=25)
            sage: A.table(show_tilde_o_time=1, precision=0) # long time
            +---------------+---------------+------------------+
            |               |    estimate   | tilde_o_estimate |
            +---------------+------+--------+-------+----------+
            | algorithm     | time | memory |  time |   memory |
            +---------------+------+--------+-------+----------+
            | BallCollision |   24 |     16 |    11 |        3 |
            | BJMMdw        |   24 |     14 |    -- |       -- |
            | BJMMpdw       |   24 |     15 |    -- |       -- |
            | BJMM          |   23 |     15 |     9 |        7 |
            | BJMM_plus     |   23 |     15 |    -- |       -- |
            | BothMay       |   23 |     14 |     9 |        7 |
            | Dumer         |   23 |     16 |    11 |        3 |
            | MayOzerov     |   23 |     15 |     9 |        8 |
            | Prange        |   29 |     13 |    11 |        0 |
            | Stern         |   23 |     16 |    11 |        3 |
            +---------------+------+--------+-------+----------+

            sage: from cryptographic_estimators.SDEstimator import SDEstimator
            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import BJMMdw
            sage: A = SDEstimator(3488,2720,64,excluded_algorithms=[BJMMdw])
            sage: A.table(precision=3, show_all_parameters=1) # long time
            +---------------+--------------------------------------------------------------------------------+
            |               |                                    estimate                                    |
            +---------------+---------+---------+------------------------------------------------------------+
            | algorithm     |    time |  memory |                         parameters                         |
            +---------------+---------+---------+------------------------------------------------------------+
            | BallCollision | 151.460 |  49.814 |             {'r': 7, 'p': 4, 'pl': 0, 'l': 39}             |
            | BJMMpdw       | 143.448 |  86.221 |            {'r': 7, 'p': 12, 'p1': 8, 'w2': 0}             |
            | BJMM          | 141.886 | 104.057 | {'r': 7, 'depth': 3, 'p': 16, 'p1': 6, 'p2': 12, 'l': 197} |
            | BJMM_plus     | 142.111 |  97.541 |      {'r': 7, 'p': 14, 'p1': 10, 'l': 167, 'l1': 81}       |
            | BothMay       | 141.711 |  87.995 |   {'r': 7, 'p': 12, 'w1': 0, 'w2': 0, 'p1': 9, 'l': 79}    |
            | Dumer         | 151.380 |  58.019 |                 {'r': 7, 'l': 47, 'p': 5}                  |
            | MayOzerov     | 140.795 |  86.592 | {'r': 7, 'depth': 3, 'p': 12, 'p1': 5, 'p2': 10, 'l': 95}  |
            | Prange        | 173.388 |  21.576 |                          {'r': 7}                          |
            | Stern         | 151.409 |  49.814 |                 {'r': 7, 'p': 4, 'l': 39}                  |
            +---------------+---------+---------+------------------------------------------------------------+

            sage: from cryptographic_estimators.SDEstimator import SDEstimator
            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import BJMMdw
            sage: A = SDEstimator(3488,2720,64,excluded_algorithms=[BJMMdw],memory_access=3)
            sage: A.table(precision=3, show_all_parameters=1) # long time
            +---------------+------------------------------------------------------------------------+
            |               |                                estimate                                |
            +---------------+---------+--------+-----------------------------------------------------+
            | algorithm     |    time | memory |                      parameters                     |
            +---------------+---------+--------+-----------------------------------------------------+
            | BallCollision | 163.650 | 32.587 |          {'r': 7, 'p': 2, 'pl': 0, 'l': 21}         |
            | BJMMpdw       | 162.998 | 30.600 |          {'r': 7, 'p': 2, 'p1': 1, 'w2': 0}         |
            | BJMM          | 162.976 | 30.619 |    {'r': 7, 'depth': 2, 'p': 2, 'p1': 1, 'l': 21}   |
            | BJMM_plus     | 161.294 | 24.602 |     {'r': 7, 'p': 2, 'p1': 1, 'l': 21, 'l1': 9}     |
            | BothMay       | 160.317 | 25.172 | {'r': 7, 'p': 2, 'w1': 0, 'w2': 0, 'p1': 1, 'l': 8} |
            | Dumer         | 163.635 | 32.608 |              {'r': 7, 'l': 21, 'p': 2}              |
            | MayOzerov     | 160.311 | 25.179 |    {'r': 7, 'depth': 2, 'p': 2, 'p1': 1, 'l': 8}    |
            | Prange        | 180.580 | 21.576 |                       {'r': 7}                      |
            | Stern         | 163.260 | 32.587 |              {'r': 7, 'p': 2, 'l': 21}              |
            +---------------+---------+--------+-----------------------------------------------------+

        """
        super(SDEstimator, self).table(show_quantum_complexity=show_quantum_complexity,
                                       show_tilde_o_time=show_tilde_o_time,
                                       show_all_parameters=show_all_parameters,
                                       precision=precision, truncate=truncate)
