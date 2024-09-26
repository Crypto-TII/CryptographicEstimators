from math import log, inf

load("tests/external_estimators/helpers/cost.sage")
load("tests/external_estimators/helpers/attack_cost.sage")

# Beullens


def ext_beullens():
    """Special value test."""

    inputs = [(250r, 125r, q) for q in [11r, 17r, 31r, 53r]]

    def gen_single_kat(input):
        n, k, q = input
        expected_complexity = attack_cost(n, k, q) + log(n, 2r)

        return input, expected_complexity

    inputs_with_expected_outputs = list(map(gen_single_kat, inputs))
    return inputs_with_expected_outputs


def ext_beullens_range():
    """Small values test."""
    inputs = [
        (n, k, q) for n in range(100r, 103r) for k in range(50r, 53r) for q in [7r, 11r]
    ]

    def gen_single_kat(input):
        n, k, q = input

        candidate_1 = attack_cost(n, k, q)
        candidate_2 = attack_cost(n, k, q)

        if candidate_1 is None and candidate_2 is None:
            return None

        final_candidate = min(candidate_1, candidate_2)
        if final_candidate == inf:
            return None

        expected_complexity = final_candidate + log(n, 2)

        return input, expected_complexity

    inputs_with_expected_outputs = list(map(gen_single_kat, inputs))

    return [element for element in inputs_with_expected_outputs if element is not None]


# BBPS
