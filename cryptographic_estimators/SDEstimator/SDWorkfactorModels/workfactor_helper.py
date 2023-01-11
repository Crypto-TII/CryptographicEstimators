from random import uniform as ru
from math import log2
import numpy as np
from scipy.optimize import fsolve


def inverse_binary_entropy(v):
    if v == 1:
        return 0.5
    if v < 0.00001:
        return 0

    return fsolve(lambda x: v - (-x * log2(x) - (1 - x) * log2(1 - x)), 0.0000001)[0]


def binary_entropy(c):
    if c == 0. or c == 1.:
        return 0.

    if c < 0. or c > 1.:
        return -1000

    return -(c * log2(c) + (1 - c) * log2(1 - c))


def binomial_approximation(n, k):
    if k > n or n == 0:
        return 0
    if k == n:
        return 0
    return n * binary_entropy(k / n)


def wrap(f, g):
    def inner(x):
        return f(g(*x))

    return inner


def list_of_random_tuples(x, y, z):
    return [(ru(x, y)) for _ in range(z)]


def may_ozerov_near_neighbor_time(list_size, vector_length, target_weight):
    if vector_length <= 0 or list_size < 0:
        return 100
    normed_list_size = list_size / vector_length
    if normed_list_size > 0.999999999:
        normed_list_size = 0.999999999

    normed_weight = target_weight / vector_length
    if normed_weight > 0.5:
        normed_weight = 1 - normed_weight

    d = inverse_binary_entropy(1 - normed_list_size)

    if normed_weight <= 2 * d * (1 - d):
        mo_exp = (1 - normed_weight) * (1 - binary_entropy((d - normed_weight / 2) / (1 - normed_weight)))
    else:
        mo_exp = 2 * normed_list_size + binary_entropy(normed_weight) - 1
    return max(mo_exp * vector_length, 2 * list_size - vector_length + binomial_approximation(vector_length, target_weight))


def representations_asymptotic(target_weight, weight_to_cancel, vector_length):
    if target_weight == 0. or vector_length == 0.:
        return 0
    if vector_length < target_weight or vector_length - target_weight < weight_to_cancel:
        return 0.
    return binomial_approximation(target_weight, target_weight / 2.) + binomial_approximation(vector_length - target_weight, weight_to_cancel)

