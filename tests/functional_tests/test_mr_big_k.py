from math import inf, log2

import pytest

from cryptographic_estimators.MREstimator import MRProblem
from cryptographic_estimators.MREstimator.MRAlgorithms import BigK


def test_big_k():
    """Section 4.2: check both sides of k=m(n-r), hybrid composition and invalid guesses."""
    for k in (11, 12, 13):
        estimator = BigK(MRProblem(q=2, m=4, n=4, k=k, r=1), bit_complexities=False)
        # There are 12 entries to constrain; enumeration disappears at k=12.
        cost = 2 ** max(0, 12 - k) * 12 ** 3
        assert estimator._bk_time_complexity_helper_(2, 4, 4, k, 1) == pytest.approx(log2(cost))
        assert estimator.time_complexity(a=0, lv=0) == pytest.approx(log2(cost))

    estimator = BigK(MRProblem(q=2, m=4, n=4, k=10, r=1), bit_complexities=False)
    # a=1 leaves n=3,k=6: four guesses of eight entries, plus 556 reduction operations.
    assert estimator.time_complexity(a=1, lv=0) == pytest.approx(1 + log2(4 * 8 ** 3 + 556))
    assert estimator.time_complexity(a=3, lv=0) == inf
    assert estimator.time_complexity(a=-1, lv=0) == inf
    with pytest.raises(ValueError, match='w must be in the range'):
        BigK(MRProblem(q=2, m=4, n=4, k=10, r=1), w=4)
