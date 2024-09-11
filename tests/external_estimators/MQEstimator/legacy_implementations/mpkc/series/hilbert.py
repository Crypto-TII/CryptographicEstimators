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


from sage.all import ZZ, QQ
from sage.misc.misc_c import prod
from sage.rings.power_series_ring import PowerSeriesRing
from sage.arith.misc import is_prime_power


class HilbertSeries(object):
    """
    Construct an instance of Hilbert series

    INPUT:

    - ``n`` -- no of variables
    - ``degrees`` -- a list of integers representing the degree of the polynomials
    - ``q`` -- order of the finite field (default: None)

    EXAMPLES::

        sage: from mpkc.series.hilbert import HilbertSeries
        sage: H = HilbertSeries(10, [2]*15)
        sage: H
        Hilbert series for system with 10 variables and 15 polynomials
        sage: H = HilbertSeries(10, [2]*15, q=2)
        sage: H
        Hilbert series for system with 10 variables and 15 polynomials over F_2
    """
    def __init__(self, n, degrees, q=None):
        self._q = q
        self._nvariables = n
        self._degrees = degrees
        self._ring = PowerSeriesRing(QQ, 'z', default_prec=2*len(self._degrees))
        z = self._ring.gen()
        if q is not None:
            if not is_prime_power(q):
                raise ValueError("the order of finite field q must be a prime power")
            if q < 2*len(self._degrees):
                self._series = prod([(1 - z ** d) / (1 - z ** (d * q)) for d in degrees]) * ((1 - z ** q) / (1 - z)) ** n
            else:
                self._series = prod([1 - z ** d for d in degrees]) / (1 - z) ** n
        else:
            self._series = prod([1 - z ** d for d in degrees]) / (1 - z) ** n

    @property
    def nvariables(self):
        """
        Return the no. of variables

        EXAMPLES::

            sage: from mpkc.series.hilbert import HilbertSeries
            sage: H = HilbertSeries(5, [2]*7)
            sage: H.nvariables
            5
        """
        return self._nvariables

    @property
    def degrees(self):
        """
        Return a list of degrees of the polynomials

        EXAMPLES::

            sage: from mpkc.series.hilbert import HilbertSeries
            sage: H = HilbertSeries(5, [2]*7)
            sage: H.degrees
            [2, 2, 2, 2, 2, 2, 2]
        """
        return self._degrees

    @property
    def precision(self):
        """
        Return the default precision of the series

        EXAMPLES::

            sage: from mpkc.series.hilbert import HilbertSeries
            sage: H = HilbertSeries(5, [2]*7)
            sage: H.precision
            14
        """
        return self.ring.default_prec()

    @property
    def ring(self):
        """
        Return the power series ring

        EXAMPLES::

            sage: from mpkc.series.hilbert import HilbertSeries
            sage: H = HilbertSeries(5, [2]*7)
            sage: H.ring
            Power Series Ring in z over Rational Field
        """
        return self._ring

    @property
    def series(self):
        """
        Return the series

        EXAMPLES::

            sage: from mpkc.series.hilbert import HilbertSeries
            sage: H = HilbertSeries(4, [2]*5)
            sage: H.series
            1 + 4*z + 5*z^2 - 5*z^4 - 4*z^5 - z^6 + O(z^10)
            sage: H = HilbertSeries(4, [2]*5, q=2)
            sage: H.series
            1 + 4*z + z^2 - 16*z^3 - 14*z^4 + 40*z^5 + 50*z^6 - 80*z^7 - 125*z^8 + 140*z^9 + O(z^10)
        """
        return self._series

    @property
    def npolynomials(self):
        """
        Return the no. of polynomials

        EXAMPLES::

            sage: from mpkc.series.hilbert import HilbertSeries
            sage: H = HilbertSeries(10, [2]*15)
            sage: H.npolynomials
            15
        """
        return len(self._degrees)

    def first_nonpositive_integer(self):
        """
        Return the first non-positive integer of the series

        EXAMPLES::

            sage: from mpkc.series.hilbert import HilbertSeries
            sage: H = HilbertSeries(10, [2]*15)
            sage: H.first_nonpositive_integer()
            4
        """
        s = self.series()
        for d in range(self.precision):
            if s[d] <= 0:
                return ZZ(d)
        else:
            raise ValueError("unable to find a nonpositive coefficient in the series")

    def __repr__(self):
        text = f"Hilbert series for system with {self.nvariables} variables and {self.npolynomials} polynomials"
        if self._q is not None:
            text += f" over F_{self._q}"
        return text
