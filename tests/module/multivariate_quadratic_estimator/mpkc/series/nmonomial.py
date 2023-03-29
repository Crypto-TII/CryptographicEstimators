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


from sage.arith.misc import is_prime_power
from sage.rings.power_series_ring import PowerSeriesRing
from sage.rings.all import QQ


class NMonomialSeries(object):
    """
    Construct an instance of the series of a polynomial ring

    INPUT:

    - ``n`` -- the number of variables
    - ``q`` -- the size of the field (default: None)
    - ``max_prec`` -- degree of the series (default: None)

    EXAMPLES::

        sage: from mpkc.series.nmonomial import NMonomialSeries
        sage: NM = NMonomialSeries(n=6, q=5)
        sage: NM
        Class for the number of monomials in the polynomial ring in 6 variables over F_5
    """
    def __init__(self, n, q=None, max_prec=None):
        self._n = n
        if max_prec is not None:
            self._max_prec = max_prec
        else:
            self._max_prec = self._n + 1

        R = PowerSeriesRing(QQ, 'z', default_prec=self._max_prec)
        z = R.gen()

        if q is not None:
            if not is_prime_power(q):
                raise ValueError("the order of finite field q must be a prime power")
            self._q = q
            if q < self._max_prec and q <= 2 ** 10:
                self._series_of_degree = ((1 - z ** self._q) ** self._n) / ((1 - z) ** self._n)
            else:
                self._series_of_degree = 1 / ((1 - z) ** self._n)
        else:
            self._series_of_degree = 1 / ((1 - z) ** self._n)

        self._series_up_to_degree = self._series_of_degree / (1 - z)

    def series_monomials_of_degree(self):
        """
        Return the series of the number of monomials of a given degree

        EXAMPLES::

            sage: from mpkc.series.nmonomial import NMonomialSeries
            sage: NM = NMonomialSeries(n=6, q=5)
            sage: NM.series_monomials_of_degree()
            1 + 6*z + 21*z^2 + 56*z^3 + 126*z^4 + 246*z^5 + 426*z^6 + O(z^7)
        """
        return self._series_of_degree

    def series_monomials_up_to_degree(self):
        """
        Return the series of the number of monomials up to given degree

        EXAMPLES::

            sage: from mpkc.series.nmonomial import NMonomialSeries
            sage: NM = NMonomialSeries(n=6, q=5)
            sage: NM.series_monomials_up_to_degree()
            1 + 7*z + 28*z^2 + 84*z^3 + 210*z^4 + 456*z^5 + 882*z^6 + O(z^7)
        """
        return self._series_up_to_degree

    def nmonomials_of_degree(self, d):
        """
        Return the number of monomials of degree `d`

        INPUT:

        - ``d`` -- a non-negative integer

        EXAMPLES::

            sage: from mpkc.series.nmonomial import NMonomialSeries
            sage: NM = NMonomialSeries(n=6, q=5)
            sage: NM.nmonomials_of_degree(4)
            126
        """
        max_prec = self._max_prec
        if d < max_prec:
            return self._series_of_degree[d]
        else:
            ValueError(f'The degree d should be smaller than the precision of the series which is {self._max_prec}')

    def nmonomials_up_to_degree(self, d):
        """
        Return the number of monomials up to degree `d`

        INPUT:

        - ``d`` -- a non-negative integer

        EXAMPLES::

            sage: from mpkc.series.nmonomial import NMonomialSeries
            sage: NM = NMonomialSeries(n=6, q=5)
            sage: NM.nmonomials_up_to_degree(4)
            210
        """
        max_prec = self._max_prec
        if d < max_prec:
            return self._series_up_to_degree[d]
        else:
            ValueError(f'The degree d should be smaller than the precision of the series which is {max_prec}')

    def __repr__(self):
        n = self._n
        q = self._q
        if q is None:
            return f'Class for the number of monomials in the polynomial ring in {n} variables'
        else:
            return f'Class for the number of monomials in the polynomial ring in {n} variables over F_{q}'
