from math import floor, isfinite, log2

import pytest

from cryptographic_estimators.MREstimator import KernelSearch, MRProblem


# Improved Kernel Search column in the supplied Cryptanalysis of MinRank 2.0
# manuscript (main_review_v21.tex, tab:ks-variants), in field operations, w=2.81.
KERNEL_SEARCH_TABLE = [
    (2, 42, 42, 1443, 4, 165),
    (2, 50, 50, 2024, 5, 230),
    (2, 56, 56, 2499, 6, 295),
    (16, 16, 16, 143, 4, 159),
    (16, 19, 19, 195, 5, 235),
    (16, 22, 22, 255, 6, 304),
    (2, 19, 19, 81, 10, 64),
    (2, 21, 21, 121, 10, 76),
    (2, 29, 29, 190, 15, 122),
]


@pytest.mark.parametrize('q, m, n, k, r, expected', KERNEL_SEARCH_TABLE)
def test_kernel_search_matches_manuscript(q, m, n, k, r, expected):
    estimator = KernelSearch(MRProblem(q, m, n, k, r), w=2.81, bit_complexities=False)
    # Disable the existing hybrid wrapper to compare the standalone solver.
    assert floor(estimator.time_complexity(a=0, lv=0)) == expected


# Full-precision outputs of improved_kernel_search in the supplied
# artifacts/hybrid_kernel_search/kernel_seach_estimator.py, with bit_complexities=False.
# Include k=m (fallback), k<m, k=m+1, and m dividing k (one expected rank check).
REFERENCE_COSTS = [
    ((2, 4, 4, 4, 1), (7.906890595608519, 8.604775689421102, 8.832890014164741)),
    ((2, 4, 4, 3, 1), (7.0, 7.829976483801489, 8.087462841250339)),
    ((2, 4, 4, 5, 1), (8.523561956057012, 8.919250746483815, 9.066089190457772)),
    ((2, 4, 4, 8, 1), (10.20945336562895, 10.517698959448076, 10.63662462054365)),
    ((7, 9, 8, 15, 4), (32.62205941962906, 32.623589644009414, 32.62450975360673)),
    ((16, 15, 15, 78, 6), (157.50308065894413, 157.50308206419888, 157.50308390638997)),
]


@pytest.mark.parametrize('parameters, expected', REFERENCE_COSTS)
@pytest.mark.parametrize('index, w', enumerate((2, 2.81, 3)))
def test_kernel_search_matches_reference_artifact(parameters, expected, index, w):
    estimator = KernelSearch(MRProblem(*parameters), w=w, bit_complexities=False)
    assert estimator.time_complexity(a=0, lv=0) == pytest.approx(expected[index], abs=1e-12, rel=0)


def test_original_kernel_search_rank_check():
    estimator = KernelSearch(MRProblem(q=2, m=4, n=4, k=4, r=1), bit_complexities=False)
    # Two guesses, each with 20 construction, 80 elimination, and 128 rank-check operations.
    assert estimator.time_complexity(a=0, lv=0) == pytest.approx(log2(2 * (20 + 80 + 128)))


def test_improved_kernel_search_rank_check():
    estimator = KernelSearch(MRProblem(q=2, m=4, n=4, k=8, r=1), bit_complexities=False)
    # Two outer guesses: 36+144 setup, then two last-vector guesses costing 36+80+192 each.
    assert estimator.time_complexity(a=0, lv=0) == pytest.approx(log2(2 * (36 + 144 + 2 * (36 + 80 + 192))))


def test_kernel_search_large_exponent():
    estimator = KernelSearch(MRProblem(q=2, m=1100, n=1100, k=2200, r=1050), bit_complexities=False)
    time = estimator.time_complexity(a=0, lv=0)
    assert isfinite(time)
    assert 2100 < time < 2200


@pytest.mark.parametrize('a, lv', [(0, 0), (4, 3)])
def test_kernel_search_bit_conversion(a, lv):
    problem = MRProblem(q=16, m=15, n=15, k=78, r=6)
    basic = KernelSearch(problem, bit_complexities=False).time_complexity(a=a, lv=lv)
    bits = KernelSearch(problem).time_complexity(a=a, lv=lv)
    assert bits == pytest.approx(problem.to_bitcomplexity_time(basic))


def test_kernel_search_hybrid_optimization():
    estimator = KernelSearch(MRProblem(q=7, m=9, n=10, k=15, r=4), bit_complexities=False)
    costs = [estimator.time_complexity(a=a, lv=lv) for a in range(3) for lv in range(4)]
    assert estimator.time_complexity() == pytest.approx(min(costs))
    parameters = estimator.optimal_parameters().copy()
    assert estimator.time_complexity(**parameters) == pytest.approx(min(costs))
    estimator.reset()
    assert estimator.time_complexity() == pytest.approx(min(costs))


@pytest.mark.parametrize('a, lv', [(2, 0), (2, 1)])
def test_kernel_search_fully_reduced_instance(a, lv):
    estimator = KernelSearch(MRProblem(q=2, m=4, n=4, k=8, r=1), bit_complexities=False)
    # No unknowns remain; only the existing hybrid reduction is charged.
    expected = estimator.hybridization_factor(a, lv) + estimator.cost_reduction(a, lv)
    assert estimator.time_complexity(a=a, lv=lv) == pytest.approx(expected)


def test_kernel_search_memory_bound():
    estimator = KernelSearch(MRProblem(q=2, m=4, n=4, k=8, r=1, memory_bound=0))
    assert estimator.time_complexity() == float('inf')


@pytest.mark.parametrize('w', [1.99, 3.01])
def test_kernel_search_invalid_linear_algebra_constant(w):
    with pytest.raises(ValueError, match='w must be in the range'):
        KernelSearch(MRProblem(q=2, m=4, n=4, k=8, r=1), w=w)
