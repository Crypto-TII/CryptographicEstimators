from cryptographic_estimators.DUMMYEstimator import *
A = DUMMYEstimator(n=100, memory_bound=20, show_verbose_information=1)
A.table(show_all_parameters=1, show_verbose_information=1)

from cryptographic_estimators.MQEstimator import MQEstimator
MQE = MQEstimator(n=20, m=20, q=3, show_verbose_information=True)
MQE.table(show_verbose_information=True)

from cryptographic_estimators.SDEstimator import SDEstimator
SDE = SDEstimator(n=300,k=150,w=38)
SDE.table()
SDE = SDEstimator(n=300,k=150,w=38, show_verbose_information=True)
SDE.table(show_verbose_information=True)

from cryptographic_estimators.SDFqEstimator import SDFqEstimator
SDFqE = SDFqEstimator(n=100,k=50,w=30,q=3, show_verbose_information=True)
SDFqE.table(show_verbose_information=True)

from cryptographic_estimators.PKEstimator import PKEstimator
PK = PKEstimator(n=40,m=10,q=7,ell=2, show_verbose_information=True)
PK.table(show_verbose_information=True)

from cryptographic_estimators.LEEstimator import LEEstimator
LE = LEEstimator(n=30,k=20,q=251, show_verbose_information=True)
LE.table(show_verbose_information=True)

from cryptographic_estimators.PEEstimator import PEEstimator
PE = PEEstimator(n=60,k=20,q=7, show_verbose_information=True)
PE.table(show_verbose_information=True)
