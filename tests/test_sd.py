from cryptographic_estimators.SDEstimator.SDAlgorithms import BJMM_plus
from cryptographic_estimators.SDEstimator import SDProblem
from .modules.optimize import bjmm_depth_2_qc_complexity
from math import log2

ranges = 0.1
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
    test_bjmm_plus1()
    test_bjmm_plus2()