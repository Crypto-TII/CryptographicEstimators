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
