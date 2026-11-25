from math import inf, log2

import pytest

from cryptographic_estimators.MREstimator import MRProblem
from cryptographic_estimators.MREstimator.MRAlgorithms import BruteForce


def test_bruteforce():
    """Section 4.1: for q=2,r=1 the probability of an invertible minor is 3/8."""
    estimator = BruteForce(MRProblem(q=2, m=4, n=4, k=2, r=1), bit_complexities=False)
    cost = (8 / 3) * 2 ** 2 * 2 ** 3
    assert estimator.time_complexity(a=0, lv=0) == pytest.approx(log2(cost))
    assert estimator._BFE_time_complexity_helper_(2, 4, 2, 1) == pytest.approx(log2(cost))
    assert estimator.time_complexity(a=1, lv=0) == inf
    with pytest.raises(ValueError, match='w must be in the range'):
        BruteForce(MRProblem(q=2, m=4, n=4, k=2, r=1), w=4)
