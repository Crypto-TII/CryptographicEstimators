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


from ...SDEstimator.sd_algorithm import SDAlgorithm
from ...SDEstimator.sd_problem import SDProblem
from ...SDEstimator.sd_helper import _gaussian_elimination_complexity, _mem_matrix, binom, log2
from ...helper import ComplexityType
from ..sd_constants import *
from ..SDWorkfactorModels.prange import PrangeScipyModel


class Prange(SDAlgorithm):
    def __init__(self, problem: SDProblem, **kwargs):
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

            sage: from cryptographic_estimators.SDEstimator.SDAlgorithms import Prange
            sage: from cryptographic_estimators.SDEstimator import SDProblem
            sage: Prange(SDProblem(n=100,k=50,w=10))
            Prange estimator for syndrome decoding problem with (n,k,w) = (100,50,10) over Finite Field of size 2
        """
        self._name = "Prange"
        super(Prange, self).__init__(problem, **kwargs)
        self.scipy_model = PrangeScipyModel

    def _time_and_memory_complexity(self, parameters: dict, verbose_information=None):
        """
        Return time complexity of Prange's algorithm for given set of parameters

        INPUT:
        -  ``parameters`` -- dictionary including parameters
        -  ``verbose_information`` -- if set to a dictionary `permutations` and `gauß` will be returned.
        """

        n, k, w = self.problem.get_parameters()

        solutions = self.problem.nsolutions

        r = parameters["r"]
        memory = log2(_mem_matrix(n, k, r))

        Tp = max(log2(binom(n, w)) - log2(binom(n - k, w)) - solutions, 0)
        Tg = log2(_gaussian_elimination_complexity(n, k, r))
        time = Tp + Tg

        if verbose_information is not None:
            verbose_information[VerboseInformation.PERMUTATIONS.value] = Tp
            verbose_information[VerboseInformation.GAUSS.value] = Tg

        return time, memory

    def __repr__(self):
        """
        """
        rep = "Prange estimator for " + str(self.problem)
        return rep
