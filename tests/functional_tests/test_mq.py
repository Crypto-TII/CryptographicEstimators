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
    PseudoOilAttack
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


# Parameters of [POS26]_ (https://github.com/maxostuzzi/MQ_chemistry) for MAYO SL1 and QR-UOV SL1 and the
# bit complexity given for them by eval_complexity_tree.py, (n, m, q, k, l, bs, complexity).
POS26_PAPER = [
    (860, 78, 16, 32, 14, [3, 3, 3, 3, 3, 3, 3, 3], 146.3983),
    (840, 100, 7, 54, 12, [4, 4, 5, 5, 5], 172.1836),
]


@pytest.mark.parametrize("n, m, q, k, l, bs, complexity", POS26_PAPER)
def test_pseudo_oil_attack_matches_paper(n, m, q, k, l, bs, complexity):
    """The estimator reproduces the complexity of the parameters of [POS26]_."""
    estimator = PseudoOilAttack(MQProblem(n=n, m=m, q=q))
    assert round(estimator.time_complexity(k=k, l=l, B=sum(bs), p=len(bs)), 4) == complexity


# Output of optimisation.py of [POS26]_, minimized over p = 1, ..., 4: (n, m, q, complexity, (k, l, B, p)).
POS26_OPTIMISATION = [
    (30, 13, 3, 15.6254, (5, 2, 3, 1)),
    (60, 15, 16, 30.1135, (3, 2, 5, 3)),
]


@pytest.mark.parametrize("n, m, q, complexity, parameters", POS26_OPTIMISATION)
def test_pseudo_oil_attack_matches_optimisation_script(n, m, q, complexity, parameters):
    """The estimator reproduces the optimum found by the optimisation script of [POS26]_."""
    estimator = PseudoOilAttack(MQProblem(n=n, m=m, q=q))
    assert round(estimator.time_complexity(), 4) == complexity
    assert (estimator.k(), estimator.l(), estimator.B(), estimator.p()) == parameters
