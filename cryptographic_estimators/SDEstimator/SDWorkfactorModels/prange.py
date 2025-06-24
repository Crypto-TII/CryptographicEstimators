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


from .scipy_model import ScipyModel
from ..sd_problem import SDProblem
from .workfactor_helper import binomial_approximation


class PrangeScipyModel(ScipyModel):
    def __init__(self, par_names: list, problem: SDProblem, iterations, accuracy):
        """Optimization model for workfactor computation of Prange's algorithm."""
        par_names += ["p"]
        super().__init__(par_names, problem, iterations, accuracy)

    def _build_model_and_set_constraints(self):
        self.constraints = [
            {'type': 'ineq', 'fun': self._inject_vars(
                lambda x: 1 - self.rate(x) - self.w(x) - x.p)},
            {'type': 'ineq', 'fun': self._inject_vars(
                lambda x: self.rate(x) - x.p)},
            {'type': 'ineq', 'fun': self._inject_vars(
                lambda x: self.w(x) - x.p)},
        ]

    def _memory(self, x):
        return 0

    def _time_lists(self, x):
        return [binomial_approximation(self.rate(x), x.p)]

    def _time_perms(self, x):
        return max(0,
                   binomial_approximation(1., self.w(x))
                   - binomial_approximation(self.rate(x), x.p)
                   - binomial_approximation(1 - self.rate(x), self.w(x) - x.p)
                   - self.nsolutions
                   )

    def _time(self, x):
        x = self.set_vars(*x)
        return self._time_perms(x) + max(self._time_lists(x))
