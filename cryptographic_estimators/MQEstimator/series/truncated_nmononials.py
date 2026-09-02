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


class TruncatedNMonomialSeries(object):
    def __init__(self, n: int, s: int, precision: int = None):
        """Construct an instance of the series of a truncated polynomial ring.

        The ring is F[x_1, ..., x_n] / <x_1^s, ..., x_n^s>. Its monomials of degree d are those of
        the polynomial ring whose exponents are all smaller than s, so their number is the d-th
        coefficient of (1 + x + ... + x^(s-1))^n. That count is the quantity T(n, s, d) of Furue and
        Ikematsu [FI26]_.

        Args:
            n (int): The number of variables.
            s (int): The truncation of the ring, that is the exponent with x_i ^ s = 0.
            precision (int, optional): The number of coefficients of the series, so that the
                coefficients of degree 0 up to precision - 1 are available. Defaults to
                n * (s - 1) + 1, which is the whole series: the ring is spanned by the monomials of
                degree at most n * (s - 1), so T(n, s, d) is zero in every larger degree. A caller
                that only needs lower degrees should pass its own bound, which is cheaper.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.truncated_nmononials import TruncatedNMonomialSeries
            >>> NM = TruncatedNMonomialSeries(n=6, s=5, precision=8)
            >>> NM
            Class for the number of monomials in the polynomial ring in 6 variables truncated at 5
            >>> TruncatedNMonomialSeries(n=6, s=5).precision
            25
        """
        if not isinstance(s, int) or s < 1:
            raise ValueError("The truncation s must be a positive integer.")
        if precision is None:
            precision = n * (s - 1) + 1
        if precision < 1:
            raise ValueError("The precision must be a positive integer.")

        self._n = n
        self._truncation = s
        self._max_prec = precision

        x = power_series([0, 1], prec=self._max_prec)
        self._series_of_degree = ((1 - x**s) / (1 - x)) ** n
        self._series_up_to_degree = self._series_of_degree / (1 - x)

    @classmethod
    def _from_series(cls, n: int, s: int, precision: int, series):
        """Return the instance with the given attributes, bypassing the expansion of the series.

        Args:
            n (int): The number of variables.
            s (int): The truncation of the ring.
            precision (int): The number of coefficients of the series.
            series: The already expanded series of the number of monomials of each degree.
        """
        instance = cls.__new__(cls)
        instance._n = n
        instance._truncation = s
        instance._max_prec = precision
        instance._series_of_degree = series
        x = power_series([0, 1], prec=precision)
        instance._series_up_to_degree = series / (1 - x)
        return instance

    @property
    def _nmonomial_series_of_degree(self):
        """Return the representation of the _series_of_degree attribute.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.truncated_nmononials import TruncatedNMonomialSeries
            >>> NM = TruncatedNMonomialSeries(n=6, s=5, precision=8)
            >>> NM._nmonomial_series_of_degree
            1 + 6*x + 21*x^2 + 56*x^3 + 126*x^4 + 246*x^5 + 426*x^6 + 666*x^7 + O(x^8)
        """
        return self._series_of_degree

    @property
    def _nmonomial_series_up_to_degree(self):
        """Return the representation of the _series_up_to_degree attribute.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.truncated_nmononials import TruncatedNMonomialSeries
            >>> NM = TruncatedNMonomialSeries(n=6, s=5, precision=8)
            >>> NM._nmonomial_series_up_to_degree
            1 + 7*x + 28*x^2 + 84*x^3 + 210*x^4 + 456*x^5 + 882*x^6 + 1548*x^7 + O(x^8)
        """
        return self._series_up_to_degree

    @property
    def nvariables(self):
        """Return the number of variables.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.truncated_nmononials import TruncatedNMonomialSeries
            >>> NM = TruncatedNMonomialSeries(n=6, s=5, precision=8)
            >>> NM.nvariables
            6
        """
        return self._n

    @property
    def truncation(self):
        """Return the truncation s of the ring, the exponent with x_i ^ s = 0.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.truncated_nmononials import TruncatedNMonomialSeries
            >>> NM = TruncatedNMonomialSeries(n=6, s=25, precision=8)
            >>> NM.truncation
            25
        """
        return self._truncation

    @property
    def precision(self):
        """Return the precision of the series.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.truncated_nmononials import TruncatedNMonomialSeries
            >>> NM = TruncatedNMonomialSeries(n=6, s=5, precision=8)
            >>> NM.precision
            8
        """
        return self._max_prec

    def nmonomials_of_degree(self, d: int):
        """Return the number of monomials of degree d, that is T(n, s, d) of [FI26]_.

        Args:
            d (int): A non-negative integer.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.truncated_nmononials import TruncatedNMonomialSeries
            >>> NM = TruncatedNMonomialSeries(n=6, s=5, precision=8)
            >>> NM.nmonomials_of_degree(4)
            126
        """
        max_prec = self._max_prec
        if d < max_prec:
            return int(self._series_of_degree[d])

        raise ValueError(
            f"The degree d should be smaller than the precision of the series which is {max_prec}"
        )

    def nmonomials_up_to_degree(self, d: int):
        """Return the number of monomials up to degree d.

        Args:
            d (int): A non-negative integer.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.truncated_nmononials import TruncatedNMonomialSeries
            >>> NM = TruncatedNMonomialSeries(n=6, s=5, precision=8)
            >>> NM.nmonomials_up_to_degree(4)
            210
        """
        max_prec = self._max_prec
        if d < max_prec:
            return int(self._series_up_to_degree[d])

        raise ValueError(
            f"The degree d should be smaller than the precision of the series which is {max_prec}"
        )

    def remove_variable(self):
        """Return the series of the same ring in one variable less.

        Removing a variable divides the series by 1 + x + ... + x^(s-1), which is exact and much
        cheaper than expanding the series again. Successive calls therefore walk the counts
        T(n, s, .), T(n-1, s, .), ... of [FI26]_ one variable at a time.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.series.truncated_nmononials import TruncatedNMonomialSeries
            >>> NM = TruncatedNMonomialSeries(n=6, s=5, precision=8)
            >>> NM.remove_variable().nvariables
            5
            >>> [NM.remove_variable().nmonomials_of_degree(d) for d in range(6)]
            [1, 5, 15, 35, 70, 121]
        """
        if self._n < 1:
            raise ValueError("The series has no variable left to remove.")
        x = power_series([0, 1], prec=self._max_prec)
        series = self._series_of_degree * (1 - x) / (1 - x**self._truncation)
        return self._from_series(self._n - 1, self._truncation, self._max_prec, series)

    def __repr__(self):
        return (
            f"Class for the number of monomials in the polynomial ring in {self._n} variables "
            f"truncated at {self._truncation}"
        )
