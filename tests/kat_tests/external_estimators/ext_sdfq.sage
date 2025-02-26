load("tests/external_estimators/helpers/attack_cost.sage")
load("tests/external_estimators/helpers/cost.sage")

from math import comb as binomial, log2
from itertools import chain

import sage.all


def lee_brickell_correction(k: int) -> float:
    """
    Calculate the correction term for the Lee-Brickell procedure.

    Args:
        k (int): The dimension of the code.

    Returns:
        float: The calculated correction term.

    Notes:
        See SDFqAlgorithms/leebrickell.py line 98/99
    """
    return log2(k) * 2 - log2(binomial(k, 2))


def ext_lee_brickell():
    """Generate expected complexities for Lee-Brickell SDFq problems.

    This function calculates the expected complexities for a predefined set of
    Lee-Brickell SDFq problem parameters.

    Returns:
        list of tuple: Each tuple contains:
            - tuple: Input parameters (n, k, w, q)
            - float: Corresponding expected complexity
    """

    inputs = [(256r, 128r, 64r, 251r), (961r, 771r, 48r, 31r)]

    def gen_single_kat(input: tuple):
        n, k, w, q = input
        expected_complexity = (
            log2(ISD_COST(n, k, w, q)) + log2(n) - lee_brickell_correction(k)
        )
        return input, expected_complexity

    inputs_with_expected_outputs = list(map(gen_single_kat, inputs))
    return inputs_with_expected_outputs


def ext_stern():
    """Generate expected complexities for Stern SDFq problems.

    This function calculates the expected complexities for a predefined set of
    Stern SDFq problem parameters using the Peters ISD algorithm.

    Returns:
        list of tuple: Each tuple contains:
            - tuple: Input parameters (n, k, w, q)
            - float: Corresponding expected complexity
    """

    inputs = [(256r, 128r, 64r, 251r), (961r, 771r, 48r, 31r)]

    def gen_single_kat(input):
        n, k, w, q = input
        expected_complexity, _, _ = peters_isd(n, k, q, w)
        return input, expected_complexity

    inputs_with_expected_outputs = list(map(gen_single_kat, inputs))
    return inputs_with_expected_outputs


def ext_stern_range():
    """Generate ranges of expected complexities for Stern SDFq problems.

    This function calculates the expected complexities for a range of Stern SDFq
    problem parameters using the Peters ISD algorithm.

    Returns:
        list of tuple: A flattened list where each tuple contains:
            - tuple: Input parameters (n, k, w, q)
            - float: Corresponding expected complexity

    Note:
        The function generates combinations of parameters within predefined ranges
        and q values.
    """

    inputs = [
        (
            range(50r, 70r, 5r),
            range(20r, 40r, 2r),
            [7r, 11r, 17r, 53r, 103r, 151r, 199r, 251r],
        ),
    ]

    def gen_single_range(ranges_input):
        n_range, k_range, q_values = ranges_input

        inputs = [
            (n, k, w, q)
            for n in n_range
            for k in k_range
            for w in range(4, min(n - k - 1, int(0.5 * n)))
            for q in q_values
        ]

        def gen_single_kat(input):
            n, k, w, q = input
            expected_complexity, _, _ = peters_isd(n, k, q, w)
            return input, expected_complexity

        inputs_with_expected_outputs_on_range = list(map(gen_single_kat, inputs))
        return inputs_with_expected_outputs_on_range

    inputs_with_expected_outputs = list(chain(*map(gen_single_range, inputs)))
    return inputs_with_expected_outputs
