import pytest

from cryptographic_estimators.UOVEstimator import ReconciliationFI, UOVProblem

# Table 3 of [FI26]_ (Furue and Ikematsu, ePrint 2026/298): for each UOV parameter set, the log2
# gate count of the reconciliation attack and the optimal (ell, k, D). `time` and `memory` pin the
# unrounded model output. theta=None selects the gate conversion 2*log2(q)^2 + log2(q) that
# Section 5 of [FI26]_ applies to produce the table.
FI26_TABLE_3 = [
    ("uov-Ip", 256, 112, 44, 141, 141.3502087237885, 75.27349581618392, (1, 26, 18)),
    ("uov-Is", 16, 160, 64, 176, 176.48367368079795, 93.25312349565213, (1, 42, 22)),
    ("uov-III", 256, 184, 72, 208, 207.5218546761562, 109.0384474318432, (1, 46, 26)),
    ("uov-V", 256, 244, 96, 258, 258.35614376024665, 134.83770870084402, (1, 64, 32)),
]


@pytest.mark.parametrize("name, q, n, m, complexity, time, memory, parameters", FI26_TABLE_3)
def test_reconciliation_fi_matches_table_3(name, q, n, m, complexity, time, memory, parameters):
    """The estimator reproduces every row of Table 3 of [FI26]_.

    A UOV key has an m-dimensional oil space, so the o of Section 4.3 of [FI26]_ is m here, not the
    n - m vinegar count; the (ell, k, D) of each row would not come out otherwise.
    """
    estimator = ReconciliationFI(UOVProblem(n=n, m=m, q=q, theta=None))
    assert round(estimator.time_complexity()) == complexity
    assert estimator.time_complexity() == time
    assert estimator.memory_complexity() == memory
    assert (estimator.l(), estimator.k(), estimator.D()) == parameters
