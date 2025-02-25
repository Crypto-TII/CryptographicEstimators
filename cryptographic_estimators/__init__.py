from .base_algorithm import BaseAlgorithm
from .base_estimator import BaseEstimator
from .base_problem import BaseProblem
from .helper import ComplexityType, concat_pretty_tables, _truncate, round_or_truncate

from .SDEstimator import *
from .MQEstimator import *
from .SDFqEstimator import *
from .RegSDEstimator import *
from .PKEstimator import *
from .LEEstimator import *
from .PEEstimator import *
from .DummyEstimator import *
from .MREstimator import *
from .UOVEstimator import *
from .MAYOEstimator import *
from .RankSDEstimator import *

# WARNING:
# This sets the MAXIMUM number of coefficients that can be calculated for any
# power series created with python-flint.
# Do not remove the power_series import; it's needed to enforce this cap.
# The chosen limit should be sufficient for most use cases, and values
# below 4000 will raise testing errors.
MAX_COEFFS = 20000
from flint import fmpq_series as power_series, ctx
ctx.cap = MAX_COEFFS
