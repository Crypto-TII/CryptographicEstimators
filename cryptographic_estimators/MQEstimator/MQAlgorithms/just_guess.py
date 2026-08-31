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


from cryptographic_estimators.base_algorithm import optimal_parameter
from ...MQEstimator.mq_algorithm import MQAlgorithm
from ...MQEstimator.mq_problem import MQProblem
from ..mq_constants import MQ_LAS_VEGAS
from ...MQEstimator.MQAlgorithms.booleansolve_fxl import BooleanSolveFXL
from math import log2, inf

class JustGuess(MQAlgorithm):
    def __init__(self, problem: MQProblem, **kwargs):
        """Construct an instance of Just Guess estimator.

        Just Guess is an algorithm to solve the underdetermined MQ problem [MOR26]_.

        Args:
            problem (MQProblem): MQProblem object including all necessary parameters.
            w (float): Linear algebra constant (2 <= w <= 3). Default is 2.81
            h (Optional[float]): External hybridization parameter (default: 0).
            memory_access (int): Specifies the memory access cost model.
                0 - constant (default)
                1 - logarithmic
                2 - square-root
                3 - cube-root
                Alternatively, deploy a custom function which takes as input the logarithm of the total memory usage and returns the logarithm of the memory access cost.
            complexity_type (int): Complexity type to consider.
                0 - estimate (default)
                1 - tilde O complexity

        Examples:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.just_guess import JustGuess
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = JustGuess(MQProblem(q=16, n=924, m=67))
            >>> E
            JustGuess estimator for the MQ problem with 924 variables and 67 polynomials
        """
        n, m, q = problem.get_problem_parameters()

        if not isinstance(q, int):
            raise TypeError("q must be an integer")

        if not problem.is_underdefined_system():
            raise ValueError("The MQ problem should be underdefined, i.e., m must be <= n")

        super().__init__(problem, **kwargs)
        self._name = "JustGuess"

        self.best = inf
        self.set_parameter_ranges("p", 0, m)   
        self.set_parameter_ranges("k", 0, m)

    @optimal_parameter
    def k(self):
        """Return the optimal value of k.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.just_guess import JustGuess
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = JustGuess(MQProblem(q=16, n=45, m=10))
            >>> E.k()
            2
        """
        return self._get_optimal_parameter("k")

    @optimal_parameter
    def p(self):
        """Return the optimal value of p.
        
        Examples:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.just_guess import JustGuess
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = JustGuess(MQProblem(q=16, n=45, m=10))
            >>> E.p()
            7
        """
        return self._get_optimal_parameter("p")

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): A dictionary including the parameters.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.just_guess import JustGuess
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = JustGuess(MQProblem(q=16, n=45, m=10, theta=None), bit_complexities=True)
            >>> E.time_complexity()
            22.47536929194652
    
        Tests:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.just_guess import JustGuess
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = JustGuess(MQProblem(q=16, n=924, m=67), bit_complexities=False)
            >>> E.time_complexity()
            103.96311188597973

            >>> E = JustGuess(MQProblem(q=16, n=924, m=67, theta=1), bit_complexities=True)
            >>> E.time_complexity()
            105.96311188597973

            >>> E = JustGuess(MQProblem(q=16, n=924, m=67, theta=None), bit_complexities=True)
            >>> E.time_complexity()
            109.13303688742204
        """
        n, m, q = self.problem.get_problem_parameters()
        p = parameters["p"]
        k = parameters["k"]

        def cost_assign_assign(n):
            '''
            Returns [# field mult, # field add] for matrix vector multiplication u**tAu
            '''
            return [n * (n+1)/2 + n, n * (n+1)/2 + n - 1]

        def cost_assign_var(n):
            '''
            Returns [# of field multiplications, # of field additions] to perform an inner-product between two n-dim vectors.
            '''
            return [n,n-1]

        def cost_sub_assign(k_assigned, n_lin, check = False):
            assign_assign = [cost *n_lin for cost in cost_assign_assign(k_assigned)]
            if check:
                assign_var = 0
                return [assign_assign[0] + assign_var, assign_assign[1] + assign_var]
            else:
                assign_var = [cost * n_lin for cost in cost_assign_var(k_assigned)]
                return [assign_assign[0] + assign_var[0], assign_assign[1] + assign_var[1]]

        def overhead(q,m,p,k):
            C_MQtree = p
            for i in range(p):
                C_MQtree += sum(cost_sub_assign(k+i,1))
            C_linsub = (m - k - p) * sum(cost_sub_assign(k + p, m-k-p))
            C_linsolve = 2/3*(m - k - p)**3
            C_check = sum(cost_sub_assign(m, 1, check = True)) * q * (1 - q**(-k))/(q-1)
            cost = C_MQtree + C_linsub + C_linsolve + C_check
            return cost

        if not (2 * k + p - m < 0 or m - k - p < 0 or 2 * (n-m) < p * (2*m - 2*k - p - 1) or n - 1 < (m - k - p - 1) * (m - k + 2)):
            iterations_c = q**k
            cost = overhead(q,m,p,k)
            return  log2(iterations_c * cost)

        return inf
    
    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.just_guess import JustGuess
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = JustGuess(MQProblem(q=16, n=45, m=10))
            >>> E.memory_complexity()
            16.30563428754671
        """
        n, m, q = self.problem.get_problem_parameters()
        p = parameters["p"]
        k = parameters["k"]

        if not (2 * k + p - m < 0 or m - k - p < 0 or 2 * (n-m) < p * (2*m - 2*k - p - 1) or n - 1 < (m - k - p - 1) * (m - k + 2)):
            return log2(m * n**2)

        return inf