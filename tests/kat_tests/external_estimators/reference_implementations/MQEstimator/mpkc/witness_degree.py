# *****************************************************************************
# Multivariate Quadratic (MQ) Estimator
# Copyright (C) 2021-2022 Emanuele Bellini, Rusydi H. Makarim, Javier Verbel
# Cryptography Research Centre, Technology Innovation Institute LLC
#
# This file is part of MQ Estimator
#
# MQ Estimator is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# MQ Estimator is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# MQ Estimator. If not, see <https://www.gnu.org/licenses/>.
# *****************************************************************************


from .series.hilbert import HilbertSeries


def semi_regular_system(n, degrees, q=None):
    """
    Return the witness degree for semi-regular system

    INPUT:

    - ``n`` -- no. of variables
    - ``degrees`` -- a list of integers representing the degree of the polynomials
    - ``q`` -- order of the finite field (default: None)

    EXAMPLES::

        sage: from mpkc import witness_degree
        sage: witness_degree.semi_regular_system(10, [2]*15)
        5
        sage: witness_degree.semi_regular_system(10, [2]*15, q=2)
        4
    """
    m = len(degrees)
    if m <= n and q is None:
        raise ValueError("The number of polynomials must be greater than the number of variables")
    elif m < n and q is not None:
        raise ValueError("The number of polynomials must be greater than or equal to the number of variables")

    s = HilbertSeries(n, degrees, q=q)
    z = s.ring.gen()
    s._series /= (1 - z)
    return s.first_nonpositive_integer()


def quadratic_system(n, m, q=None):
    """
    Return the witness degree for quadratic system

    INPUT:

    - ``n`` -- no. of variables
    - ``m`` -- no. of polynomials
    - ``q`` -- order of the finite field (default: None)

    EXAMPLES::

        sage: from mpkc import witness_degree
        sage: witness_degree.quadratic_system(10, 15)
        5
        sage: witness_degree.quadratic_system(10, 15, q=2)
        4
        sage: witness_degree.quadratic_system(15, 15, q=7)
        12
    """
    return semi_regular_system(n, [2] * m, q=q)
