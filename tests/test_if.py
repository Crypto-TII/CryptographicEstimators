# from cryptographic_estimators.IFEstimator import *
# A = IFEstimator(n=2048)
# A.table(show_tilde_o_time=1, precision=0)

from cryptographic_estimators.IFEstimator import GNFS
from cryptographic_estimators.IFEstimator import IFProblem
TD = GNFS(IFProblem(n=4096))
print(TD)
TD._time_and_memory_complexity({})
print(TD._time_and_memory_complexity({}))

from cryptographic_estimators.IFEstimator import *
from cryptographic_estimators.IFEstimator.if_helper import M, Lfunction, D, primality_testing, pifunction

n = 1024
print(M(n))
print(Lfunction(0.5, 1, n))
print(pifunction(127))
print(D(n))
print(primality_testing(n))