load("tests/references/helpers/cost.sage")
load("tests/references/helpers/kmp_cost.sage")
load("tests/references/helpers/our_cost.sage")

from itertools import chain


def ext_kmp():
    """Special value test."""

    inputs = [
        (94, 55, 509, 1),
    ]

    def gen_single_kat(input):
        n, m, q, ell = input
        _, _, _, _, _, expected_complexity = kmp_cost_numerical(n, m, ell, q)

        return input, expected_complexity

    inputs_with_expected_outputs = list(map(gen_single_kat, inputs))
    return inputs_with_expected_outputs


def ext_sbc():
    """Special value test."""

    inputs = [
        (94, 55, 509, 1),
    ]

    def gen_single_kat(input):
        n, m, q, ell = input
        _, _, _, _, _, expected_complexity = compute_new_cost(n, m, q, ell)

        return input, expected_complexity

    inputs_with_expected_outputs = list(map(gen_single_kat, inputs))
    return inputs_with_expected_outputs


def ext_kmp_range():
    """Small values test."""

    inputs = [
        (n, m, ell, q)
        for n in range(30, 100)
        for m in range(int(0.3 * n), int(0.7 * n))
        for ell in range(1, 2)
        for q in [7, 11, 17, 53, 103, 151, 199, 251]
    ]

    def gen_single_kat(input):
        n, m, ell, q = input
        if q ^ ell < n:
            return None

        # we adapted the KMP algorithm to allow to enumerate on m.
        _, _, _, _, _, expected_complexity = kmp_cost_numerical(n, m, ell, q)

        return input, expected_complexity

    inputs_with_expected_outputs = list(map(gen_single_kat, inputs))

    return [element for element in inputs_with_expected_outputs if element is not None]


def ext_sbc_range():
    """Small values test."""

    inputs = [
        (n, m, ell, q)
        for n in range(30, 50, 5)
        for m in range(n // 2, n // 2 + 5)
        for ell in range(1, 3)
        for q in [53, 151, 251]
    ]

    def gen_single_kat(input):
        n, m, ell, q = input
        if q ^ ell < n:
            return None

        _, _, _, _, _, expected_complexity = compute_new_cost(n, m, q, ell)

        return input, expected_complexity

    inputs_with_expected_outputs = list(map(gen_single_kat, inputs))

    return [element for element in inputs_with_expected_outputs if element is not None]
