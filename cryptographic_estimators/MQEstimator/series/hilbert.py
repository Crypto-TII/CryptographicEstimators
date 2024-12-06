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
from math import prod


class HilbertSeries(object):
    def __init__(self, n: int, degrees: list[int], q=None):
        """Construct an instance of Hilbert series.

        Args:
            n (int): The number of variables.
            degrees (list[int]): A list of integers representing the degree of the polynomials.
            q (int, optional): The order of the finite field. Defaults to None.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.hilbert import HilbertSeries
            >>> H = HilbertSeries(10, [2]*15)
            >>> H
            Hilbert series for system with 10 variables and 15 polynomials
            >>> H = HilbertSeries(10, [2]*15, q=2)
            >>> H
            Hilbert series for system with 10 variables and 15 polynomials over F_2
        """

        self._q = q
        self._nvariables = n
        self._degrees = degrees
        # Precision sufficient for systems with variables not exceeding equations.
        self._prec = 2 * len(self._degrees)
        self._gen = power_series([0, 1], prec=self._prec)
        x = self._gen
        if q is not None:
            if not is_prime_power(q):
                raise ValueError("The order of finite field q must be a prime power.")
            if q < 2 * len(self._degrees):
                self._series = (
                    prod([(1 - x**d) / (1 - x ** (d * q)) for d in degrees])
                    * ((1 - x**q) / (1 - x)) ** n
                )
            else:
                self._series = prod([1 - x**d for d in degrees]) / (1 - x) ** n
        else:
            self._series = prod([1 - x**d for d in degrees]) / (1 - x) ** n
        self._series_up_to_degree = self._series / (1 - x)

    @property
    def _hilbert_series(self):
        """Return the representation of the _series attribute.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.hilbert import HilbertSeries
            >>> H = HilbertSeries(5, [2]*7)
            >>> H._hilbert_series
            1 + 5*x + 8*x^2 + (-14)*x^4 + (-14)*x^5 + 8*x^7 + 5*x^8 + x^9 + O(x^14)
        """
        return self._series

    @property
    def _hilbert_series_up_to_degree(self):
        """Return the representation of the _series_up_to_degree attribute.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.hilbert import HilbertSeries
            >>> H = HilbertSeries(5, [2]*7)
            >>> H._hilbert_series_up_to_degree
            1 + 6*x + 14*x^2 + 14*x^3 + (-14)*x^5 + (-14)*x^6 + (-6)*x^7 + (-1)*x^8 + O(x^14)
        """
        return self._series_up_to_degree

    @property
    def nvariables(self):
        """Return the number of variables.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.hilbert import HilbertSeries
            >>> H = HilbertSeries(5, [2]*7)
            >>> H.nvariables
            5
        """
        return self._nvariables

    @property
    def degrees(self):
        """Return a list of degrees of the polynomials.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.hilbert import HilbertSeries
            >>> H = HilbertSeries(5, [2]*7)
            >>> H.degrees
            [2, 2, 2, 2, 2, 2, 2]
        """
        return self._degrees

    @property
    def precision(self):
        """Return the precision of the series.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.hilbert import HilbertSeries
            >>> H = HilbertSeries(5, [3]*7)
            >>> H.precision
            14
        """
        return self._prec

    @property
    def npolynomials(self):
        """Return the number of polynomials.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.hilbert import HilbertSeries
            >>> H = HilbertSeries(10, [2]*15)
            >>> H.npolynomials
            15
        """
        return len(self._degrees)

    def coefficient_of_degree(self, d: int):
        """Return the d-th coefficient in the Hilbert serie self._series.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.hilbert import HilbertSeries
            >>> H = HilbertSeries(4, [2]*5)
            >>> H.coefficient_of_degree(5)
            -4
        """

        if d < self._prec:
            return int(self._series[d])

        raise ValueError(
            f"The degree d should be smaller than the precision of the series which is {self._prec}"
        )

    def coefficient_up_to_degree(self, d: int):
        """Return the d-th coefficient in the Hilbert serie self._series/(1-x)

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.hilbert import HilbertSeries
            >>> H = HilbertSeries(4, [2]*5)
            >>> H.coefficient_up_to_degree(4)
            5
        """

        if d < self._prec:
            return int(self._series_up_to_degree[d])
        raise ValueError(
            f"The degree d should be smaller than the precision of the series which is {self._prec}"
        )

    def first_nonpositive_coefficient(self):
        """Return the first non-positive integer of the series.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.hilbert import HilbertSeries
            >>> H = HilbertSeries(10, [2]*15)
            >>> H.first_nonpositive_coefficient()
            4
        """
        serie = self._series
        for d in range(self.precision):
            if serie[d] <= 0:
                return int(d)
        raise ValueError("Unable to find a nonpositive coefficient in the serie.")

    def first_nonpositive_coefficient_up_to_degree(self):
        """Return the first non-positive integer of the serie self._series/(1-x).

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.hilbert import HilbertSeries
            >>> H = HilbertSeries(10, [2]*15)
            >>> H.first_nonpositive_coefficient_up_to_degree()
            5
        """
        for d in range(self.precision):
            if self._series_up_to_degree[d] <= 0:
                return int(d)
        raise ValueError(
            "Unable to find a nonpositive coefficient in the up_to_degree serie."
        )

    def __repr__(self):
        text = f"Hilbert series for system with {self.nvariables} variables and {self.npolynomials} polynomials"
        if self._q is not None:
            text += f" over F_{self._q}"
        return text
