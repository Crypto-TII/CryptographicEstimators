#!/usr/bin/env python3

from cryptographic_estimators.MQEstimator import MQEstimator
m = MQEstimator(n=64, m=32, q=16)
print(m.estimate(bit_complexities=0))
t = m.algorithms()[-2]
t.set_parameters({'k':0})
t.time_complexity()
print(t.best)
