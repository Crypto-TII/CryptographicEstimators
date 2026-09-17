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


from flint import fmpq_series as power_series


class TruncatedHilbertSeries(object):
    def __init__(self, n: int, m: int, s: int, precision: int = None):
        """Construct an instance of the Hilbert series of a truncated quadratic system.

        The ring is F[x_1, ..., x_n] / <x_1^s, ..., x_n^s>, whose Hilbert series is
        (1 + x + ... + x^(s-1))^n. A polynomial f of degree d that is a nonzerodivisor there
        satisfies f^s = 0, so quotienting by it divides the series by 1 + x^d + ... + x^(d(s-1)),
        the truncated analogue of multiplying by (1 - x^d) in the untruncated case. Under the
        corresponding semi-regularity assumption the series of m homogeneous quadratics is therefore

            (1 + x + ... + x^(s-1))^n * (1 + x^2 + ... + x^(2(s-1)))^(-m).

        The degree d= 2 is built in.

        Args:
            n (int): The number of variables.
            m (int): The number of homogeneous quadratic polynomials.
            s (int): The truncation of the ring, that is the exponent with x_i ^ s = 0.
            precision (int, optional): The number of coefficients of the series, so that the
                coefficients of degree 0 up to precision - 1 are available. Defaults to
                n * (s - 1) + 1, the number of degrees in which the ring is nonzero: the quotient
                vanishes in every larger degree, so no coefficient there says anything about the
                system. A caller that only needs lower degrees should pass its own bound, which is
                cheaper.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.truncated_hilbert import TruncatedHilbertSeries
            >>> H = TruncatedHilbertSeries(10, 15, s=2, precision=12)
            >>> H
            Truncated Hilbert series for system with 10 variables and 15 quadratic polynomials truncated at 2
            >>> TruncatedHilbertSeries(10, 15, s=2).precision
            11
        """
        if not isinstance(m, int) or m < 0:
            raise ValueError("The number m of polynomials must be a non-negative integer.")
        if not isinstance(s, int) or s < 1:
            raise ValueError("The truncation s must be a positive integer.")
        if precision is None:
            precision = n * (s - 1) + 1
        if precision < 1:
            raise ValueError("The precision must be a positive integer.")

        self._nvariables = n
        self._npolynomials = m
        self._truncation = s
        self._prec = precision

        x = power_series([0, 1], prec=self._prec)
        self._series = ((1 - x**s) / (1 - x)) ** n
        self._series *= ((1 - x**2) / (1 - x ** (2 * s))) ** m

    @classmethod
    def _from_series(cls, n: int, m: int, s: int, precision: int, series):
        """Return the instance with the given attributes, bypassing the expansion of the series.

        Args:
            n (int): The number of variables.
            m (int): The number of homogeneous quadratic polynomials.
            s (int): The truncation of the ring.
            precision (int): The number of coefficients of the series.
            series: The already expanded power series.
        """
        instance = cls.__new__(cls)
        instance._nvariables = n
        instance._npolynomials = m
        instance._truncation = s
        instance._prec = precision
        instance._series = series
        return instance

    @property
    def _truncated_hilbert_series(self):
        """Return the representation of the _series attribute.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.truncated_hilbert import TruncatedHilbertSeries
            >>> H = TruncatedHilbertSeries(5, 7, s=2, precision=6)
            >>> H._truncated_hilbert_series
            1 + 5*x + 3*x^2 + (-25)*x^3 + (-37)*x^4 + 71*x^5 + O(x^6)
        """
        return self._series

    @property
    def nvariables(self):
        """Return the number of variables.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.truncated_hilbert import TruncatedHilbertSeries
            >>> H = TruncatedHilbertSeries(5, 7, s=2, precision=6)
            >>> H.nvariables
            5
        """
        return self._nvariables

    @property
    def npolynomials(self):
        """Return the number of polynomials, all of them quadratic.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.truncated_hilbert import TruncatedHilbertSeries
            >>> H = TruncatedHilbertSeries(10, 15, s=2, precision=12)
            >>> H.npolynomials
            15
        """
        return self._npolynomials

    @property
    def truncation(self):
        """Return the truncation s of the ring, the exponent with x_i ^ s = 0.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.truncated_hilbert import TruncatedHilbertSeries
            >>> H = TruncatedHilbertSeries(10, 15, s=4, precision=12)
            >>> H.truncation
            4
        """
        return self._truncation

    @property
    def precision(self):
        """Return the precision of the series.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.truncated_hilbert import TruncatedHilbertSeries
            >>> H = TruncatedHilbertSeries(10, 15, s=4, precision=12)
            >>> H.precision
            12
        """
        return self._prec

    def coefficient_of_degree(self, d: int):
        """Return the d-th coefficient in the truncated Hilbert serie self._series.

        Args:
            d (int): A non-negative integer.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.truncated_hilbert import TruncatedHilbertSeries
            >>> H = TruncatedHilbertSeries(4, 0, s=3, precision=9)
            >>> H.coefficient_of_degree(4)
            19
        """
        if d < self._prec:
            return int(self._series[d])

        raise ValueError(
            f"The degree d should be smaller than the precision of the series which is {self._prec}"
        )

    def first_nonpositive_coefficient(self):
        """Return the degree of the first non-positive coefficient of the series.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.truncated_hilbert import TruncatedHilbertSeries
            >>> H = TruncatedHilbertSeries(10, 15, s=2, precision=12)
            >>> H.first_nonpositive_coefficient()
            3
        """
        for d in range(self._prec):
            if self._series[d] <= 0:
                return int(d)
        raise ValueError("Unable to find a nonpositive coefficient in the serie.")

    def remove_variable(self):
        """Return the series of the same system in one variable less.

        Removing a variable divides the series by 1 + x + ... + x^(s-1), which is exact and much
        cheaper than expanding the series again. Successive calls therefore walk the whole family
        of systems obtained by specialising variables one at a time.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.truncated_hilbert import TruncatedHilbertSeries
            >>> H = TruncatedHilbertSeries(4, 0, s=3, precision=9)
            >>> H.remove_variable().nvariables
            3
            >>> [H.remove_variable().coefficient_of_degree(d) for d in range(7)]
            [1, 3, 6, 7, 6, 3, 1]
        """
        if self._nvariables < 1:
            raise ValueError("The series has no variable left to remove.")
        x = power_series([0, 1], prec=self._prec)
        series = self._series * (1 - x) / (1 - x**self._truncation)
        return self._from_series(
            self._nvariables - 1, self._npolynomials, self._truncation, self._prec, series
        )

    def __repr__(self):
        return (
            f"Truncated Hilbert series for system with {self.nvariables} variables and "
            f"{self.npolynomials} quadratic polynomials truncated at {self._truncation}"
        )
