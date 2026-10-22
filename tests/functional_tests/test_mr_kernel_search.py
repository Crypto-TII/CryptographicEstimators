from math import ceil, floor

import pytest

from cryptographic_estimators.MREstimator import KernelSearch, MRProblem


def test_kernel_search():
    """Check the improved cost, single-vector fallback, and invalid linear algebra exponent."""
    # Reference artifact outputs in field operations, with w=2.81.
    for k, expected in [(4, 8.604775689421102), (5, 8.919250746483815), (8, 10.517698959448076)]:
        estimator = KernelSearch(MRProblem(q=2, m=4, n=4, k=k, r=1), w=2.81, bit_complexities=False)
        assert estimator._improved_kernel_search(2, 4, 4, k, 1) == pytest.approx(expected, abs=1e-12, rel=0)

    with pytest.raises(ValueError, match='w must be in the range'):
        KernelSearch(MRProblem(q=2, m=4, n=4, k=8, r=1), w=4)


def test_kernel_search_variants_table():
    """Reproduce all four cost columns and hybrid parameters in tab:ks-variants of [ABCPSV]_."""
    # q, m=n, k, r, original, improved, hybrid original, hybrid improved, a_original, a_improved.
    rows = [
        (2, 42, 1443, 4, 169, 165, 159, 157, 32, 31),
        (2, 50, 2024, 5, 235, 230, 225, 222, 38, 38),
        (2, 56, 2499, 6, 301, 295, 290, 288, 43, 42),
        (16, 16, 143, 4, 164, 159, 155, 155, 8, 8),
        (16, 19, 195, 5, 241, 235, 230, 230, 10, 10),
        (16, 22, 255, 6, 310, 304, 300, 300, 11, 11),
        (2, 19, 81, 10, 68, 64, 59, 59, 3, 3),
        (2, 21, 121, 10, 79, 76, 73, 73, 5, 5),
        (2, 29, 190, 15, 126, 122, 118, 118, 6, 6),
    ]
    for q, n, k, r, original, improved, hybrid_original, hybrid_improved, a_original, a_improved in rows:
        estimator = KernelSearch(MRProblem(q, n, n, k, r), w=2.81, bit_complexities=False)
        assert floor(estimator._kernel_search(q, n, n, k, r)) == original
        assert floor(estimator._improved_kernel_search(q, n, n, k, r)) == improved
        assert floor(estimator.time_complexity()) == hybrid_improved
        lv_expected = 5 if (q, n, k, r) == (2, 19, 81, 10) else 0
        assert estimator.optimal_parameters() == {'a': a_improved, 'lv': lv_expected}
        # The estimator uses the improved solver; enumerate the original solver for its table column.
        choices = []
        for lv in range(r):
            for a in range(ceil((k - lv) / n)):
                solver = estimator._kernel_search(q, n, n - a, k - lv - a * n, r)
                cost = estimator.hybridization_factor(a, lv)
                cost += estimator._log2_sum(estimator.hybrid_reduction_cost(a, lv), solver)
                choices.append((cost, a, lv))
        cost, a, lv = min(choices)
        assert floor(cost) == hybrid_original
        assert (a, lv) == (a_original, lv_expected)
