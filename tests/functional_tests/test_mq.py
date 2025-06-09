import pytest
from cryptographic_estimators.MQEstimator import (
    MQProblem,
    MQEstimator,
    MQProblem,
    Bjorklund,
    BooleanSolveFXL,
    CGMTA,
    Crossbred,
    DinurFirst,
    DinurSecond,
    F5,
    HybridF5,
    KPG,
    Lokshtanov,
    MHT,
)


def test_mq_raises_exception_with_bjorklund():
    e = [
        DinurFirst,
        DinurSecond,
        BooleanSolveFXL,
        HybridF5,
        Lokshtanov,
        Crossbred,
        F5,
        KPG,
        CGMTA,
        MHT,
    ]

    with pytest.raises(TypeError, match="q must be equal to 2"):
        Bjorklund(MQProblem(100, 50, 4))
        mq_estimator = MQEstimator(100, 50, 4, excluded_algorithms=e)
        mq_estimator.estimate()
