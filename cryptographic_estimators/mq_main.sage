from MQEstimator.mq_estimator import MQEstimator
from MQEstimator.mq_problem import MQProblem

from MQEstimator.MQAlgorithms.boolean_solve_fxl import BooleanSolveFXL
from MQEstimator.MQAlgorithms.bjorklund import Bjorklund
from MQEstimator.MQAlgorithms.cgmta import CGMTA
from MQEstimator.MQAlgorithms.crossbred import Crossbred
from MQEstimator.MQAlgorithms.dinur1 import DinurFirst
from MQEstimator.MQAlgorithms.dinur2 import DinurSecond
from MQEstimator.MQAlgorithms.exhaustive_search import ExhaustiveSearch
from MQEstimator.MQAlgorithms.f5 import F5
from MQEstimator.MQAlgorithms.hybrid_f5 import HybridF5
from MQEstimator.MQAlgorithms.kpg import KPG
from MQEstimator.MQAlgorithms.lokshtanov import Lokshtanov
from MQEstimator.MQAlgorithms.mht import MHT

E = MQEstimator(n=15, m=15, q=2)
E.table()

