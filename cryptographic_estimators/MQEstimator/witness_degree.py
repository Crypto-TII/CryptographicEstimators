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
