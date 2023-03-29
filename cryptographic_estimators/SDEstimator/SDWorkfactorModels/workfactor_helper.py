# ****************************************************************************
# Copyright 2023 Technology Innovation Institute
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ****************************************************************************


from random import uniform as ru
from math import log2
from scipy.optimize import fsolve
from typing import Any


def inverse_binary_entropy(v: float):
    """
    compute the inverse binary entropy function:
        eg the unique x in [0, ..., 1/2], v = H^{-1}(x)
    """
    if v == 1:
        return 0.5
    if v < 0.00001:
        return 0

    return fsolve(lambda x: v - (-x * log2(x) - (1 - x) * log2(1 - x)), 0.0000001)[0]


def binary_entropy(c: float):
    """
    computes the binary entropy function H
    """
    if c == 0. or c == 1.:
        return 0.

    if c < 0. or c > 1.:
        return -1000

    return -(c * log2(c) + (1 - c) * log2(1 - c))


def binomial_approximation(n: float, k: float):
    """
    computes the binomial coefficietn (n over k) via Sterlings approximation
    """
    if k > n or n == 0:
        return 0
    if k == n:
        return 0
    return n * binary_entropy(k / n)


def wrap(f, g):
    """
    helper function for the scipy optimization framework
    """
    def inner(x):
        return f(g(*x))

    return inner


def list_of_random_tuples(x: float, y: float, z: int):
    """
    """
    return [(ru(x, y)) for _ in range(z)]


def may_ozerov_near_neighbor_time(list_size: float, vector_length: float, target_weight: float):
    """
    computes the asymptotic runtime of the Nearest Neighbour Algorithm by
    May-Ozerov [MO15]_
    """
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
        mo_exp = (1 - normed_weight) * (1 -
                                        binary_entropy((d - normed_weight / 2) / (1 - normed_weight)))
    else:
        mo_exp = 2 * normed_list_size + binary_entropy(normed_weight) - 1
    return max(mo_exp * vector_length, 2 * list_size - vector_length + binomial_approximation(vector_length, target_weight))


def representations_asymptotic(target_weight: float, weight_to_cancel: float, vector_length: float):
    """
    computes the asymptotic number of representations of a length-$vector_length$ weight-$target_weight$ vector
    via the sum of two length-$vector_length$ weight-($target_weight$/2+$weight_to_cancel$) vectors
    """
    if target_weight == 0. or vector_length == 0.:
        return 0
    if vector_length < target_weight or vector_length - target_weight < weight_to_cancel:
        return 0.
    return binomial_approximation(target_weight, target_weight / 2.) + binomial_approximation(vector_length - target_weight, weight_to_cancel)
