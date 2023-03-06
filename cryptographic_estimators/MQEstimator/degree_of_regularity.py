from ..MQEstimator.series.hilbert import HilbertSeries


def generic_system(n: int, degrees: list[int], q=None):
    """
    Return the degree of regularity for the system of polynomial equations

    INPUT:

    - ``n`` -- no. of variables
    - ``degrees`` -- a list of integers representing the degree of the polynomials
    - ``q`` -- order of the finite field (default: None)

    EXAMPLES::

        sage: from cryptographic_estimators.MQEstimator import degree_of_regularity
        sage: degree_of_regularity.generic_system(5, [2]*10)
        3

    TESTS::

        sage: degree_of_regularity.generic_system(10, [3]*5)
        Traceback (most recent call last):
        ...
        ValueError: degree of regularity is defined for system with n <= m
    """
    m = len(degrees)

    if n > m:
        raise ValueError("degree of regularity is defined for system with n <= m")

    return semi_regular_system(n=n, degrees=degrees, q=q)


def regular_system(n: int, degrees: list[int]):
    """
    Return the degree of regularity for regular system

    INPUT:

    - ``n`` -- no. of variables
    - ``degree`` -- a list of integers representing the degree of the polynomials

    .. NOTE::

        The degree of regularity for regular system is defined only for systems with equal numbers of variables
        and polynomials

    EXAMPLES::

        sage: from cryptographic_estimators.MQEstimator import degree_of_regularity
        sage: degree_of_regularity.regular_system(15, [2]*15)
        16

    TESTS::

        sage: from cryptographic_estimators.MQEstimator import degree_of_regularity
        sage: degree_of_regularity.regular_system(15, [2]*16)
        Traceback (most recent call last):
        ...
        ValueError: the number of variables must be equal to the number of polynomials
    """
    m = len(degrees)
    if n != m:
        raise ValueError("the number of variables must be equal to the number of polynomials")
    return semi_regular_system(n=n, degrees=degrees)


def semi_regular_system(n: int, degrees: list[int], q=None):
    r"""
    Return the degree of regularity for semi-regular system

    The degree of regularity of a semi-regular system $(f_1, \ldots, f_m)$ of respective degrees $d_1, \ldots, d_m$ is
    given by the index of the first non-positive coefficient of

    .. MATH::

        \dfrac{\prod_{i=1}^{m} (1 - z^{d_i})}{(1 - z)^{n}}

    If the system is defined over a finite field of order `q`, then it is the index of the first non-positive
    coefficient of the following sequence

    .. MATH::

        \prod_{i=1}^{m} \dfrac{(1 - z^{d_i})}{(1 - z^{q d_i})} \cdot \Bigg( \dfrac{(1 - z^{q})}{(1 - z)} \Bigg)^{n}

    INPUT:

    - ``n`` -- no. of variables
    - ``degrees`` -- a list of integers representing the degree of the polynomials
    - ``q`` -- order of the finite field (default: None)

    EXAMPLES::

        sage: from cryptographic_estimators.MQEstimator import degree_of_regularity
        sage: degree_of_regularity.semi_regular_system(10, [2]*15)
        4
        sage: degree_of_regularity.semi_regular_system(10, [2]*15, q=2)
        3

    TESTS::

        sage: degree_of_regularity.semi_regular_system(10, [2]*9)
        Traceback (most recent call last):
        ...
        ValueError: the number of polynomials must be >= than the number of variables
    """
    m = len(degrees)
    if m < n:
        raise ValueError("the number of polynomials must be >= than the number of variables")

    s = HilbertSeries(n, degrees, q=q)
    return s.first_nonpositive_integer()


def quadratic_system(n: int, m: int, q=None):
    """
    Return the degree of regularity for quadratic system

    INPUT:

    - ``n`` -- no. of variables
    - ``m`` -- no. of polynomials
    - ``q`` -- order of the finite field (default: None)

    EXAMPLES::

        sage: from cryptographic_estimators.MQEstimator import degree_of_regularity
        sage: degree_of_regularity.quadratic_system(10, 15)
        4
        sage: degree_of_regularity.quadratic_system(10, 15, q=2)
        3
        sage: degree_of_regularity.quadratic_system(15, 15)
        16
    """
    return generic_system(n, [2] * m, q=q)
