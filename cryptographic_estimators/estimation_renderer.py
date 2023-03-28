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


from .base_constants import BASE_ALGORITHM, BASE_PARAMETERS, BASE_TIME, BASE_MEMORY, BASE_ADDITIONALO, BASE_QUANTUMO, BASE_TILDEO_ESTIMATE
from .helper import concat_all_tables, round_or_truncate
from copy import deepcopy
from prettytable import PrettyTable
from sage.all import RR


class EstimationRenderer():
    def __init__(self, show_quantum_complexity=0, show_tilde_o_time=0, show_all_parameters=0, precision=1, truncate=0) -> None:
        """
        Creates an estimation renderer
        INPUT:

        - ``show_quantum_complexity`` -- show quantum time complexity (default: false)
        - ``show_tilde_o_time`` -- show Ō time complexity (default: false)
        - ``show_all_parameters`` -- show all optimization parameters (default: false)
        - ``precision`` -- number of decimal digits output (default: 1)
        - ``truncate`` -- truncate rather than round the output (default: false)
        """
        self._show_quantum_complexity = show_quantum_complexity
        self._show_tilde_o_time = show_tilde_o_time
        self._show_all_parameters = show_all_parameters
        self._precision = precision
        self._truncate = truncate

    def as_table(self, estimation_result: dict) -> None:
        """
        Prints the given estimation dictionary as a table
        """
        estimation = deepcopy(estimation_result)
        if estimation == {}:
            raise ValueError("No algorithms associated with this estimator.")

        key = list(estimation.keys())[0]
        tables = []
        tbl = self._create_initial_table_containing_algorithm_column(
            estimation)
        tables.append(tbl)

        for j in estimation[key].keys().__reversed__():
            if j == BASE_QUANTUMO and not self._show_quantum_complexity:
                continue
            if j == BASE_TILDEO_ESTIMATE and not self._show_tilde_o_time:
                continue
            if j == BASE_ADDITIONALO:
                continue

            tbl = self._create_subtable_containing_all_columns(j, estimation)
            self._add_rows(tbl, estimation)
            tables.append(tbl)

            if j == BASE_QUANTUMO:
                tbl._min_width = {BASE_TIME: len(BASE_QUANTUMO)}

        tbl_join = concat_all_tables(tables)

        print(tbl_join)

    def _create_initial_table_containing_algorithm_column(self, estimation: dict) -> PrettyTable:
        """
        creates a `PrettyTable` with the analysis results, containg
            - expected runtime and memory
            - optimal parameters

        """
        table = PrettyTable([BASE_ALGORITHM])
        table.padding_width = 1
        table.title = ' '
        table.align[BASE_ALGORITHM] = "l"

        for i in estimation.keys():
            table.add_row([i])

        return table

    def _create_subtable_containing_all_columns(self, sub_table_name: str, estimation: dict):
        """
        Creates a `PrettyTable` subtable.

        INPUT:

        - ``sub_table_name`` -- TODO
        - ``estimation`` the estimation dictionary containing the results
        """
        algorithm_name = list(estimation.keys())[0]
        table_columns = [
            i for i in list(estimation[algorithm_name][sub_table_name].keys())
            if i != BASE_PARAMETERS or self._show_all_parameters
        ]
        table = PrettyTable(table_columns, min_table_width=len(sub_table_name))
        table.padding_width = 1
        table.title = sub_table_name
        if BASE_TIME in table_columns:
            table.align[BASE_TIME] = "r"
        if BASE_MEMORY in table_columns:
            table.align[BASE_MEMORY] = "r"
        return table

    def _add_rows(self, sub_table: PrettyTable, estimation: dict) -> PrettyTable:
        """

        INPUT:

        - ``tbl`` -- current `PrettyTable` table
        - ``truncate`` -- bool: if set the value will be truncated
        - ``estimation`` the estimation dictionary containing the results

        """
        for i in estimation.keys():
            row = [estimation[i][sub_table.title][k]
                   for k in sub_table.field_names]
            row = [round_or_truncate(
                i, self._truncate, self._precision) if i in RR else i for i in row]
            sub_table.add_row(row)
        return sub_table
