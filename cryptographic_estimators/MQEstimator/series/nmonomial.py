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


from cryptographic_estimators.helper import is_prime_power
from flint import fmpq_series as power_series


class NMonomialSeries(object):
    def __init__(self, n: int, q=None, max_prec=None):
        """Construct an instance of the series of a polynomial ring.

        Args:
            n (int): The number of variables.
            q (int, optional): The size of the field (default: None).
            max_prec (int, optional): The degree of the series (default: None).

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.nmonomial import NMonomialSeries
            >>> NM = NMonomialSeries(n=6, q=5)
            >>> NM
            Class for the number of monomials in the polynomial ring in 6 variables over F_5
        """

        self._n = n
        if max_prec is not None:
            self._max_prec = max_prec
        else:
            self._max_prec = self._n + 1

        x = power_series([0, 1], prec=self._max_prec)

        if q is not None:
            if not is_prime_power(q):
                raise ValueError("the order of finite field q must be a prime power")
            self._q = q
            if q < self._max_prec:
                self._series_of_degree = ((1 - x**self._q) ** self._n) / (
                    (1 - x) ** self._n
                )
            else:
                self._series_of_degree = 1 / ((1 - x) ** self._n)
        else:
            self._series_of_degree = 1 / ((1 - x) ** self._n)

        self._series_up_to_degree = self._series_of_degree / (1 - x)

    @property
    def _nmonomial_series_of_degree(self):
        """Return the representation of the _series_of_degree attribute.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.nmonomial import NMonomialSeries
            >>> NM = NMonomialSeries(n=6, q=5)
            >>> NM._nmonomial_series_of_degree
            1 + 6*x + 21*x^2 + 56*x^3 + 126*x^4 + 246*x^5 + 426*x^6 + O(x^7)
        """
        return self._series_of_degree

    @property
    def _nmonomial_series_up_to_degree(self):
        """Return the representation of the _series_up_to_degree attribute.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.nmonomial import NMonomialSeries
            >>> NM = NMonomialSeries(n=6, q=5)
            >>> NM._nmonomial_series_up_to_degree
            1 + 7*x + 28*x^2 + 84*x^3 + 210*x^4 + 456*x^5 + 882*x^6 + O(x^7)
        """
        return self._series_up_to_degree

    def nmonomials_of_degree(self, d: int):
        """Returns the number of monomials of degree d.
    
        Args:
            d (int): A non-negative integer.
    
        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.nmonomial import NMonomialSeries
            >>> NM = NMonomialSeries(n=6, q=5)
            >>> NM.nmonomials_of_degree(4)
            126
        """
        max_prec = self._max_prec
        if d < max_prec:
            return int(self._series_of_degree[d])

        raise ValueError(
            f"The degree d should be smaller than the precision of the series which is {self._max_prec}"
        )

    def nmonomials_up_to_degree(self, d: int):
        """Return the number of monomials up to degree d.
    
        Args:
            d (int): A non-negative integer.
    
        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.nmonomial import NMonomialSeries
            >>> NM = NMonomialSeries(n=6, q=5)
            >>> NM.nmonomials_up_to_degree(4)
            210
        """
        max_prec = self._max_prec
        if d < max_prec:
            return int(self._series_up_to_degree[d])

        raise ValueError(
            f"The degree d should be smaller than the precision of the series which is {max_prec}"
        )

    def __repr__(self):
        n = self._n
        q = self._q
        if q is None:
            return f"Class for the number of monomials in the polynomial ring in {n} variables"
        else:
            return f"Class for the number of monomials in the polynomial ring in {n} variables over F_{q}"
