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


def generic_system(n: int, degrees: list[int], q=None):
    """Returns the degree of regularity for the system of polynomial equations.

    Args:
        n (int): The number of variables.
        degrees (list[int]): A list of integers representing the degrees of the polynomials.
        q (int, optional): The order of the finite field. Defaults to None.

    Examples:
        >>> from cryptographic_estimators.MQEstimator import degree_of_regularity
        >>> degree_of_regularity.generic_system(5, [2]*10)
        3

    Tests:
        >>> degree_of_regularity.generic_system(10, [3]*5)
        Traceback (most recent call last):
        ...
        ValueError: degree of regularity is defined for system with n <= m
    """
    m = len(degrees)

    if n > m:
        raise ValueError(
            "degree of regularity is defined for system with n <= m")

    return semi_regular_system(n=n, degrees=degrees, q=q)


def regular_system(n: int, degrees: list[int]):
    """Return the degree of regularity for regular system.

    Args:
        n (int): The number of variables.
        degrees (list[int]): A list of integers representing the degree of the polynomials.

    Note:
        The degree of regularity for regular system is defined only for systems with equal numbers of variables and polynomials.

    Examples:
        >>> from cryptographic_estimators.MQEstimator import degree_of_regularity
        >>> degree_of_regularity.regular_system(15, [2]*15)
        16

    Tests:
        >>> from cryptographic_estimators.MQEstimator import degree_of_regularity
        >>> degree_of_regularity.regular_system(15, [2]*16)
        Traceback (most recent call last):
        ...
        ValueError: the number of variables must be equal to the number of polynomials
    """
    m = len(degrees)
    if n != m:
        raise ValueError(
            "the number of variables must be equal to the number of polynomials")
    return semi_regular_system(n=n, degrees=degrees)


def semi_regular_system(n: int, degrees: list[int], q=None):
    """Return the degree of regularity for semi-regular system.

    The degree of regularity of a semi-regular system (f_1, ..., f_m) of respective degrees d_1, ..., d_m is
    given by the index of the first non-positive coefficient of:

    (prod_{i=1}^{m} (1 - z^{d_i})) / (1 - z)^{n}

    If the system is defined over a finite field of order q, then it is the index of the first non-positive
    coefficient of the following sequence:

    (prod_{i=1}^{m} (1 - z^{d_i}) / (1 - z^{q d_i})) * ((1 - z^{q}) / (1 - z))^{n}

    Args:
        n (int): The number of variables.
        degrees (list[int]): A list of integers representing the degree of the polynomials.
        q (int, optional): Order of the finite field. Defaults to None.

    Examples:
        >>> from cryptographic_estimators.MQEstimator import degree_of_regularity
        >>> degree_of_regularity.semi_regular_system(10, [2]*15)
        4
        >>> degree_of_regularity.semi_regular_system(10, [2]*15, q=2)
        3

    Tests:
        >>> degree_of_regularity.semi_regular_system(10, [2]*9)
        Traceback (most recent call last):
        ...
        ValueError: the number of polynomials must be >= than the number of variables
    """
    m = len(degrees)
    if m < n:
        raise ValueError(
            "the number of polynomials must be >= than the number of variables")

    s = HilbertSeries(n, degrees, q=q)
    return s.first_nonpositive_coefficient()


def quadratic_system(n: int, m: int, q=None):
    """Compute the degree of regularity for a quadratic system.

    Args:
        n (int): The number of variables.
        m (int): The number of polynomials.
        q (Optional[int]): The order of the finite field. Defaults to `None`.

    Examples:
        >>> from cryptographic_estimators.MQEstimator import degree_of_regularity
        >>> degree_of_regularity.quadratic_system(10, 15)
        4
        >>> degree_of_regularity.quadratic_system(10, 15, q=2)
        3
        >>> degree_of_regularity.quadratic_system(15, 15)
        16
    """
    return generic_system(n, [2] * m, q=q)
