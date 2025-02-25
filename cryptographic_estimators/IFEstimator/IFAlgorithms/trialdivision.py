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
from math import exp, log, floor



class TrialDivision(IFAlgorithm):
    """
    INPUT:
    - ``problem`` -- an instance of the IFProblem class
    """

    def __init__(self, problem: IFProblem, **kwargs):
        self._name = "TrialDivision"
        super(TrialDivision, self).__init__(problem, **kwargs)

    def _time_and_memory_complexity(self, parameters: dict, consider_division = True):
        """
        # The function realizes the following algorithm:
        1. Build a list of prime numbers up to size 2**(floor(sqrt(n))), store this list. Time: pi(floor(sqrt(n)))*time_miller_rabin
        2. For each saved prime, check if it divides our number (complexity of gcd = complexity of division)

        In case memory is limited (<pi(floor(sqrt(n))) ), go over all numbers  < sqrt(n) and test for division (without primility testing)    

        INPUT:

        - ``parameters`` -- dictionary including the parameters
        - ``consider_division'' -- flag indicating if the runtime of integer division is considered or not 

        """
        n = self.problem.parameters["n"]    # bit size of the number to factor
        memory_bound = self.problem.memory_bound
        log_prime_factors_size = floor(n/2-log2(n/2 * 0.693147180559945)) # log2 of pi(sqrt(n)) = numer of primes < 2^(sqrt(n))

        time = (n/2 - 1)       # naive brute force
        if consider_division: time+= log2(D(n)) 

        memory = log_prime_factors_size

        if memory_bound < log_prime_factors_size:       #if memory allows to store all primes < < 2^(sqrt(n)), store all primes
            tmp = log_prime_factors_size+log2(primality_testing(n)) 
            if consider_division: tmp = log_prime_factors_size+log2(primality_testing(n)+D(n)) 
            if tmp<time:                                
                time = tmp
                memory = log_prime_factors_size

        return time, memory
    
    def _tilde_o_time_and_memory_complexity(self, parameters: dict):
        """
        # The function realizes the following algorithm *WHITHOUT CONSIDERING THE RUNTIME OF DIVISION*
        1. Build a list of prime numbers up to size 2**(floor(sqrt(n))), store this list. Time: pi(floor(sqrt(n)))*time_miller_rabin
        2. For each saved prime, check if it divides our number (complexity of gcd = complexity of division = 1)

        In case memory is limited (<pi(floor(sqrt(n))) ), go over all numbers  < sqrt(n) and test for division (without primility testing)    

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        time, memory = self._time_and_memory_complexity(parameters, consider_division=False)

        return time, memory


