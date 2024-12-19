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
from itertools import product
from math import comb as binomial
from math import inf
from sympy import Poly, QQ
from sympy.abc import t
from sympy.polys.matrices import DomainMatrix


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


def matrix_A(m, n, r, t):
    A = DomainMatrix.zeros((r, r), QQ[t])
    square_r = range(1, r + 1)
    for i, j in product(square_r, square_r):
        entry_i_j = entry_i_j_of_A(n, m, t, i, j)
        A[i-1,j-1] = QQ[t].from_sympy(entry_i_j)
    return A


def determinant_of_A(m, n, r, t):
    A = matrix_A(m, n, r, t)
    return A.det()


def minors_series(m, n, k, r):
    exp = (m - r) * (n - r) - (k + 1)
    num = QQ[t].from_sympy((1 - t) ** exp) * determinant_of_A(m, n, r, t)
    den = QQ[t].from_sympy((t ** binomial(r, 2)))
    series = num/den
    return series

def minors_polynomial_degree(m, n_reduced, k_reduced, r):
    poly = 0
    if k_reduced >= (m - r) * (n_reduced - r):
        return inf
    series = minors_series(m, n_reduced, k_reduced, r)
    series_coeffs = list(reversed(Poly(QQ[t].to_sympy(series)).all_coeffs())) # cast from PolyElement to Poly
    for D in range(series.degree()):
        poly += series_coeffs[D] * QQ[t].from_sympy(t) ** D
        if series_coeffs[D + 1] <= 0:
            break
    return poly.degree()


def extended_binomial(n, k):
    return binomial(n,k) if n>=0 else (-1)**k * binomial(k-n-1,k)
