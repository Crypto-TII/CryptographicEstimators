from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import *
from cryptographic_estimators.SDFqEstimator import SDFqProblem

PARAMS = {"bit_complexities": 0, "is_syndrome_zero": True, "nsolutions": 0}
STERN_PARAMS = {"bit_complexities": 1, "is_syndrome_zero": True, "nsolutions": 0}


def test_sdfq_lee_brickell(test_data):
    """
    Test for the LeeBrickell-SDFq problem with an error tolerance of epsilon.
    """
    inputs_with_expected_outputs = test_data()
    epsilon = 0.01

    def test_single_case(input_with_exp_output):
        input, expected_complexity = input_with_exp_output
        n, k, w, q = input
        p = 2

        actual_complexity = LeeBrickell(
            SDFqProblem(n, k, w, q, **PARAMS), **PARAMS
        ).time_complexity(p=p)

        assert abs(actual_complexity - expected_complexity) < epsilon

    map(test_single_case, inputs_with_expected_outputs)


def test_sdfq_stern(test_data):
    """
    Test for the Stern-SDFq problem with an error tolerance of epsilon.
    """
    inputs_with_expected_outputs = test_data()
    epsilon = 0.01

    def test_single_case(input_with_exp_output):
        input, expected_complexity = input_with_exp_output
        n, k, w, q = input

        actual_complexity = Stern(
            SDFqProblem(n, k, w, q, **STERN_PARAMS), **STERN_PARAMS
        ).time_complexity()

        assert abs(actual_complexity - expected_complexity) < epsilon

    map(test_single_case, inputs_with_expected_outputs)


def test_sdfq_stern_range(test_data):
    """
    Test for the Stern-SDFq problem with an error tolerance of epsilon.

    Notes:
        This test sets the parameter range for 'l' from 1 to (n-k) for each problem instance,
        allowing the algorithm to optimize over this range when calculating the time complexity.
    """
    inputs_with_expected_outputs = test_data()
    epsilon = 0.05

    def test_single_case(input_with_exp_output):
        input, expected_complexity = input_with_exp_output
        n, k, w, q = input
        algorithm = Stern(SDFqProblem(n, k, w, q, **STERN_PARAMS), **STERN_PARAMS)
        algorithm.set_parameter_ranges("l", 1, n - k)
        actual_complexity = algorithm.time_complexity()
        assert abs(actual_complexity - expected_complexity) < epsilon

    map(test_single_case, inputs_with_expected_outputs)
