from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import *
from cryptographic_estimators.SDFqEstimator import SDFqProblem

PARAMS = {"bit_complexities": 0, "is_syndrome_zero": True, "nsolutions": 0}
STERN_PARAMS = {"bit_complexities": 1, "is_syndrome_zero": True, "nsolutions": 0}


def test_sdfq_lee_brickell(test_data):
    """
    Test for the LeeBrickell-SDFq problem, with an error tolerance of epsilon.
    """
    inputs, expected_outputs = test_data("test_sdfq", "test_sdfq_lee_brickell")
    inputs_with_exp_outputs = zip(inputs, expected_outputs)
    epsilon = 0.01

    def test_single_case(input_with_exp_output):
        input, expected_complexity = input_with_exp_output
        n, k, w, q = input
        p = 2

        actual_complexity = LeeBrickell(
            SDFqProblem(n, k, w, q, **PARAMS), **PARAMS
        ).time_complexity(p=p)

        assert abs(actual_complexity - expected_complexity) < epsilon

    map(test_single_case, inputs_with_exp_outputs)


def test_sdfq_stern(test_data):
    """
    Test for the Stern-SDFq problem, with an error tolerance of epsilon.
    """
    inputs, expected_outputs = test_data("test_sdfq", "test_sdfq_stern")
    inputs_with_exp_outputs = zip(inputs, expected_outputs)
    epsilon = 0.01

    def test_single_case(input_with_exp_output):
        input, expected_complexity = input_with_exp_output
        n, k, w, q = input

        actual_complexity = Stern(
            SDFqProblem(n, k, w, q, **STERN_PARAMS), **STERN_PARAMS
        ).time_complexity()

        assert abs(actual_complexity - expected_complexity) < epsilon

    map(test_single_case, inputs_with_exp_outputs)


def test_sdfq_stern_range(test_data: callable):
    """
    Test Stern-SDFq problem with range inputs and an error tolerance of epsilon.
    """
    range_inputs, expected_outputs = test_data("test_sdfq", "test_sdfq_stern_range")
    epsilon = 0.05

    for ranges_input, expected_complexities in zip(range_inputs, expected_outputs):
        n_range, k_range, q_values = ranges_input
        inputs = [
            (n, k, w, q)
            for n in n_range
            for k in k_range
            for w in range(4, min(n - k - 1, int(0.5 * n)))
            for q in q_values
        ]

        for input_data, expected_complexity in zip(inputs, expected_complexities):
            n, k, w, q = input_data
            algorithm = Stern(SDFqProblem(n, k, w, q, **STERN_PARAMS), **STERN_PARAMS)
            algorithm.set_parameter_ranges("l", 1, n - k)
            actual_complexity = algorithm.time_complexity()
            assert abs(actual_complexity - expected_complexity) < epsilon
