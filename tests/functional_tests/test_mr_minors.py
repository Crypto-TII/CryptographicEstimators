from math import comb, log2

from flint import ctx, fmpq_series
from sympy.abc import t

import pytest

from cryptographic_estimators.MREstimator.mr_constants import MR_SERIES_PRECISION
from cryptographic_estimators.MREstimator import MRProblem
from cryptographic_estimators.MREstimator.MRAlgorithms import Minors
from cryptographic_estimators.MREstimator.mr_helper import (
    determinant_of_A, linear_monomial_series,
    predict_solving_degree,
)

from cryptographic_estimators.MREstimator.MRAlgorithms.minors import minors_series


def test_minors():
    """Check an explicit r=1 series and the first row of the reference Minors figure."""
    assert predict_solving_degree(fmpq_series([1, 0, -1], prec=3), 3) == 1
    with pytest.raises(ValueError, match='precision'):
        predict_solving_degree(fmpq_series([1, 2, 3], prec=3), 3)
    # The last known coefficient is usable; an unknown coefficient is not.
    precision = MR_SERIES_PRECISION
    assert predict_solving_degree(fmpq_series([1] * (precision - 1), prec=precision), precision) == precision - 1
    with pytest.raises(ValueError, match='precision'):
        predict_solving_degree(fmpq_series([1] * precision, prec=precision), precision)
    assert predict_solving_degree(fmpq_series([1] * precision, prec=precision + 1), precision + 1) == precision
    # For r=2, divide the determinants t+2t^2+3t^3 and 6t by t.
    for dc, expected in ((0, [1, 2, 3, 0]), (1, [6, 0, 0, 0])):
        series = determinant_of_A(3, 4, 2, t, dc, precision=4)
        assert isinstance(series, fmpq_series)
        assert [int(series[d]) for d in range(4)] == expected
    for k, expected in ((0, [1, 1, 1, -3]), (1, [1, 2, 3, 0]), (2, [1, 3, 6, 6])):
        series = minors_series(101, 3, 4, k, 2, precision=4)
        assert isinstance(series, fmpq_series)
        assert [int(series[d]) for d in range(4)] == expected
    for precision in (0, ctx.cap + 1):
        with pytest.raises(ValueError, match='precision'):
            determinant_of_A(3, 4, 2, t, precision=precision)
    # Compare cumulative monomial counts before and after field equations apply.
    for q in (2, 3, 4):
        for k in (1, 3, 10):
            for degree in (0, 1, q, q + 2):
                expected = sum((-1) ** j * comb(k, j) * comb(k + degree - q * j, k)
                               for j in range(min(k, degree // q) + 1))
                assert linear_monomial_series(q, k, degree) == expected
    for degree in (-1, ctx.cap):
        with pytest.raises(ValueError, match='degree'):
            linear_monomial_series(2, 3, degree)
    # det(A)=1+9t+9t^2+t^3; multiplication by (1-t)^6(1-t^2)^2 gives 1+3t-32t^2+...
    assert predict_solving_degree(minors_series(2, 4, 4, 2, 1), MR_SERIES_PRECISION) == 2
    estimator = Minors(MRProblem(q=2, m=4, n=4, k=2, r=1), bit_complexities=False)
    assert estimator.time_complexity(a=0, lv=0) == pytest.approx(log2(4 ** 3))
    # artifacts/figures/q2_comparison_minors.csv, q=2,m=n=22,k=(22-r)^2-2.
    D = predict_solving_degree(minors_series(2, 22, 22, 439, 1), MR_SERIES_PRECISION)
    ncols = linear_monomial_series(2, 439, D)
    assert D == 5
    assert 2.81 * log2(ncols) == pytest.approx(103.87771548817017)
    with pytest.raises(ValueError, match='k <'):
        Minors(MRProblem(q=2, m=4, n=4, k=9, r=1))
