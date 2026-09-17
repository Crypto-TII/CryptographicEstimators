from cryptographic_estimators.MQEstimator.series.truncated_hilbert import TruncatedHilbertSeries


def test_truncated_hilbert_series_describes_a_quadratic_system():
    """The system is described by its size and its truncation only, all degrees being 2."""
    series = TruncatedHilbertSeries(5, 3, s=9, precision=8)
    assert series.nvariables == 5
    assert series.npolynomials == 3
    assert series.truncation == 9
    assert series.precision == 8


def test_truncated_hilbert_series_remove_variable_is_exact():
    """Removing a variable agrees with expanding the smaller system from scratch."""
    series = TruncatedHilbertSeries(9, 7, s=4, precision=20)
    for n in range(8, 4, -1):
        series = series.remove_variable()
        expected = TruncatedHilbertSeries(n, 7, s=4, precision=20)
        assert series.nvariables == n
        assert series.npolynomials == 7
        assert series.truncation == 4
        assert [series.coefficient_of_degree(d) for d in range(20)] == [
            expected.coefficient_of_degree(d) for d in range(20)
        ]
