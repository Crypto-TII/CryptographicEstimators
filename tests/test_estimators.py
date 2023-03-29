from cryptographic_estimators.MQEstimator import MQEstimator, MQProblem, Bjorklund, BooleanSolveFXL, F5, HybridF5, KPG, CGMTA, MHT, Lokshtanov, DinurFirst, DinurSecond, Crossbred
from cryptographic_estimators.SDEstimator import SDEstimator, Prange, Dumer, BallCollision, BJMM, BJMMdw, BJMMpdw, BothMay, MayOzerov, Stern, BJMM_plus
import pytest


def test_estimates_with_bjorklund():
    excluded_algorithms = [
        DinurFirst, DinurSecond, BooleanSolveFXL,
        HybridF5, Lokshtanov, Crossbred,
        F5, KPG, CGMTA, MHT
    ]

    mq_estimator = MQEstimator(
        100, 50, 2, excluded_algorithms=excluded_algorithms)
    result = mq_estimator.estimate()
    expected_result = {
        'Bjorklund': {'estimate': {'time': 95.50814347964285, 'memory': 36.48546485189783, 'parameters': {'lambda_': 16/49}}, 'additional_information': {}},
        'ExhaustiveSearch': {'estimate': {'time': 52.48921146923813, 'memory': 16.844129532345626, 'parameters': {}}, 'additional_information': {}}}

    assert expected_result == result


def test_mq_raises_exception_with_bjorklund():
    e = [
        DinurFirst, DinurSecond, BooleanSolveFXL,
        HybridF5, Lokshtanov, Crossbred,
        F5, KPG, CGMTA, MHT
    ]

    with pytest.raises(TypeError, match="q must be equal to 2"):
        Bjorklund(MQProblem(100, 50, 4))
        mq_estimator = MQEstimator(100, 50, 4, excluded_algorithms=e)
        mq_estimator.estimate()


def test_sd_raises_error_when_invalid_parameters_are_passed():
    e = [
        Dumer, Prange, MayOzerov,
        BJMM, BJMMpdw, BJMMdw, BothMay, Stern
    ]
    with pytest.raises(ValueError, match="k must be smaller or equal to n"):
        SDEstimator(n=1, k=5, w=2, excluded_algorithms=e)


def test_estimates_with_prange():
    excluded_algorithms = [Dumer, BallCollision, BJMM, BJMM_plus,
                           BJMMpdw, BJMMdw, BothMay, MayOzerov, Stern]
    sd_estimator = SDEstimator(
        100, 50, 2, excluded_algorithms=excluded_algorithms)
    result = sd_estimator.estimate()
    expected_result = {
        'Prange': {
            'additional_information': {
                'gauss': 10.929258408636972,
                'permutations': 2.014646775964401
            },
            'estimate': {
                'memory': 12.688250309133178,
                'parameters': {'r': 4},
                'time': 19.587761374376097}
        }
    }

    assert result == expected_result
