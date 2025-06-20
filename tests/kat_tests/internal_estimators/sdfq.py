from typing import Tuple
from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import *
from cryptographic_estimators.SDFqEstimator import SDFqProblem

PARAMS = {"bit_complexities": 0, "is_syndrome_zero": True, "nsolutions": 0}
STERN_PARAMS = {"bit_complexities": 1, "is_syndrome_zero": True, "nsolutions": 0}


def lee_brickell(
    input: Tuple[int, int, int, int], epsilon: float = 0.01
) -> Tuple[float, float]:
    """Estimate produced by the CryptographicEstimators library for the Lee-Brickell SDFq problem.

    This function calculates the complexity estimate for a single case of the Lee-Brickell SDFq problem.

    Args:
        input (Tuple[int, int, int, int]): A tuple containing (n, k, w, q) parameters for the SDFq problem.
        epsilon (float, optional): The maximum error tolerance for this estimation. Defaults to 0.01.

    Returns:
        Tuple[float, float]: A tuple containing:
            - float: The actual complexity calculated by the LeeBrickell algorithm.
            - float: The epsilon value used for error tolerance.
    """
    n, k, w, q = input
    p = 2

    actual_complexity = LeeBrickell(
        SDFqProblem(n, k, w, q, **PARAMS), **PARAMS
    ).time_complexity(p=p)

    return actual_complexity, epsilon


def stern(input, epsilon=0.01):
    """Estimate produced by the CryptographicEstimators library for the Stern-SDFq problem.

    This function calculates the complexity estimate for a single case of the Stern-SDFq problem.

    Args:
        input (Tuple[int, int, int, int]): A tuple containing (n, k, w, q) parameters for the SDFq problem.
        epsilon (float, optional): The maximum error tolerance for this estimation. Defaults to 0.01.

    Returns:
        Tuple[float, float]: A tuple containing:
            - float: The actual complexity calculated by the Stern algorithm.
            - float: The epsilon value used for error tolerance.
    """
    n, k, w, q = input

    actual_complexity = Stern(
        SDFqProblem(n, k, w, q, **STERN_PARAMS), **STERN_PARAMS
    ).time_complexity()

    return actual_complexity, epsilon


def stern_range(input, epsilon=0.05):
    """Estimate produced by the CryptographicEstimators library for the Stern-SDFq problem with parameter range optimization.

    This function calculates the complexity estimate for a single case of the Stern-SDFq problem,
    optimizing over a range of 'l' parameter values.

    Args:
        input (Tuple[int, int, int, int]): A tuple containing (n, k, w, q) parameters for the SDFq problem.
        epsilon (float, optional): The maximum error tolerance for this estimation. Defaults to 0.05.

    Returns:
        Tuple[float, float]: A tuple containing:
            - float: The actual complexity calculated by the Stern algorithm with optimized 'l'.
            - float: The epsilon value used for error tolerance.

    Note:
        This function sets the parameter range for 'l' from 1 to (n-k) for each problem instance,
        allowing the algorithm to optimize over this range when calculating the time complexity.
    """
    n, k, w, q = input

    algorithm = Stern(SDFqProblem(n, k, w, q, **STERN_PARAMS), **STERN_PARAMS)
    algorithm.set_parameter_ranges("l", 1, n - k)
    actual_complexity = algorithm.time_complexity()

    return actual_complexity, epsilon
