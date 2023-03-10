from cryptographic_estimators.SDFqEstimator import *

e = []

#n = 1000
#k = 500
#w = 50
#q = 7

q = 31
n = 961;
k = 771;
w = 48
# Given q=31, n=961, k=771, w=48: parameters p=2 and l=7 yield 2^129.09509 bit ops
sd = SDFqEstimator(n, k, w, q, excluded_algorithms=e)
sd.table(show_all_parameters=True)
exit(1)


for n in range(1,100):
    print(n)
    for k in range(1,99):
        for w in range(1, n-k):
            try:
                sd = SDEstimator(n, k, w, excluded_algorithms=e)
                #(10,4,2,excluded_algorithms=e, memory_bound=30,include_tildeo=True,nsolutions=1,quantum_maxdepth=96)
                sd.table()
            except e as Exception:
                print(e, n,k,w)
