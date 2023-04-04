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

from ...SDFqEstimator.sdfq_algorithm import SDFqAlgorithm
from ...SDFqEstimator.sdfq_problem import SDFqProblem
from ...SDFqEstimator.sdfq_helper import _mem_matrix, binom, log2
from ..sdfq_constants import *


class Prange(SDFqAlgorithm):
    def __init__(self, problem: SDFqProblem, **kwargs):
        """
        Construct an instance of Prange's estimator [Pra62]_
        expected weight distribution::
            +--------------------------------+-------------------------------+
            | <----------+ n - k +---------> | <----------+ k +------------> |
            |                w               |              0                |
            +--------------------------------+-------------------------------+

        INPUT:
        - ``problem`` -- SDProblem object including all necessary parameters

        EXAMPLES::
            sage: from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import Prange
            sage: from cryptographic_estimators.SDFqEstimator import SDFqProblem
            sage: Prange(SDFqProblem(n=100,k=50,w=10,q=3))
            Prange estimator for syndrome decoding problem with (n,k,w) = (100,50,10) over Finite Field of size 3

        """
        self._name = "Prange"
        super(Prange, self).__init__(problem, **kwargs)

    def _time_and_memory_complexity(self, parameters: dict, verbose_information=None):
        """
        Return time complexity of Prange's algorithm for given set of parameters

        INPUT:
        -  ``parameters`` -- dictionary including parameters
        -  ``verbose_information`` -- if set to a dictionary `permutations` and `gauß` will be returned.

        """

        n, k, w, q = self.problem.get_parameters()
        solutions = self.problem.nsolutions

        memory = log2(_mem_matrix(n, k, 0)) + log2(n)

        Tp = max(log2(binom(n, w)) - log2(binom(n - k, w)) - solutions, 0)
        Tg = log2(k*k)
        time = Tp + Tg + log2(n)

        if verbose_information is not None:
            verbose_information[VerboseInformation.PERMUTATIONS.value] = Tp
            verbose_information[VerboseInformation.GAUSS.value] = Tg
        
        return time, memory

    def __repr__(self):
        rep = "Prange estimator for " + str(self.problem)
        return rep
