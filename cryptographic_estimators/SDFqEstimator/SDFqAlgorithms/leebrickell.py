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

from ...SDFqEstimator.sdfq_algorithm import SDFqAlgorithm
from ...SDFqEstimator.sdfq_problem import SDFqProblem
from ...SDFqEstimator.sdfq_helper import binom, log2
from ...base_algorithm import optimal_parameter
from ..sdfq_constants import *
from types import SimpleNamespace


class LeeBrickell(SDFqAlgorithm):
    def __init__(self, problem: SDFqProblem, **kwargs):
        """Construct an instance of Lee-Brickell's estimator [LB88]_.

        Expected weight distribution:

            +--------------------------------+-------------------------------+
            | <----------+ n - k +---------> | <----------+ k +------------> |
            |               w-p              |              p                |
            +--------------------------------+-------------------------------+

        Args:
            problem (SDFqProblem): An SDProblem object including all necessary parameters.

        Tests:
            >>> from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import LeeBrickell
            >>> from cryptographic_estimators.SDFqEstimator import SDFqProblem
            >>> LeeBrickell(SDFqProblem(n=961,k=771,w=48,q=31)).time_complexity()
            140.31928490910389

        Examples:
            >>> from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import LeeBrickell
            >>> from cryptographic_estimators.SDFqEstimator import SDFqProblem
            >>> LeeBrickell(SDFqProblem(n=100,k=50,w=10,q=5))
            Lee-Brickell estimator for syndrome decoding problem with (n,k,w) = (100,50,10) over Finite Field of size 5
        """
        self._name = "LeeBrickell"
        super(LeeBrickell, self).__init__(problem, **kwargs)
        _, _, w, _ = self.problem.get_parameters()
        self.set_parameter_ranges("p", 0, max(w // 2,1))
        self.is_syndrome_zero = int(problem.is_syndrome_zero)
    
    @optimal_parameter
    def p(self):
        """Returns the optimal parameter $p$ used in the algorithm optimization.
    
        Examples:
            >>> from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import LeeBrickell
            >>> from cryptographic_estimators.SDFqEstimator import SDFqProblem
            >>> A = LeeBrickell(SDFqProblem(n=100,k=50,w=10,q=5))
            >>> A.p()
            2
        """
        return self._get_optimal_parameter("p")

    def _are_parameters_invalid(self, parameters: dict):
        """Checks if the given parameter set is invalid.
    
        Args:
            parameters (dict): The parameter set to be checked.
    
        Returns:
            bool: True if the parameter set is invalid, False otherwise.
        """
        n, k, w, _ = self.problem.get_parameters()
        par = SimpleNamespace(**parameters)
        if par.p > w or k < par.p or n - k < w - par.p:
            return True
        return False

    def _time_and_memory_complexity(self, parameters: dict, verbose_information=None):
        """Return the time complexity of Lee-Brickell's algorithm over Fq, where q > 2,
        for the given set of parameters.
    
        Note:
            This optimization assumes that the algorithm is executed on the generator matrix.
    
        Args:
            parameters (dict): A dictionary of parameters.
            verbose_information (dict, optional): If set to a dictionary, `permutations`,
                `gauß`, and `list` will be returned.
    
        Examples:
            >>> from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import LeeBrickell
            >>> from cryptographic_estimators.SDFqEstimator import SDFqProblem
            >>> A = LeeBrickell(SDFqProblem(n=100,k=50,q=3,w=10))
            >>> A.p()
            2
        """
        n, k, w, q = self.problem.get_parameters()
        par = SimpleNamespace(**parameters)

        solutions = self.problem.nsolutions
        enum = binom(k, par.p) * (q-1)**(max(0, par.p-self.is_syndrome_zero))
        # Beullens code uses (contrary to his paper)
        #enum = k**par.p * q**(max(0, par.p-self.is_syndrome_zero))
        memory = log2(k * n)

        Tp = max(log2(binom(n, w)) - log2(binom(n - k, w - par.p)) - log2(binom(k, par.p)) - solutions, 0)
        Tg = k*k
        time = Tp + log2(Tg + enum) + log2(n)
        if verbose_information is not None:
            verbose_information[VerboseInformation.PERMUTATIONS.value] = Tp
            verbose_information[VerboseInformation.GAUSS.value] = Tg
            verbose_information[VerboseInformation.LISTS.value] = [enum]

        return time, memory

    def __repr__(self):
        rep = "Lee-Brickell estimator for " + str(self.problem)
        return rep
