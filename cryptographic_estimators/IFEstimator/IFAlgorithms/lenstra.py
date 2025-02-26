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


from ..if_algorithm import IFAlgorithm
from ..if_problem import IFProblem
from ..if_helper import *
from math import log2, sqrt



class Lenstra(IFAlgorithm):
    """

    INPUT:

    - ``problem`` -- an instance of the IFProblem class
    """

    def __init__(self, problem: IFProblem, **kwargs):
        self._name = "Lenstra"
        super(Lenstra, self).__init__(problem, **kwargs)

    def _time_and_memory_complexity(self, parameters: dict, consider_arithmetic = True):
        """
        # Realizes time complexity of Lenstra factorization algorithm [Len17]_ source: https://eprint.iacr.org/2017/1087.pdf (p.6)

        INPUT:
        - ``parameters`` -- dictionary including the parameters
        - ``consider_arithmetic `` if true, consider the complexity of arithmetic on an elliptic curve over Z_{2**n}

        """
        n = self.problem.parameters["n"]    #bit size of the number to factor
        time = Lfunction(0.5, sqrt(2), n)
        if consider_arithmetic: time+=2*log2(n) 
        memory = log2(4*n+2*n) #4n to store the curve and a point on it + 2n to store one multiple of the point at a time

        return time, memory
    
    def _tilde_o_time_and_memory_complexity(self, parameters: dict):
        """
        # Realizes time complexity of Lenstra factorization algorithm [Len] source: https://eprint.iacr.org/2017/1087.pdf (p.6) 
        # DOES NOT CONSIDER THE COMPLEXITY OF ELLIPTIC CURVE ARITHMETIC   

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        time, memory = self._time_and_memory_complexity(parameters, consider_arithmetic=False)

        return time, memory


