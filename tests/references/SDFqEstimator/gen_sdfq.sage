load("tests/references/helpers/attack_cost.sage")
load("tests/references/helpers/cost.sage")

from math import comb as binomial, log2


# correction term due to correction of the LeeBrickell procedure, see SDFqAlgorithms/leebrickell.py line 98/99
def lee_brickell_correction(k):
    return log2(k) * 2 - log2(binomial(k, 2))


def gen_sdfq_lee_brickell(inputs: tuple[tuple]):
    """
    Special value test for Lee-Brickell, with an error tolerance of epsilon.

    Args:
        argument_tuples: A list of tuples where each tuple contains (n, k, w, q) for the LeeBrickell-SDFq problem.
        epsilon: The error tolerance for comparison.
    """

    def gen_single_case(input: tuple):
        n, k, w, q = input
        expected_complexity = (
            log2(ISD_COST(n, k, w, q)) + log2(n) - lee_brickell_correction(k)
        )
        return expected_complexity

    expected_outputs = list(map(gen_single_case, inputs))
    return expected_outputs


def gen_sdfq_stern(inputs):
    """
    Special value test for Stern, with an error tolerance of epsilon.

    Args:
        argument_tuples: A list of tuples where each tuple contains (n, k, w, q) for the Stern-SDFq problem.
    """

    def gen_single_case(input):
        n, k, w, q = input
        expected_complexity, _, _ = peters_isd(n, k, q, w)
        return expected_complexity

    expected_outputs = list(map(gen_single_case, inputs))
    return expected_outputs


def gen_sdfq_stern_range(inputs):
    """
    Range test for Stern, comparing against peters_isd results.

    Args:
        inputs: List of tuples where each tuple have (n_range, k_range, q_values)
            n_range: Range for 'n' values (e.g., range(50, 70, 5)).
            k_range: Range for 'k' values (e.g., range(20, 40, 2)).
            q_values: A list of 'q' values.
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
            return expected_complexity

        expected_outputs_by_range = list(map(gen_single_case, inputs))
        return expected_outputs_by_range

    expected_outputs_by_inputs = list(map(gen_single_range, inputs))
    return expected_outputs_by_inputs


if __name__ == "__main__":
    # print(gen_sdfq_lee_brickell([(256, 128, 64, 251), (961, 771, 48, 31)], 0.01))
    # print(gen_sdfq_stern([(256, 128, 64, 251), (961, 771, 48, 31)], 0.01))
    print(
        gen_sdfq_stern_range(
            range(50, 70, 5),
            range(20, 40, 2),
            [7, 11, 17, 53, 103, 151, 199, 251],
            0.05,
        )
    )
