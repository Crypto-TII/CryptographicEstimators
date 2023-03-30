from cryptographic_estimators.SDEstimator.SDAlgorithms import Prange, Dumer, BallCollision, BJMMd2, BJMMd3, BJMM, \
    BJMMdw, \
    BJMMpdw, BothMay, MayOzerov, MayOzerovD2, MayOzerovD3, Stern, BJMM_plus
from cryptographic_estimators.SDEstimator import SDProblem
from .module.estimator import prange_complexity, dumer_complexity, stern_complexity, ball_collision_decoding_complexity, \
    bjmm_depth_2_complexity, bjmm_depth_3_complexity, bjmm_complexity, bjmm_depth_2_disjoint_weight_complexity, \
    bjmm_depth_2_partially_disjoint_weight_complexity, both_may_depth_2_complexity, may_ozerov_complexity, \
    may_ozerov_depth_2_complexity, may_ozerov_depth_3_complexity
from .module.optimize import bjmm_depth_2_qc_complexity

ranges = 0.01

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
    tests that all estimations match those from https://github.com/Crypto-TII/syndrome_decoding_estimator up to
    a tolerance of 0.01 bit
    """
    assert len(algos) == len(test_algos)
    for i, _ in enumerate(test_algos):
        A1 = algos[i]
        A2 = test_algos[i]
        for set in test_sets:
            n, k, w = set[0], set[1], set[2]
            Alg = A1(SDProblem(n=n, k=k, w=w), bit_complexities=0)
            Alg2 = A2(n=n, k=k, w=w)

            # Slight correction of parameter ranges leads to (slightly) better parameters in case of the
            # CryptographicEstimators for Both-May and May-Ozerov. For test we fix parameters to the once from the
            # online code.
            if Alg._name == "Both-May" or Alg._name == "May-OzerovD2" or Alg._name == "May-OzerovD3":
                too_much = [i for i in Alg2["parameters"] if i not in Alg.parameter_names()]
                for i in too_much:
                    Alg2["parameters"].pop(i)
                Alg.set_parameters(Alg2["parameters"])

            T1 = Alg.time_complexity()
            T2 = Alg2["time"]
            assert T2 - ranges <= T1 <= T2 + ranges


def test_bjmm_plus():
    """
    tests that BJMM+ estimation matches the one from https://github.com/FloydZ/Improving-ISD-in-Theory-and-Practice
     up to a tolerance of 0.01 bit
    """
    for set in test_sets:
        n, k, w = set[0], set[1], set[2]
        t = bjmm_depth_2_qc_complexity(n, k, w)
        t1 = t["time"]
        t2 = BJMM_plus(SDProblem(n, k, w), bit_complexities=0).time_complexity()
        assert t1 - ranges <= t2 <= t1 + ranges


if __name__ == "__main__":
    test_all()
    test_bjmm_plus()
