from math import comb, inf, log2


import pytest

from cryptographic_estimators.MREstimator.mr_constants import MR_SERIES_PRECISION
from cryptographic_estimators.MREstimator import MRProblem, SupportMinors
from cryptographic_estimators.MREstimator.mr_helper import predict_solving_degree, linear_monomial_series

from cryptographic_estimators.MREstimator.MRAlgorithms.support_minors import support_minors_series


def test_support_minors():
    """For r=1 the determinant is explicit: 4+12t+4t^2; (1-t)^6(1-t^2)^2 gives b=1."""
    # The shifted determinant is 6; the remaining factor is (1-t).
    series = support_minors_series(101, 3, 4, 0, 2, precision=4)
    assert [int(series[d]) for d in range(4)] == [6, -6, 0, 0]
    assert predict_solving_degree(support_minors_series(2, 4, 4, 2, 1), MR_SERIES_PRECISION) == 1
    # The series is 2 + 2t, so its first zero coefficient occurs at degree two.
    assert predict_solving_degree(support_minors_series(2, 2, 2, 1, 1), MR_SERIES_PRECISION) == 2
    estimator = SupportMinors(MRProblem(q=2, m=4, n=4, k=2, r=1), w=2.81, bit_complexities=False)
    cost = estimator.time_complexity(a=0, lv=0, nprime=4, b=1)
    assert cost == pytest.approx(log2(3 * 3 * 2 * 12 ** 2))
    assert estimator.time_complexity(a=0, lv=0, nprime=4, b=2) == inf
    # First row of artifacts/figures/q2_comparison_without_nprime.csv: b exceeds r+1.
    b = predict_solving_degree(support_minors_series(2, 22, 22, 439, 1), MR_SERIES_PRECISION)
    ncols = comb(22, 1) * linear_monomial_series(2, 439, b)
    assert b == 4
    assert log2(3 * 440 * 2) + 2 * log2(ncols) == pytest.approx(81.32686808713301)
    assert estimator.parameter_ranges['b'] == {'min': 1, 'max': 4}
    assert estimator.parameter_names() == ['a', 'lv', 'b', 'nprime']
    estimator.set_parameter_ranges('b', 2, 4)
    estimator.set_parameter_ranges('nprime', 4, 4)
    assert estimator.time_complexity() == inf
    assert estimator.time_complexity(a=0, lv=0, nprime=4, b=1) == inf
    # Field equations reduce the column count in characteristic two at degree two.
    assert predict_solving_degree(support_minors_series(2, 7, 6, 10, 2), MR_SERIES_PRECISION) == 2
    assert predict_solving_degree(support_minors_series(3, 7, 6, 10, 2), MR_SERIES_PRECISION) == 2
