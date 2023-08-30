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

from math import log2, inf, \
    comb as binomial


def cost_to_find_random_2dim_subcodes_with_support_w(n: int, k: int, w: int):
    """
    returns the cost of finding a 2 dimensional subcode in a code of length n and dimension k and support w
    """
    if n-k<w-2:
        return inf
    return log2((k * k + binomial(k, 2))) + log2(binomial(n, w)) - log2(binomial(n - k, w - 2)) - log2(binomial(k, 2))