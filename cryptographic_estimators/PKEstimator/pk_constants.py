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

from enum import Enum


PK_COLUMNS = "columns"
PK_ROWS = "rows"
PK_FIELD_SIZE = "field size"
PK_DIMENSION = "dimension"


class VerboseInformation(Enum):
    KMP_L1 = "L1"
    KMP_L2 = "L2"
    KMP_FINAL_LIST = "final list"
    SBC_ISD = "ISD cost"
    SBC_U = "u"
