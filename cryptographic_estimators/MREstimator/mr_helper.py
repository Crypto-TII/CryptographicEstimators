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

class Variant(Enum):
     strassen = 1
     block_wiedemann = 2

def _strassen_complexity_(rank, ncols):
    """Returns the complexity of Gaussian elimination using Strassen algorithm"""
    w = 2.81
    return log2(7 * rank)  + (w - 1) * log2(ncols)

def _bw_complexity_(row_density, ncols):
    """Returns the complexity of block Wiedemann to find elements in the kernel of a matrix"""
    return log2(3 * row_density) + 2 * log2(ncols)

