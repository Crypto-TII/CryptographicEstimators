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
from math import inf
from ..SDEstimator.sd_algorithm import SDAlgorithm
from ..SDEstimator.sd_problem import SDProblem
from ..SDEstimator.SDAlgorithms import BJMMd2, BJMMd3, MayOzerovD2, MayOzerovD3
from ..base_estimator import BaseEstimator


class SDEstimator(BaseEstimator):
    """Construct an instance of Syndrome Decoding Estimator.

    Args:
        n (int): Code length.
        k (int): Code dimension.
        w (int): Error weight.
        excluded_algorithms (Union[List, Tuple], optional): A list or tuple of excluded algorithms. Defaults to None.
        nsolutions (int): Number of solutions.

    """

    excluded_algorithms_by_default = [BJMMd2, BJMMd3, MayOzerovD2, MayOzerovD3]

    def __init__(self, n: int, k: int, w: int, memory_bound=inf, **kwargs):
        if not kwargs.get("excluded_algorithms"):
            kwargs["excluded_algorithms"] = []

        kwargs["excluded_algorithms"] += self.excluded_algorithms_by_default

        super(SDEstimator, self).__init__(
            SDAlgorithm, SDProblem(n, k, w, memory_bound=memory_bound, **kwargs), **kwargs
        )

    def table(
        self,
        show_quantum_complexity=0,
        show_tilde_o_time=0,
        show_all_parameters=0,
        precision=1,
        truncate=0,
    ):
        """Print table describing the complexity of each algorithm and its optimal parameters.

        Args:
            show_quantum_complexity (int, optional): Show quantum time complexity. Defaults to 0.
            show_tilde_o_time (int, optional): Show Ō time complexity. Defaults to 0.
            show_all_parameters (int, optional): Show all optimization parameters. Defaults to 0.
            precision (int, optional): Number of decimal digits output. Defaults to 1.
            truncate (int, optional): Truncate rather than round the output. Defaults to 0.

        Examples:
            >>> from cryptographic_estimators.SDEstimator import SDEstimator
            >>> A = SDEstimator(n=100, k=50, w=10)
            >>> A.table()
            +---------------+---------------+
            |               |    estimate   |
            +---------------+------+--------+
            | algorithm     | time | memory |
            +---------------+------+--------+
            | BallCollision | 23.3 |   16.0 |
            | BJMMdw        | 23.4 |   14.7 |
            | BJMMpdw       | 23.3 |   14.3 |
            | BJMM          | 22.8 |   15.0 |
            | BJMMplus      | 22.8 |   15.0 |
            | BothMay       | 22.4 |   14.7 |
            | Dumer         | 22.7 |   16.4 |
            | MayOzerov     | 22.3 |   14.8 |
            | Prange        | 28.3 |   12.7 |
            | Stern         | 22.3 |   16.0 |
            +---------------+------+--------+


        Tests:
            >>> if skip_long_doctests:
            ...     pytest.skip()
            >>> from cryptographic_estimators.SDEstimator import SDEstimator
            >>> from cryptographic_estimators.SDEstimator import BothMay
            >>> A = SDEstimator(n=100, k=42, w=13, bit_complexities=1,excluded_algorithms=[BothMay], workfactor_accuracy=25)
            >>> A.table(show_tilde_o_time=1, precision=0)
            +---------------+---------------+------------------+
            |               |    estimate   | tilde_o_estimate |
            +---------------+------+--------+-------+----------+
            | algorithm     | time | memory |  time |   memory |
            +---------------+------+--------+-------+----------+
            | BallCollision |   24 |     16 |    11 |        3 |
            | BJMMdw        |   24 |     14 |    -- |       -- |
            | BJMMpdw       |   24 |     15 |    -- |       -- |
            | BJMM          |   23 |     15 |     9 |        7 |
            | BJMMplus      |   23 |     15 |    -- |       -- |
            | Dumer         |   23 |     16 |    11 |        3 |
            | MayOzerov     |   23 |     15 |     9 |        8 |
            | Prange        |   29 |     13 |    11 |        0 |
            | Stern         |   23 |     16 |    11 |        3 |
            +---------------+------+--------+-------+----------+

            >>> from cryptographic_estimators.SDEstimator import SDEstimator
            >>> from cryptographic_estimators.SDEstimator.SDAlgorithms import BJMMdw
            >>> A = SDEstimator(3488, 2720, 64, excluded_algorithms=[BJMMdw])
            >>> A.table(precision=3, show_all_parameters=1)
            +---------------+--------------------------------------------------------------------------------+
            |               |                                    estimate                                    |
            +---------------+---------+---------+------------------------------------------------------------+
            | algorithm     |    time |  memory |                         parameters                         |
            +---------------+---------+---------+------------------------------------------------------------+
            | BallCollision | 151.460 |  49.814 |             {'r': 7, 'p': 4, 'pl': 0, 'l': 39}             |
            | BJMMpdw       | 143.448 |  86.221 |            {'r': 7, 'p': 12, 'p1': 8, 'w2': 0}             |
            | BJMM          | 141.886 | 104.057 | {'r': 7, 'depth': 3, 'p': 16, 'p1': 6, 'p2': 12, 'l': 197} |
            | BJMMplus      | 142.111 |  97.541 |      {'r': 7, 'p': 14, 'p1': 10, 'l': 167, 'l1': 81}       |
            | BothMay       | 141.711 |  87.995 |   {'r': 7, 'p': 12, 'w1': 0, 'w2': 0, 'p1': 9, 'l': 79}    |
            | Dumer         | 151.380 |  58.019 |                 {'r': 7, 'l': 47, 'p': 5}                  |
            | MayOzerov     | 140.795 |  86.592 | {'r': 7, 'depth': 3, 'p': 12, 'p1': 5, 'p2': 10, 'l': 95}  |
            | Prange        | 173.388 |  21.576 |                          {'r': 7}                          |
            | Stern         | 151.409 |  49.814 |                 {'r': 7, 'p': 4, 'l': 39}                  |
            +---------------+---------+---------+------------------------------------------------------------+

            >>> from cryptographic_estimators.SDEstimator import SDEstimator
            >>> from cryptographic_estimators.SDEstimator.SDAlgorithms import BJMMdw
            >>> A = SDEstimator(3488,2720,64,excluded_algorithms=[BJMMdw],memory_access=3)
            >>> A.table(precision=3, show_all_parameters=1)
            +---------------+----------------------------------------------------------------------------+
            |               |                                  estimate                                  |
            +---------------+---------+--------+---------------------------------------------------------+
            | algorithm     |    time | memory |                        parameters                       |
            +---------------+---------+--------+---------------------------------------------------------+
            | BallCollision | 153.405 | 32.587 |            {'r': 7, 'p': 2, 'pl': 0, 'l': 21}           |
            | BJMMpdw       | 153.217 | 30.600 |            {'r': 7, 'p': 2, 'p1': 1, 'w2': 0}           |
            | BJMM          | 153.191 | 30.619 |      {'r': 7, 'depth': 2, 'p': 2, 'p1': 1, 'l': 21}     |
            | BJMMplus      | 153.210 | 24.602 |       {'r': 7, 'p': 2, 'p1': 1, 'l': 21, 'l1': 9}       |
            | BothMay       | 152.059 | 25.172 |   {'r': 7, 'p': 2, 'w1': 0, 'w2': 0, 'p1': 1, 'l': 8}   |
            | Dumer         | 153.385 | 32.608 |                {'r': 7, 'l': 21, 'p': 2}                |
            | MayOzerov     | 150.210 | 32.092 | {'r': 7, 'depth': 3, 'p': 4, 'p1': 1, 'p2': 2, 'l': 20} |
            | Prange        | 173.447 | 21.576 |                         {'r': 7}                        |
            | Stern         | 153.015 | 32.587 |                {'r': 7, 'p': 2, 'l': 21}                |
            +---------------+---------+--------+---------------------------------------------------------+
        """
        super(SDEstimator, self).table(
            show_quantum_complexity=show_quantum_complexity,
            show_tilde_o_time=show_tilde_o_time,
            show_all_parameters=show_all_parameters,
            precision=precision,
            truncate=truncate,
        )
