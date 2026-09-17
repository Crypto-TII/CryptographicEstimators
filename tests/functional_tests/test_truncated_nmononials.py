from math import comb

import pytest

from cryptographic_estimators.MQEstimator.series.nmonomial import NMonomialSeries
from cryptographic_estimators.MQEstimator.series.truncated_nmononials import TruncatedNMonomialSeries


@pytest.mark.parametrize("s", [1, 2, 3, 8, 9, 49])
def test_truncated_nmonomial_series_counts_monomials(s):
    """T(n, s, d) counts the monomials of degree d whose exponents are all below s."""
    n, precision = 4, 10
    series = TruncatedNMonomialSeries(n, s, precision)
    assert series.truncation == s
    assert series.nvariables == n
    assert series.precision == precision
    for d in range(precision):
        # Inclusion-exclusion on the number of variables whose exponent reaches s.
        expected = sum(
            (-1) ** j * comb(n, j) * comb(d - j * s + n - 1, n - 1)
            for j in range(n + 1)
            if d - j * s >= 0
        )
        assert series.nmonomials_of_degree(d) == expected
        assert series.nmonomials_up_to_degree(d) == sum(
            series.nmonomials_of_degree(i) for i in range(d + 1)
        )


@pytest.mark.parametrize("q", [2, 4, 8, 9, 16, 25, 27])
def test_truncated_nmonomial_series_matches_nmonomial_series_at_truncation_q(q):
    """Truncating at s = q is the truncation NMonomialSeries applies over F_q."""
    n, precision = 6, 12
    truncated = TruncatedNMonomialSeries(n, q, precision)
    untruncated = NMonomialSeries(n, q=q, max_prec=precision)
    for d in range(precision):
        assert truncated.nmonomials_of_degree(d) == untruncated.nmonomials_of_degree(d)
        assert truncated.nmonomials_up_to_degree(d) == untruncated.nmonomials_up_to_degree(d)
