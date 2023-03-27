from cryptographic_estimators.SDEstimator.SDAlgorithms import Prange, Dumer, BallCollision, BJMMd2, BJMMd3, BJMM, BJMMdw,\
    BJMMpdw, BothMay, MayOzerov, MayOzerovD2, MayOzerovD3, Stern, BJMM_plus
from cryptographic_estimators.SDEstimator import SDProblem
from math import log2
from module.estimator import prange_complexity, dumer_complexity, stern_complexity, ball_collision_decoding_complexity, \
    bjmm_depth_2_complexity, bjmm_depth_3_complexity, bjmm_complexity, bjmm_depth_2_disjoint_weight_complexity, \
    bjmm_depth_2_partially_disjoint_weight_complexity, both_may_depth_2_complexity, may_ozerov_complexity, \
    may_ozerov_depth_2_complexity, may_ozerov_depth_3_complexity

ranges = 0.1

test_sets = [
    [100, 50, 10],
    [1284, 1028, 24],
    [3488, 2720, 64],
]

algos = [
    Prange,
    Stern,
    Dumer,
    BallCollision,
    BJMMd2,
    BJMMd3,
    BJMM,
    BJMMdw,
    BJMMpdw,
    BothMay,
    MayOzerov,
    MayOzerovD2,
    MayOzerovD3,
]

test_algos = [
    prange_complexity,
    stern_complexity,
    dumer_complexity,
    ball_collision_decoding_complexity,
    bjmm_depth_2_complexity,
    bjmm_depth_3_complexity,
    bjmm_complexity,
    bjmm_depth_2_disjoint_weight_complexity,
    bjmm_depth_2_partially_disjoint_weight_complexity,
    both_may_depth_2_complexity,
    may_ozerov_complexity,
    may_ozerov_depth_2_complexity,
    may_ozerov_depth_3_complexity,
]

def test_all():
    """
    tests all Syndrome Decoding algorithms
    """
    assert len(algos) == len(test_algos)
    for i, _ in enumerate(test_algos):
        A1 = algos[i]
        A2 = test_algos[i]
        for set in test_sets:
            n, k, w = set[0], set[1], set[2]
            T1 = A1(SDProblem(n=n, k=k, w=w)).time_complexity()
            T2 = A2(n=n, k=k, w=w)["time"] + log2(n)

            print(A1, T1, T2)
            assert T2 - ranges <= T1 <= T2 + ranges
            
            
def test_bjmm_plus1():
    t = bjmm_depth_2_qc_complexity(1284, 1028, 24)
    t1 = t["time"] + log2(1284)
    t2 = BJMM_plus(SDProblem(1284, 1028, 24)).time_complexity()
    assert t1 - ranges <= t2 <= t1 + ranges


def test_bjmm_plus2():
    t = bjmm_depth_2_qc_complexity(3488, 2720, 64)
    t1 = t["time"]+ log2(3488)
    t2 = BJMM_plus(SDProblem(3488, 2720, 64)).time_complexity()
    assert t1 - ranges <= t2 <= t1 + ranges


if __name__ == "__main__":
    test_all()
    test_bjmm_plus1()
    test_bjmm_plus2()
    