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


from .dummy_algorithm import DummyAlgorithm
from .dummy_problem import DummyProblem
from ..base_estimator import BaseEstimator
from math import inf


class DummyEstimator(BaseEstimator):
    def __init__(self, problem_parameter1: float, problem_parameter2, memory_bound=inf, **kwargs):
        """Construct an instance of DummyEstimator.

        Args:
            problem_parameter1 (float): First parameter of the problem
            problem_parameter2: Second parameter of the problem
            memory_bound: Specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
            **kwargs: Additional keyword arguments
                nsolutions: Number of solutions of the problem in logarithmic scale
        """
        super(DummyEstimator, self).__init__(DummyAlgorithm, DummyProblem(problem_parameter1=problem_parameter1,
                                                                          problem_parameter2=problem_parameter2,
                                                                          memory_bound=memory_bound, **kwargs), **kwargs)

    def table(self, show_quantum_complexity=False, show_tilde_o_time=False, show_all_parameters=False, precision=1, truncate=False, parameters_inside=False):
        """Print table describing the complexity of each algorithm and its optimal parameters.
    
        Args:
            show_quantum_complexity (int): Show quantum time complexity (default: 0)
            show_tilde_o_time (int): Show Ō time complexity (default: 0)
            show_all_parameters (int): Show all optimization parameters (default: 0)
            precision (int): Number of decimal digits output (default: 1)
            truncate (int): Truncate rather than round the output (default: 0)
        """
        super(DummyEstimator, self).table(show_quantum_complexity=show_quantum_complexity,
                                          show_tilde_o_time=show_tilde_o_time,
                                          show_all_parameters=show_all_parameters,
                                          precision=precision, truncate=truncate, 
                                          parameters_inside=parameters_inside)
