from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import *
from cryptographic_estimators.SDFqEstimator import *
#from cryptographic_estimators.SDEstimator.SDAlgorithms import *
#from cryptographic_estimators.SDEstimator import *

#e = [Stern, Dumer, MayOzerov, BJMMd2, BJMMd3, BJMMdw, BJMMpdw, MayOzerovD2, MayOzerovD3, BothMay, BallCollision]
a =SDFqEstimator(n=100,k=50,w=10,q=5)#, bit_complexities=False)
a.table(show_all_parameters=True,precision=5)
p = SDFqProblem(961, 771, 48, 31)
s = Stern(p)
#print(s.time_complexity(), s.l(), s.p())

a =SDFqEstimator(n=961,k=771,w=48,q=31, bit_complexities=False)
a.table(show_all_parameters=True,precision=5)
#a=SDEstimator(100, 50, 10, memory_access=1)
#a=SDEstimator(3488,2720,64,excluded_algorithms=[BJMMdw])
#b=SDEstimator(3488,2720,64,excluded_algorithms=[BJMMdw],precision=3,memory_access=1)
#a.table(show_all_parameters=True,precision=5)
#b.table(show_all_parameters=True,precision=5)
