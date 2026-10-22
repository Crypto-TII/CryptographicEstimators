# ****************************************************************************
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
# ****************************************************************************

from cryptographic_estimators.MQEstimator.series import NMonomialSeries
from .mr_constants import MR_SERIES_PRECISION
from functools import lru_cache
from flint import fmpq_series, ctx
from math import log2
from enum import Enum
from itertools import product
from math import comb as binomial
from sympy import Poly, QQ
from sympy.abc import t
from sympy.polys.matrices import DomainMatrix


class Variant(Enum):
    strassen = 1
    block_wiedemann = 2


def _strassen_complexity_(rank, ncols, w=2.81):
    """Returns the complexity of Gaussian elimination using Strassen algorithm.

    Args:
        rank: Target rank.
        ncols: Number of columns.
        w: Linear algebra exponent.
    """
    return log2(7 * rank) + (w - 1) * log2(ncols)


def _bw_complexity_(row_density, ncols):
    """Returns the complexity of block Wiedemann to find elements in the kernel of a matrix.

    Args:
        row_density: Row density.
        ncols: No. of columns.
    """
    return log2(3 * row_density) + 2 * log2(ncols)


def entry_i_j_of_A(n, m, t, i, j, dc=0):
    """Return an entry of the transposed Minors or Support-Minors matrix."""
    n_bound = n + dc - j
    m_bound = m - dc - i
    max_degree = min(n_bound - dc, m_bound)
    return sum(
        binomial(n_bound, ell + dc) * binomial(m_bound, ell) * t ** ell
        for ell in range(max_degree + 1)
    )


def matrix_A(m, n, r, t, dc=0):
    """Build the Minors (dc=0) or Support-Minors (dc=1) matrix, transposed."""
    polynomial_ring = QQ[t]
    A = DomainMatrix.zeros((r, r), polynomial_ring)
    square_r = range(1, r + 1)
    for i, j in product(square_r, square_r):
        entry = entry_i_j_of_A(n, m, t, i, j, dc)
        A[i - 1, j - 1] = polynomial_ring.from_sympy(entry)
    return A


@lru_cache(maxsize=128)
def A_det(m, n, r, dc=0, t=t):
    """Return coefficients of det(A_dc)/t^binomial(r,2).

    dc=0 gives the Minors matrix; dc=1 gives the Support-Minors matrix.
    """
    determinant = QQ[t].to_sympy(matrix_A(m, n, r, t, dc).det())
    coefficients = Poly(determinant, t).all_coeffs()
    coefficients.reverse()  # Order by increasing degree.
    shift = binomial(r, 2)
    return tuple(int(c) for c in coefficients[shift:])


def determinant_of_A(m, n, r, t, dc=0, precision=None):
    """Return det(A_dc)/t^binomial(r,2) as a FLINT series."""
    if precision is None:
        precision = MR_SERIES_PRECISION
    if not 0 < precision <= ctx.cap:
        raise ValueError('precision must be positive and at most the python-flint precision cap')
    coefficients = A_det(m, n, r, dc, t)
    return fmpq_series(list(coefficients), prec=precision)


def determinantal_series(q, m, n, k, r, dc=0, precision=None):
    """Return the Minors (dc=0) or Support-Minors (dc=1) series with field equations."""
    if precision is None:
        precision = MR_SERIES_PRECISION
    series = determinant_of_A(m, n, r, t, dc, precision)
    z = fmpq_series([0, 1], prec=precision)
    exponent = (m - r) * (n - r) - (k + 1)
    if exponent >= 0:
        series *= (1 - z) ** exponent
    else:
        series /= (1 - z) ** (-exponent)
    return series * (1 - z ** q) ** k


def linear_monomial_series(q, k, degree):
    """Return [t^degree](1-t^q)^k/(1-t)^(k+1), including the homogenizing variable."""
    if not 0 <= degree < ctx.cap:
        raise ValueError("degree must be nonnegative and below the python-flint precision cap")
    monomials = NMonomialSeries(n=k, q=q, max_prec=degree + 1)
    return monomials.nmonomials_up_to_degree(degree)


def predict_solving_degree(series, precision):
    """Return the first nonpositive coefficient's degree within the supplied precision."""
    for degree in range(precision):
        if series[degree] <= 0:
            return degree
    raise ValueError('MinRank solving degree exceeds the supplied series precision')
