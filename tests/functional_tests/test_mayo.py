import pytest

from cryptographic_estimators.MAYOEstimator import MAYOProblem
from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.intersection_fi import IntersectionFI
from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.reconciliation_fi import ReconciliationFI

# Table 4 of [FI26]_ (Furue and Ikematsu, ePrint 2026/298): for each MAYO parameter set, the log2
# gate count of the reconciliation attack and the optimal (ell, k, D). The table indexes its rows by
# (q, n, m, o) alone, the whipping parameter k of MAYO playing no role in key recovery; the k below
# is the number of guessed coordinates.
FI26_TABLE_4 = [
    ("MAYO1", 16, 86, 78, 8, 238, (3, 2, 41)),
    ("MAYO2", 16, 81, 64, 17, 113, (1, 4, 13)),
    ("MAYO3", 16, 118, 108, 10, 314, (3, 2, 53)),
    ("MAYO5", 16, 154, 142, 12, 397, (3, 2, 66)),
]


@pytest.mark.parametrize("name, q, n, m, o, complexity, parameters", FI26_TABLE_4)
def test_reconciliation_fi_matches_table_4(name, q, n, m, o, complexity, parameters):
    """The estimator reproduces every row of Table 4 of [FI26]_.

    The whipping parameter k of MAYO is required by MAYOProblem but does not enter the attack, so
    any value serves; Table 4 of [FI26]_ likewise reports one complexity per (q, n, m, o).
    """
    estimator = ReconciliationFI(MAYOProblem(n=n, m=m, o=o, k=10, q=q))
    assert round(estimator.time_complexity()) == complexity
    assert (estimator.l(), estimator.k(), estimator.D()) == parameters


# The intersection attack column of the same Table 4 of [FI26]_. Every one of these MAYO parameter
# sets has 2o <= v = n - o, so all four take the branch of Equations (15) and (16): the solution
# space has dimension 1, leaving k = 0 as the only choice, and the reported cost includes the
# q^(v - 2o + 1) repetitions needed for the two subspaces to meet.
FI26_TABLE_4_INTERSECTION = [
    ("MAYO1", 16, 86, 78, 8, 351, (4, 0, 9)),
    ("MAYO2", 16, 81, 64, 17, 227, (4, 0, 10)),
    ("MAYO3", 16, 118, 108, 10, 478, (4, 0, 11)),
    ("MAYO5", 16, 154, 142, 12, 629, (4, 0, 14)),
]


@pytest.mark.parametrize(
    "name, q, n, m, o, complexity, parameters", FI26_TABLE_4_INTERSECTION
)
def test_intersection_fi_matches_table_4(name, q, n, m, o, complexity, parameters):
    """The estimator reproduces the intersection attack column of Table 4 of [FI26]_."""
    estimator = IntersectionFI(MAYOProblem(n=n, m=m, o=o, k=10, q=q))
    assert round(estimator.time_complexity()) == complexity
    assert (estimator.l(), estimator.k(), estimator.D()) == parameters
