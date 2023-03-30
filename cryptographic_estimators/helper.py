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


from math import log2
from enum import Enum


class ComplexityType(Enum):
    """
    distinguish between normal optimisation and tilde O optimisation
    """
    ESTIMATE = 0
    TILDEO = 1


def concat_all_tables(tables):
    """

    INPUT:

    - ``tables`` -- list of `PrettyTable`
    """
    tbl_join = concat_pretty_tables(str(tables[0]), str(tables[1]))
    for i in range(2, len(tables)):
        tbl_join = concat_pretty_tables(tbl_join, str(tables[i]))
    return tbl_join


def concat_pretty_tables(t1: str, t2: str):
    """
    Merge two columns into one 
    INPUT:

    - ``t1`` -- first column
    - ``t2`` -- second column

    """
    v = t1.split("\n")
    v2 = t2.split("\n")
    vnew = ""
    for i in range(len(v)):
        vnew += v[i] + v2[i][1:] + "\n"
    return vnew[:-1]


def _truncate(x: float, precision: int):
    """
    truncate a value

    INPUT:

    - ``x`` -- value to truncate
    - ``precision`` -- number of decimial digits to truncate to

    """
    return float(int(x * 10 ** precision) / 10 ** precision)


def round_or_truncate(x: float, truncate: bool, precision: int):
    """
    eiter rounds or truncates `x` if `truncate` is `true`

    INPUT:

    - ``x`` -- value to either truncate or round
    - ``truncate`` -- if `true`: `x` will be truncated else rounded
    - ``precision`` -- number of decimial digits

    """
    val = _truncate(x, precision) if truncate \
        else round(float(x), precision)
    return '{:.{p}f}'.format(val, p=precision)
