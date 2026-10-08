from cryptographic_estimators.MQEstimator.MQAlgorithms.just_guess import JustGuess
from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
from cryptographic_estimators.MQEstimator import MQEstimator

# from cryptographic_estimators.MAYOEstimator import MAYOEstimator
# E = MAYOEstimator(n=66, m=64, o=8, k=9, q=16)
# print(E.table())

from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.reconciliation_fi import ReconciliationFI
from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
E = ReconciliationFI(MAYOProblem(n=86, m=78, o=8, k=10, q=16))
print(E.memory_complexity())
