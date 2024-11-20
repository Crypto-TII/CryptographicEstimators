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
from math import exp, log, pi


class IFAlgorithm1(IFAlgorithm):
    """
    Construct an instance of IFAlgorithm1 estimator

    Add reference to correponding paper here.
    https://eprint.iacr.org/2017/1087.pdf

    INPUT:

    - ``problem`` -- an instance of the IFProblem class
    """

    def __init__(self, problem: IFProblem, **kwargs):
        self._name = "IFAlgorithm1"
        super(IFAlgorithm1, self).__init__(problem, **kwargs)

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        n = self.problem.parameters["n"]
        N = 2 ** n

        k = (64 / 9) ** (1 / 3)

        return k * (log(N) ** (1 / 3)) * (log(log(N)) ** (2 / 3))

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        n = self.problem.parameters["n"]
        N = 2 ** n

        k = 2/(3 ** (2/3))

        #b1 = b2
        b1 = exp(k * (log(N) ** (1 / 3)) * (log(log(N)) ** (2 / 3)))

        #B'_1 / B'_2 ( B'_1 * log(B_1) + B'_2)
        
        b1_prime = (pi * b1) + 1
        b2_prime = (pi * b1) + log(N)

        return log((b1_prime / b2_prime) * (b1_prime * log(b1) + b2_prime))
