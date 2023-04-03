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

from enum import  Enum


LE_CODE_LENGTH = "code length"
LE_CODE_DIMENSION = "code dimension"
LE_FIELD_SIZE = "field size"
LE_SD_PARAMETERS="sd_parameters"

class VerboseInformation(Enum):
    """
    """
    NW = "Nw_prime"
    LISTS = "L_prime"
    LISTS_SIZE = "list_size"
    NORMAL_FORM = "normal_form"
    ISD = "C_ISD"
