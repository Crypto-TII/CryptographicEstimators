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
from ..if_constants import *
from ..if_helper import *
from math import exp, log


class GNFS(IFAlgorithm):
    """
    Construct an instance of IFAlgorithm1 estimator
    The estimates as per [Len17]_  Sec. 5.5.4 https://eprint.iacr.org/2017/1087.pdf

    INPUT:

    - ``problem`` -- an instance of the IFProblem class
    """

    def __init__(self, problem: IFProblem, **kwargs):
        self._name = "GNFS"
        super(GNFS, self).__init__(problem, **kwargs)

    def _time_and_memory_complexity(self, parameters: dict, correctingfactor = True):
        """
        Return the time complexity of the General Number Field Sieve algorithm for a given set of parameters


        INPUT:

        - ``parameters`` -- dictionary including the parameters
        - ``correcting factor`` if true, adjust the runtime with the constant from [GuiSlides]_ https://people.rennes.inria.fr/Aurore.Guillevic/talks/2024-07-Douala/24-07-Douala-RSA.pdf

        """
        n = self.problem.parameters["n"]

        k = (64 / 9) ** (1 / 3)
      
        time_ln = Lfunction(1/3, k, n/lge)                 
        time = time_ln * lge                    # the multiple lge converts the value to base-2


        # memory = storing a matrix of relations size 2pi(B1) X 2pi(B1). Note that the matrix is sparce, with O(n) non-zero entries per row (p. 121 in [Cop93]_)
        # B1 = L[1/3, 2/3**(2/3)]
        B1 = Lfunction(1/3, 2/(3**(2./3)), n/lge)
        memory = (B1*lge - log2(B1) + 1) + log2(n) # log2(pi(B1)) = log2(B1)-log2(ln(B1)) = B1*lge - log2(B1); adding +1 to account for the factor 2 in 2pi(B1); 

        if correctingfactor:
            time = time - correcting_factor 


        return time, memory

    def _tilde_o_time_and_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        return self._time_and_memory_complexity(parameters,correctingfactor=False)

        
    

