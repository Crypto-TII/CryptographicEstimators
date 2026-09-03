import pytest

from cryptographic_estimators.UOVEstimator import IntersectionFI, ReconciliationFI, UOVProblem

# Table 3 of [FI26]_ (Furue and Ikematsu, ePrint 2026/298): for each UOV parameter set, the log2
# gate count of the reconciliation attack and the optimal (ell, k, D). theta=None selects the gate
# conversion 2*log2(q)^2 + log2(q) that Section 5 of [FI26]_ applies to produce the table.
FI26_TABLE_3 = [
    ("uov-Ip", 256, 112, 44, 141, (1, 26, 18)),
    ("uov-Is", 16, 160, 64, 176, (1, 42, 22)),
    ("uov-III", 256, 184, 72, 208, (1, 46, 26)),
    ("uov-V", 256, 244, 96, 258, (1, 64, 32)),
]


@pytest.mark.parametrize("name, q, n, m, complexity, parameters", FI26_TABLE_3)
def test_reconciliation_fi_matches_table_3(name, q, n, m, complexity, parameters):
    """The estimator reproduces every row of Table 3 of [FI26]_.

    A UOV key has an m-dimensional oil space, so the o of Section 4.3 of [FI26]_ is m here, not the
    n - m vinegar count; the (ell, k, D) of each row would not come out otherwise.
    """
    estimator = ReconciliationFI(UOVProblem(n=n, m=m, q=q, theta=None))
    assert round(estimator.time_complexity()) == complexity
    assert (estimator.l(), estimator.k(), estimator.D()) == parameters


# The intersection attack column of the same Table 3 of [FI26]_. Every one of these UOV parameter
# sets has v = n - m < 2m, so all four take the branch of Equations (13) and (14), with a solution
# space of dimension 2m - v and no probability factor.
FI26_TABLE_3_INTERSECTION = [
    ("uov-Ip", 256, 112, 44, 128, (1, 7, 13)),
    ("uov-Is", 16, 160, 64, 159, (1, 16, 16)),
    ("uov-III", 256, 184, 72, 182, (1, 14, 18)),
    ("uov-V", 256, 244, 96, 223, (1, 22, 22)),
]


@pytest.mark.parametrize(
    "name, q, n, m, complexity, parameters", FI26_TABLE_3_INTERSECTION
)
def test_intersection_fi_matches_table_3(name, q, n, m, complexity, parameters):
    """The estimator reproduces the intersection attack column of Table 3 of [FI26]_."""
    estimator = IntersectionFI(UOVProblem(n=n, m=m, q=q, theta=None))
    assert round(estimator.time_complexity()) == complexity
    assert (estimator.l(), estimator.k(), estimator.D()) == parameters
