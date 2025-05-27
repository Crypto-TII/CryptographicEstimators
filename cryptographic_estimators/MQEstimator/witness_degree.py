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


from ..MQEstimator.series.hilbert import HilbertSeries


def semi_regular_system(n: int, degrees: list[int], q=None):
    """Returns the witness degree for a semi-regular system.

    Args:
        n (int): The number of variables.
        degrees (list[int]): A list of integers representing the degree of the polynomials.
        q (int, optional): The order of the finite field. Defaults to None.

    Examples:
        >>> from cryptographic_estimators.MQEstimator import witness_degree
        >>> witness_degree.semi_regular_system(10, [2]*15)
        5
        >>> witness_degree.semi_regular_system(10, [2]*15, q=2)
        4
    """
    m = len(degrees)
    if m <= n and q is None:
        raise ValueError(
            "The number of polynomials must be greater than the number of variables"
        )
    elif m < n and q is not None:
        raise ValueError(
            "The number of polynomials must be greater than or equal to the number of variables"
        )

    serie = HilbertSeries(n, degrees, q=q)
    return serie.first_nonpositive_coefficient_up_to_degree()


def quadratic_system(n: int, m: int, q=None):
    """Returns the witness degree for a quadratic system.

    Args:
        n (int): The number of variables.
        m (int): The number of polynomials.
        q (Optional[int]): The order of the finite field (default is None).

    Examples:
        >>> from cryptographic_estimators.MQEstimator import witness_degree
        >>> witness_degree.quadratic_system(10, 15)
        5
        >>> witness_degree.quadratic_system(10, 15, q=2)
        4
        >>> witness_degree.quadratic_system(15, 15, q=7)
        12
    """
    return semi_regular_system(n, [2] * m, q=q)
