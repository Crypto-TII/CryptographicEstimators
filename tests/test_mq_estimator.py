from cryptographic_estimators.MQEstimator import MQEstimator, Bjorklund, BooleanSolveFXL, F5, HybridF5, KPG, CGMTA, MHT, Lokshtanov, DinurFirst, DinurSecond, Crossbred
from cryptographic_estimators.SDEstimator import SDEstimator, Prange, Dumer, BallCollision, BJMM, BJMMdw, BJMMpdw, BothMay, MayOzerov, Stern


def test_estimates_with_bjorklund():
    excluded_algorithms = [DinurFirst, DinurSecond, BooleanSolveFXL,
                           F5, HybridF5, KPG, CGMTA, MHT, Lokshtanov, Crossbred]
    mq_estimator = MQEstimator(
        100, 50, 2, excluded_algorithms=excluded_algorithms)
    result = mq_estimator.estimate()
    expected_result = {
        'Bjorklund': {
            'estimate': {
                'time': 89.8642852457829,
                'memory': 36.48546485189783,
                'parameters': {'lambda_': 16/49}
            },
            'additional_information': {}},
        'ExhaustiveSearch': {
            'estimate': {
                'time': 52.48921146923813,
                'memory': 16.844129532345626,
                'parameters': {}
            },
            'additional_information': {}
        }
    }
    assert expected_result == result


def test_estimats_with_prange():
    excluded_algorithms = [Dumer, BallCollision, BJMM,
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
