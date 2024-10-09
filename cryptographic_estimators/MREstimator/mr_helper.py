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

from math import log2
from enum import Enum
from sage.all import QQ
from sage.rings.power_series_ring import PowerSeriesRing
from itertools import product
from math import comb as binomial
from sage.matrix.special import zero_matrix


class Variant(Enum):
    strassen = 1
    block_wiedemann = 2


def _strassen_complexity_(rank, ncols):
    """Returns the complexity of Gaussian elimination using Strassen algorithm.

    Args:
        rank: Target rank.
        ncols: Number of columns.
    """
    w = 2.81
    return log2(7 * rank) + (w - 1) * log2(ncols)


def _bw_complexity_(row_density, ncols):
    """Returns the complexity of block Wiedemann to find elements in the kernel of a matrix.

    Args:
        row_density: Row density.
        ncols: No. of columns.
    """
    return log2(3 * row_density) + 2 * log2(ncols)


def _binomial_mult(n, m, i, j, l):
    return binomial(m - i, l) * binomial(n - j, l)

def entry_i_j_of_A(n, m, t, i, j):
    limit = max(m - i, n - j)
    return sum([_binomial_mult(n, m, i, j, l) * t ** l for l in range(limit +  1)])

def matrix_A(m, n, r, PR):
    A = zero_matrix(PR, r, r)
    t = PR.gen()
    square_r = range(1, r + 1)
    for i, j in product(square_r, square_r):
        entry_i_j = entry_i_j_of_A(n, m, t, i, j)
        A.add_to_entry(i-1, j-1, entry_i_j)
    return A

def deteterminant_of_A(m, n, r, t):
    A = matrix_A(m, n, r, t)
    return A.determinant()

def minors_series(m, n, k, r):
    PR =  PowerSeriesRing(QQ, 't', default_prec=max(n, m) + 2)
    t = PR.gen()
    exp = (m - r) * (n - r) - (k + 1)
    series = (1 - t) ** exp  * deteterminant_of_A(m, n, r, PR)/(t ** binomial(r, 2))
    return series

def minors_polynomial(m, n_reduced, k_reduced, r):
    poly = 0
    series = minors_series(m, n_reduced, k_reduced, r)
    t = series.parent().gen()
    for D in range(series.degree()):
        poly += series[D] * t ** D
        if series[D + 1] <= 0:
            break
    return poly
