from tests.external_estimators.helpers.optimize import bjmm_depth_2_qc_complexity
from tests.external_estimators.helpers.estimator import (
    prange_complexity,
    dumer_complexity,
    stern_complexity,
    ball_collision_decoding_complexity,
    bjmm_depth_2_complexity,
    bjmm_depth_3_complexity,
    bjmm_complexity,
    bjmm_depth_2_disjoint_weight_complexity,
    bjmm_depth_2_partially_disjoint_weight_complexity,
    both_may_depth_2_complexity,
    may_ozerov_complexity,
    may_ozerov_depth_2_complexity,
    may_ozerov_depth_3_complexity,
)

# TODO: Move into a docstring
# def test_sd_raises_error_when_invalid_parameters_are_passed():
#     e = [Dumer, Prange, MayOzerov, BJMM, BJMMpdw, BJMMdw, BothMay, Stern]
#     with pytest.raises(ValueError, match="k must be smaller or equal to n"):
#         SDEstimator(n=1, k=5, w=2, excluded_algorithms=e)


def ext_estimates_with_prange():
    inputs = [
        (
            100,
            50,
            2,
            (
                "Dumer",
                "BallCollision",
                "BJMM",
                "BJMMplus",
                "BJMMpdw",
                "BJMMdw",
                "BothMay",
                "MayOzerov",
                "Stern",
            ),
        )
    ]
    expected_outputs = [
        {
            "Prange": {
                "additional_information": {
                    "gauss": 10.929258408636972,
                    "permutations": 2.014646775964401,
                },
                "estimate": {
                    "memory": 12.688250309133178,
                    "parameters": {"r": 4},
                    "time": 19.587761374376097,
                },
            }
        }
    ]
    inputs_with_expected_outputs = list(zip(inputs, expected_outputs))
    return inputs_with_expected_outputs


# def ext_all():
