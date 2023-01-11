from ..MQEstimator.series.hilbert import HilbertSeries


def semi_regular_system(n, degrees, q=None):
    """
    Return the witness degree for semi-regular system

    INPUT:

    - ``n`` -- no. of variables
    - ``degrees`` -- a list of integers representing the degree of the polynomials
    - ``q`` -- order of the finite field (default: None)

    EXAMPLES::

        sage: from cryptographic_estimators.MQEstimator import witness_degree
        sage: witness_degree.semi_regular_system(10, [2]*15)
        5
        sage: witness_degree.semi_regular_system(10, [2]*15, q=2)
        4
    """
    m = len(degrees)
    if m <= n and q is None:
        raise ValueError("The number of polynomials must be greater than the number of variables")
    elif m < n and q is not None:
        raise ValueError("The number of polynomials must be greater than or equal to the number of variables")

    s = HilbertSeries(n, degrees, q=q)
    z = s.ring.gen()
    s._series /= (1 - z)
    return s.first_nonpositive_integer()


def quadratic_system(n, m, q=None):
    """
    Return the witness degree for quadratic system

    INPUT:

    - ``n`` -- no. of variables
    - ``m`` -- no. of polynomials
    - ``q`` -- order of the finite field (default: None)

    EXAMPLES::

        sage: from cryptographic_estimators.MQEstimator import witness_degree
        sage: witness_degree.quadratic_system(10, 15)
        5
        sage: witness_degree.quadratic_system(10, 15, q=2)
        4
        sage: witness_degree.quadratic_system(15, 15, q=7)
        12
    """
    return semi_regular_system(n, [2] * m, q=q)
