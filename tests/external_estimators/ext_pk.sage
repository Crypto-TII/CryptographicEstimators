load("tests/external_estimators/helpers/cost.sage")
load("tests/external_estimators/helpers/kmp_cost.sage")
load("tests/external_estimators/helpers/our_cost.sage")

from itertools import chain


def ext_kmp():
    """Special value test."""

    inputs = [
        (94r, 55r, 509r, 1r),
    ]

    def gen_single_kat(input):
        n, m, q, ell = input
        _, _, _, _, _, expected_complexity = kmp_cost_numerical(n, m, ell, q)

        return input, float(expected_complexity)

    inputs_with_expected_outputs = list(map(gen_single_kat, inputs))
    return inputs_with_expected_outputs


def ext_sbc():
    """Special value test."""

    inputs = [
        (94r, 55r, 509r, 1r),
    ]

    def gen_single_kat(input):
        n, m, q, ell = input
        _, _, _, _, _, expected_complexity = compute_new_cost(n, m, q, ell)

        return input, float(expected_complexity)

    inputs_with_expected_outputs = list(map(gen_single_kat, inputs))
    return inputs_with_expected_outputs


def ext_kmp_range():
    """Small values test."""

    inputs = [
        (n, m, q, ell)
        for n in range(30r, 100r)
        for m in range(int(0.3 * n), int(0.7 * n))
        for ell in range(1r, 2r)
        for q in [7r, 11r, 17r, 53r, 103r, 151r, 199r, 251r]
    ]

    def gen_single_kat(input):
        n, m, q, ell = input
        if q ^ ell < n:
            return None

        # we adapted the KMP algorithm to allow to enumerate on m.
        _, _, _, _, _, expected_complexity = kmp_cost_numerical(n, m, ell, q)

        return input, float(expected_complexity)

    inputs_with_expected_outputs = list(map(gen_single_kat, inputs))

    return [element for element in inputs_with_expected_outputs if element is not None]


def ext_sbc_range():
    """Small values test."""

    inputs = [
        (n, m, q, ell)
        for n in range(30r, 50r, 5r)
        for m in range(n // 2r, n // 2r + 5r)
        for ell in range(1r, 3r)
        for q in [53r, 151r, 251r]
    ]

    def gen_single_kat(input):
        n, m, q, ell = input
        if q ^ ell < n:
            return None

        _, _, _, _, _, expected_complexity = compute_new_cost(n, m, q, ell)

        return input, float(expected_complexity)

    inputs_with_expected_outputs = list(map(gen_single_kat, inputs))

    return [element for element in inputs_with_expected_outputs if element is not None]
