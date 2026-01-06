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

from ..le_algorithm import LEAlgorithm
from ..le_problem import LEProblem
from ...PEEstimator import Leon as PELeon
from ...PEEstimator.pe_problem import PEProblem


class Leon(PELeon, LEAlgorithm):
    def __init__(self, problem: LEProblem, **kwargs):
        """Complexity estimate of Leons algorithm [Leo82]_.

        Estimates are adapted versions of the scripts derived in [Beu20]_ with the code accessible at
        https://github.com/WardBeullens/LESS_Attack

        Args:
            problem (LEProblem): PEProblem object including all necessary parameters
            **kwargs: Additional keyword arguments
                codewords_needed_for_success (int): Number of low word codewords needed for success (default = 100)
                sd_parameters (dict): Dictionary of parameters for SDFqEstimator used as a subroutine (default: {})

        Examples:
            >>> from cryptographic_estimators.LEEstimator.LEAlgorithms import Leon
            >>> from cryptographic_estimators.LEEstimator import LEProblem
            >>> Leon(LEProblem(n=100,k=50,q=3))
            Leon estimator for permutation equivalence problem with (n,k,q) = (100,50,3)
        """
        LEAlgorithm.__init__(self, problem, **kwargs)
        self._name = "Leon"
        n, k, q = self.problem.get_parameters()
        PELeon.__init__(self, PEProblem(n=n, k=k, q=q), **kwargs)

    def __repr__(self):
        rep = "Leon estimator for " + str(self.problem)
        return rep
