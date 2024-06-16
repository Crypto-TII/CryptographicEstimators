from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import *
from cryptographic_estimators.SDFqEstimator import SDFqProblem
from math import comb as binomial, log2 as log


load("tests/references/helpers/attack_cost.sage")
load("tests/references/helpers/cost.sage")


# global parameters
PARAMS = {"bit_complexities": 0, "is_syndrome_zero": True, "nsolutions": 0}
STERN_PARAMS = {"bit_complexities": 1, "is_syndrome_zero": True, "nsolutions": 0}


# correction term due to correction of the LeeBrickell procedure, see SDFqAlgorithms/leebrickell.py line 98/99
def lee_brickell_correction(k):
    return log(k, 2) * 2 - log(binomial(k, 2), 2)


def gen_sdfq_lee_brickell(argument_tuples, epsilon):
    """
    Special value test for Lee-Brickell, with an error tolerance of epsilon.

    Args:
        argument_tuples: A list of tuples where each tuple contains (n, k, w, q) for the LeeBrickell-SDFq problem.
        epsilon: The error tolerance for comparison.
    """

    def test_single_case(tup):
        n, k, w, q = tup
        p = 2

        expected_complexity = (
            log(ISD_COST(n, k, w, q), 2) + log(n, 2) - lee_brickell_correction(k)
        )
        actual_complexity = LeeBrickell(
            SDFqProblem(n, k, w, q, **PARAMS), **PARAMS
        ).time_complexity(p=p)

        return (
            expected_complexity - epsilon
            < actual_complexity
            < expected_complexity + epsilon
        )

    results = list(map(test_single_case, argument_tuples))
    print(results)


def gen_sdfq_stern(argument_tuples, epsilon):
    """
    Special value test for Stern, with an error tolerance of epsilon.

    Args:
        argument_tuples: A list of tuples where each tuple contains (n, k, w, q) for the Stern-SDFq problem.
        epsilon: The error tolerance for comparison.
    """

    def test_single_case(tup):
        n, k, w, q = tup
        expected_complexity, _, _ = peters_isd(n, k, q, w)
        actual_complexity = Stern(
            SDFqProblem(n, k, w, q, **STERN_PARAMS), **STERN_PARAMS
        ).time_complexity()
        return (
            expected_complexity - epsilon
            < actual_complexity
            < expected_complexity + epsilon
        )

    results = list(map(test_single_case, argument_tuples))
    print(results)


def gen_sdfq_stern_range(argument_tuples, epsilon=0.05):
    """
    Range test for Stern, comparing against peters_isd results.

    Args:
        argument_tuples: A list of tuples where each tuple contains (n, k, w, q) for the Stern-SDFq problem with parameter ranges ("l", 1, n - k).
        epsilon: The error tolerance for comparison.
    """

    def test_single_case(tup):
        n, k, w, q = tup
        A = Stern(SDFqProblem(n, k, w, q, **STERN_PARAMS), **STERN_PARAMS)
        A.set_parameter_ranges("l", 1, n - k)

        actual_complexity = A.time_complexity()
        expected_complexity, _, _ = peters_isd(n, k, q, w)

        return (
            expected_complexity - epsilon
            < actual_complexity
            < expected_complexity + epsilon
        )

    results = list(map(test_single_case, argument_tuples))
    return results


if __name__ == "__main__":
    print(lee_brickell_correction(9))
    input()
    gen_sdfq_lee_brickell([(256, 128, 64, 251), (961, 771, 48, 31)], 0.01)
    gen_sdfq_stern([(256, 128, 64, 251), (961, 771, 48, 31)], 0.01)
    n_range, k_range, q_values = (
        range(50, 70, 5),
        range(20, 40, 2),
        [7, 11, 17, 53, 103, 151, 199, 251],
    )
    argument_tuples_stern_range = [
        (n, k, w, q)
        for n in n_range
        for k in k_range
        for w in range(4, min(n - k - 1, int(0.5 * n)))
        for q in q_values
    ]
    gen_sdfq_stern_range(
        argument_tuples_stern_range,
        0.05,
    )
