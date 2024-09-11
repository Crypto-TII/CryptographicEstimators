load("tests/external_estimators/helpers/attack_cost.sage")
load("tests/external_estimators/helpers/cost.sage")

from math import comb as binomial, log2
from itertools import chain


def lee_brickell_correction(k: int) -> float:
    """
    Calculate the correction term for the Lee-Brickell procedure.

    Args:
        k: The dimension of the code.

    Returns:
        The calculated correction term.

    Notes:
        See SDFqAlgorithms/leebrickell.py line 98/99
    """
    return log2(k) * 2 - log2(binomial(k, 2))


def ext_lee_brickell(inputs: list[tuple]):
    """
    Generate expected complexities for Lee-Brickell SDFq problems.

    Args:
        inputs: A list of tuples, each containing (n, k, w, q) for a Lee-Brickell SDFq problem.

    Returns:
        A list of tuples, each containing the input parameters and the corresponding expected complexity.
    """

    def gen_single_case(input: tuple):
        n, k, w, q = input
        expected_complexity = (
            log2(ISD_COST(n, k, w, q)) + log2(n) - lee_brickell_correction(k)
        )
        return input, expected_complexity

    inputs_with_expected_outputs = list(map(gen_single_case, inputs))
    return inputs_with_expected_outputs


def ext_stern(inputs: list[tuple]):
    """
    Generate expected complexities for Stern SDFq problems.

    Args:
        inputs: A list of tuples, each containing (n, k, w, q) for a Stern SDFq problem.

    Returns:
        A list of tuples, each containing the input parameters and the corresponding expected complexity.
    """

    def gen_single_case(input):
        n, k, w, q = input
        expected_complexity, _, _ = peters_isd(n, k, q, w)
        return input, expected_complexity

    inputs_with_expected_outputs = list(map(gen_single_case, inputs))
    return inputs_with_expected_outputs


def ext_stern_range(inputs: list[tuple]):
    """
    Generate ranges of expected complexities for Stern SDFq problems.

    Args:
        inputs: A list of tuples, each containing (n_range, k_range, q_values) where:
            n_range is a range of 'n' values,
            k_range is a range of 'k' values,
            q_values is a list of 'q' values.

    Returns:
        A flattened list of tuples, each containing the input parameters (n, k, w, q) and
        the corresponding expected complexity for all combinations within the given ranges.
    """

    def gen_single_range(ranges_input):
        n_range, k_range, q_values = ranges_input

        inputs = [
            (n, k, w, q)
            for n in n_range
            for k in k_range
            for w in range(4, min(n - k - 1, int(0.5 * n)))
            for q in q_values
        ]

        def gen_single_case(input):
            n, k, w, q = input
            expected_complexity, _, _ = peters_isd(n, k, q, w)
            return input, expected_complexity

        inputs_with_expected_outputs_on_range = list(map(gen_single_case, inputs))
        return inputs_with_expected_outputs_on_range

    inputs_with_expected_outputs = list(chain(*map(gen_single_range, inputs)))
    return inputs_with_expected_outputs
