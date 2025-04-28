# ****************************************************************************
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
# ****************************************************************************


from .base_constants import BASE_ALGORITHM, BASE_PARAMETERS, BASE_TIME, BASE_MEMORY, BASE_ADDITIONALO, BASE_QUANTUMO, BASE_TILDEO_ESTIMATE
from .helper import concat_all_tables, round_or_truncate
from copy import deepcopy
from prettytable import PrettyTable
from numpy import float64


class EstimationRenderer():
    def __init__(self, show_quantum_complexity=0, show_tilde_o_time=0, show_all_parameters=0, precision=1, truncate=0) -> None:
        """Creates an estimation renderer.

        Args:
            show_quantum_complexity (int): Show quantum time complexity (default: 0).
            show_tilde_o_time (int): Show Ō time complexity (default: 0).
            show_all_parameters (int): Show all optimization parameters (default: 0).
            precision (int): Number of decimal digits output (default: 1).
            truncate (int): Truncate rather than round the output (default: 0).
        """
        self._show_quantum_complexity = show_quantum_complexity
        self._show_tilde_o_time = show_tilde_o_time
        self._show_all_parameters = show_all_parameters
        self._precision = precision
        self._truncate = truncate

    def as_table(self, estimation_result: dict) -> None:
        """Prints the given estimation dictionary as a table."""
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
        """ Creates a table containing:
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

    #TODO: Sub_table_name description
    def _create_subtable_containing_all_columns(self, sub_table_name: str, estimation: dict):
        """Creates a `PrettyTable` subtable.
    
        Args:
            sub_table_name (str): 
            estimation (dict): The estimation dictionary containing the results
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
        """Add rows to the table based on estimation.
    
        Args:
            sub_table (PrettyTable): Current PrettyTable table
            estimation (dict): The estimation dictionary containing the results
    
        Returns:
            PrettyTable: Updated table with added rows
        """
        for i in estimation.keys():
            row = [estimation[i][sub_table.title][k]
                   for k in sub_table.field_names]
            row = [round_or_truncate(
                i, self._truncate, self._precision) if type(i) in (float, float64) else i for i in row]
            sub_table.add_row(row)
        return sub_table
