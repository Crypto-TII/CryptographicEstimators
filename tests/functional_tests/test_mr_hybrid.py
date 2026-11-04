from math import inf, log2

import pytest

from cryptographic_estimators.MREstimator import KernelSearch, MRProblem


def test_hybrid_approach():
    """Check ProcessGuess's three steps, additive composition and excluded terminal guesses."""
    estimator = KernelSearch(MRProblem(q=2, m=4, n=4, k=10, r=1), bit_complexities=False)
    # a=1, lv=0: 44 construction, 176 elimination, 336 substitution operations.
    assert estimator.hybrid_reduction_cost(1, 0) == pytest.approx(log2(44 + 176 + 336))
    solver = estimator._improved_kernel_search(2, 4, 3, 6, 1)
    assert estimator.time_complexity(a=1, lv=0) == pytest.approx(1 + log2(556 + 2 ** solver))
    assert estimator.time_complexity(a=3, lv=0) == inf
    assert estimator.time_complexity(a=-1, lv=0) == inf
    assert estimator.hybrid_reduction_cost(0, 0) == -inf
    estimator.reset()
    assert estimator.time_complexity() <= estimator.time_complexity(a=0, lv=0)
