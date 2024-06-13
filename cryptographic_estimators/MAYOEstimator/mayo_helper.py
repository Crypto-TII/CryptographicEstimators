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

from ..MQEstimator.MQAlgorithms import BooleanSolveFXL
from ..MQEstimator import MQProblem
from math import log2, inf
from sage.functions.other import floor


def _optimize_k(n: int, m: int, k: int, q: int):
    """
    Find the optimal parameter `K` from Furue, Nakamura, and Takagi strategy

    INPUT:

    - ``n`` -- number of variables
    - ``m`` -- number of polynomials
    - ``k`` -- whipping parameter
    - ``q`` -- order of the finite field

    """
    (K, time) = (0, inf)

    for i in range(0, n-1):
        m_tilde = m - floor(((k*n)-i)/(m-i)) + 1
        n_tilde = m_tilde - i

        if n_tilde < 1: break

        E = BooleanSolveFXL(MQProblem(n=n_tilde, m=m_tilde, q=q), bit_complexities=False, w=2.81)
        t = i * log2(q) + E.time_complexity()

        if t < time:
            time = t
            K = i

    return K