from .base_algorithm import BaseAlgorithm
from .base_estimator import BaseEstimator
from .base_problem import BaseProblem
from .helper import ComplexityType, concat_pretty_tables, _truncate, round_or_truncate
from . import SDEstimator
from . import MQEstimator
from . import SDFqEstimator
from . import PKEstimator
from . import LEEstimator
from . import PEEstimator
from . import DummyEstimator
from . import MREstimator
<<<<<<< HEAD
from . import UOVEstimator
=======
from . import UOVEstimator
from . import MAYOEstimator
from . import IFEstimator

# WARNING:
# This sets the MAXIMUM number of coefficients that can be calculated for any
# power series created with python-flint.
# Do not remove the power_series import; it's needed to enforce this cap.
# The chosen limit should be sufficient for most use cases, and values
# below 4000 will raise testing errors.
MAX_COEFFS = 20000
from flint import fmpq_series as power_series, ctx
ctx.cap = MAX_COEFFS
>>>>>>> b86eaac (feat: implement Integer Factoring estimator using GNFS Coppersmith)
