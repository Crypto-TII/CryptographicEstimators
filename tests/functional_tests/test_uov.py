import pytest

from cryptographic_estimators.UOVEstimator import IntersectionFI, ReconciliationFI, UOVProblem

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


# The intersection attack column of the same Table 3 of [FI26]_. Every one of these UOV parameter
# sets has v = n - m < 2m, so all four take the branch of Equations (13) and (14), with a solution
# space of dimension 2m - v and no probability factor.
FI26_TABLE_3_INTERSECTION = [
    ("uov-Ip", 256, 112, 44, 128, 128.37924912118416, 69.07449487572099, (1, 7, 13)),
    ("uov-Is", 16, 160, 64, 159, 158.54631604013366, 84.57063131471372, (1, 16, 16)),
    ("uov-III", 256, 184, 72, 182, 181.5318408236012, 96.34332946632665, (1, 14, 18)),
    ("uov-V", 256, 244, 96, 223, 223.25950266940245, 117.59119654685068, (1, 22, 22)),
]


@pytest.mark.parametrize(
    "name, q, n, m, complexity, time, memory, parameters", FI26_TABLE_3_INTERSECTION
)
def test_intersection_fi_matches_table_3(name, q, n, m, complexity, time, memory, parameters):
    """The estimator reproduces the intersection attack column of Table 3 of [FI26]_."""
    estimator = IntersectionFI(UOVProblem(n=n, m=m, q=q, theta=None))
    assert round(estimator.time_complexity()) == complexity
    assert estimator.time_complexity() == time
    assert estimator.memory_complexity() == memory
    assert (estimator.l(), estimator.k(), estimator.D()) == parameters


# The intersection attack column of Table 8 of [FI26]_, which reruns the UOV parameters of [3] over
# other fields of the same size. Unlike Tables 3 and 4, these rows tell the two readings of
# Equations (13) to (16) apart: for (5, 3) and (7, 2) below, ell = 1 already admits a solving degree
# yet the cheapest attack is at ell = 2, so the estimator must minimise over all ell rather than
# stop at the first admissible one, exactly as the code of Appendix D of [FI26]_ does.
FI26_TABLE_8_INTERSECTION = [
    ("112/44 (3,5)", 3**5, 112, 44, 159, 158.84273567879052, 84.26369431067656, (1, 11, 18)),
    ("112/44 (5,3)", 5**3, 112, 44, 165, 165.3121491934552, 87.36753228948233, (2, 19, 20)),
    ("112/44 (7,2)", 7**2, 112, 44, 165, 164.713065083476, 87.14513986814589, (2, 19, 20)),
    ("160/64 (3,2)", 3**2, 160, 64, 196, 196.33713606070725, 103.73009918086757, (1, 21, 22)),
]


@pytest.mark.parametrize(
    "name, q, n, m, complexity, time, memory, parameters", FI26_TABLE_8_INTERSECTION
)
def test_intersection_fi_matches_table_8(name, q, n, m, complexity, time, memory, parameters):
    """The estimator reproduces the intersection attack column of Table 8 of [FI26]_."""
    estimator = IntersectionFI(UOVProblem(n=n, m=m, q=q, theta=None))
    assert round(estimator.time_complexity()) == complexity
    assert estimator.time_complexity() == time
    assert estimator.memory_complexity() == memory
    assert (estimator.l(), estimator.k(), estimator.D()) == parameters
