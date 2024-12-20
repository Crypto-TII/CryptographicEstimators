import pytest
from cryptographic_estimators.SDEstimator import (
    SDEstimator,
    Prange,
    Dumer,
    BJMM,
    BJMMdw,
    BJMMpdw,
    BothMay,
    MayOzerov,
    Stern,
)

from cryptographic_estimators.SDEstimator.SDAlgorithms import (
    Prange,
    Dumer,
    BJMM,
    BJMMdw,
    BJMMpdw,
    BothMay,
    MayOzerov,
    Stern,
)

def test_sd_raises_error_when_invalid_parameters_are_passed():
    e = [Dumer, Prange, MayOzerov, BJMM, BJMMpdw, BJMMdw, BothMay, Stern]
    with pytest.raises(ValueError, match="k must be smaller or equal to n"):
        SDEstimator(n=1, k=5, w=2, excluded_algorithms=e)
