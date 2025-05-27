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

from ..base_algorithm import BaseAlgorithm
from .pk_problem import PKProblem


class PKAlgorithm(BaseAlgorithm):
    def __init__(self, problem: PKProblem, **kwargs):
        """Base class for Permuted Kernel algorithms.

        Args:
            problem (PKProblem): LEProblem object including all necessary parameters
            **kwargs: Additional keyword arguments
                cost_for_list_operation (int): Cost in Fq additions for one list operation in the SBC and KMP algorithms (default: n-m)
                memory_for_list_element (int): Memory in Fq elements for one list element in the SBC and KMP algorithms (default: n-m)
        """
        super(PKAlgorithm, self).__init__(problem, **kwargs)
        n, m, _, _ = self.problem.get_parameters()
        self.cost_for_list_operation = kwargs.get("cost_for_list_operation", n - m)
        self.memory_for_list_element = kwargs.get("memory_for_list_element", n - m)

        if self.memory_for_list_element > self.cost_for_list_operation:
            raise ValueError("Cost per list element must be at least as high as its memory usage")
