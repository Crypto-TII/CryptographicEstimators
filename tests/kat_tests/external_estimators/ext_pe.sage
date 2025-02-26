load("tests/external_estimators/helpers/attack_cost.sage")
load("tests/external_estimators/helpers/cost.sage")


# Correction term due to correction of the LeeBrickell procedure, see SDFqAlgorithms/leebrickell.py line 98/99
def lee_brickell_correction(k):
    return log(k, 2) * 2 - log(binomial(k, 2), 2)


def ext_leon1():
    """
    Comes from some hardcoded values in:
       https://github.com/WardBeullens/LESS_Attack/blob/master/attack_cost.py

    """

    inputs = [(250r, 125r, 53r), (106r, 45r, 7r)]

    def gen_single_kat(input: tuple):
        n, k, q = input
        expected_complexity = LEON(n, k, q) + log(n, 2) - lee_brickell_correction(k)
        return input, expected_complexity

    inputs_with_expected_outputs = list(map(gen_single_kat, inputs))
    return inputs_with_expected_outputs


def ext_leon2():
    """
    Comes from some hardcoded values in:
       https://github.com/WardBeullens/LESS_Attack/blob/master/attack_cost.py
    """
    inputs = [(250r, 150r, q) for q in [11r, 17r, 53r, 103r, 151r, 199r, 251r]]

    def gen_single_kat(input: tuple):
        n, k, q = input
        expected_complexity = LEON(n, k, q) + log2(n) - lee_brickell_correction(k)
        return input, float(expected_complexity)

    inputs_with_expected_outputs = list(map(gen_single_kat, inputs))
    return inputs_with_expected_outputs


def ext_beullens():
    """
    Comes from some hardcoded values in:
       https://github.com/WardBeullens/LESS_Attack/blob/master/attack_cost.py
    """

    inputs = [(250r, 125r, 53r), (106r, 45r, 7r)]

    def gen_single_kat(input: tuple):
        n, k, q = input

        complexities = [
            attack_cost(n, k, q, False, False) + log(n, 2) - lee_brickell_correction(k)
            for _ in range(10)
        ]
        expected_complexity = min(complexities)

        return input, expected_complexity

    inputs_with_expected_outputs = list(map(gen_single_kat, inputs))
    return inputs_with_expected_outputs
