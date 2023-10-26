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

from sage.all_cmdline import *
from ..minrank_algorithm import MINRANKAlgorithm
from ..minrank_problem import MINRANKProblem
from math import log2, inf
from ..minrank_constants import *

class Support_Minors(MINRANKAlgorithm):
    """
    Construct an instance of Kernel_Search estimator

    Add reference to correponding paper here.

    INPUT:

    - ``problem`` -- an instance of the MINRANKProblem class
    """

    def __init__(self, problem: MINRANKProblem, **kwargs):
        self._name = "Support_Minors"
        super(Support_Minors, self).__init__(problem, **kwargs)

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        q = self.problem.parameters[MR_Q]
        m = self.problem.parameters[MR_M]
        n = self.problem.parameters[MR_N]
        k = self.problem.parameters[MR_K]
        r = self.problem.parameters[MR_R]
        use_gate_count= self.problem.parameters[MR_USE_GATE_COUNT]
        
        time = self._strassen_complexity_(n, n)
        
        opt_b = 1
        opt_nprime = n
        
        if k > 0:
            min_time = inf
            memory = inf
            for b in range(1,  r + 2):
                for nprime in range(r + b, n + 1):
                    temp_time_BW, temp_time_strassen = self._sm_complexity_helper_(q=q, m=m, n=n, K=k, r=r, nprime=nprime, b=b)
                    temp_time = min(temp_time_BW, temp_time_strassen)
                    if temp_time < min_time:
                        min_time = temp_time
                        opt_b = b
                        opt_nprime = nprime
                        
            if opt_b == 0:
                time = inf
            else:
                time = min_time
             

            if use_gate_count:
                time = self._ngates(time)
              
        time = log2(time)

        return time
    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        
        q = self.problem.parameters[MR_Q]
        m = self.problem.parameters[MR_M]
        n = self.problem.parameters[MR_N]
        k = self.problem.parameters[MR_K]
        r = self.problem.parameters[MR_R]
        use_gate_count= self.problem.parameters[MR_USE_GATE_COUNT]
        
        memory  = 1
        opt_b = 1
        opt_nprime = n
        
        if k > 0:
            min_time = inf
            memory = inf
            for b in range(1,  r + 2):
                for nprime in range(r + b, n + 1):
                    temp_time_BW, temp_time_strassen = self._sm_complexity_helper_(q=q, m=m, n=n, K=k, r=r, nprime=nprime, b=b)
                    temp_time = min(temp_time_BW, temp_time_strassen)
                    if temp_time < min_time:
                        min_time = temp_time
                        opt_b = b
                        opt_nprime = nprime
            if opt_b == 0:
                memory = inf
            else:
                memory = k**2 * (r + 1) * binomial(k + opt_b -1, opt_b)

            if use_gate_count:
                
                memory = log2(q) * memory

       
        memory = log2(memory)

        return memory
    
    def _BW_complexity_(self,row_density, ncols):
        return 3 * row_density * ncols ** 2
        
    def _strassen_complexity_(self,rank, ncols):
        w = 2.81    
        return 7 * rank * ncols ** (w - 1)
    
    def _sm_complexity_helper_(self,q, m, n, K, r, nprime, b):
        assert(r + b <= nprime <= n)
        assert(1 <= b < r + 2)
        temp_time_BW, temp_time_strassen = inf, inf
        if nprime <= r:
            return 1,1
    
        if self._is_condition_satisfied(q, m, nprime, K, r, b):
            temp_time_BW = self._BW_complexity_(row_density = K * (r + 1), ncols = dimension(q, nprime, K, r, b))
            temp_time_strassen =  self._strassen_complexity_(rank=self.dimension(q, nprime, K, r, b) - 1, ncols=self.dimension(q, nprime, K, r, b))
        return temp_time_BW, temp_time_strassen
    
    def expected_dimension_of_support_minors_equations(self,q, m, n, K, r, b):
        """
        Return the expected number of linearly independent support minors equations

        """
        if q == 2:
            temp = 0
            for j in range(1, b + 1):
                temp += sum([(-1) ** (i + 1) * binomial(n, r + i) * binomial(m + i - 1, i) * binomial(K, j - i) for i in
                             range(1, j + 1)])
        else:
            temp = sum(
                [(-1) ** (i + 1) * binomial(n, r + i) * binomial(m + i - 1, i) * binomial(K + b - i - 1, b - i) for i in
                 range(1, b + 1)])
        return temp


    def dimension(self,q, n, K, r, b):
        """
        Dimension of the smallest vector space spanned by monomials containing the support minors equations
        """
        if q == 2:
            temp = binomial(n, r) * sum([binomial(K, j) for j in range(1, b + 1)])
        else:
            temp = binomial(n, r) * binomial(K + b - 1, b)
        return temp


    def _is_condition_satisfied(self,q, m, n, K, r, b):
        """
        Return the true value of the condition
        ``dimension(q, n, K, r, b) - 1 <= expected_dimension_of_support_minors_equations(q, m, n, K, r, b)``

        """
        return self.dimension(q, n, K, r, b) - 1 <= self.expected_dimension_of_support_minors_equations(q, m, n, K, r, b)

    