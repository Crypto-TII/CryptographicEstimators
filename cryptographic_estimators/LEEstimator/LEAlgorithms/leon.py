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

from ..le_algorithm import LEAlgorithm
from ..le_problem import LEProblem
from ...PEEstimator import Leon as PELeon
from ...PEEstimator.pe_problem import PEProblem


class Leon(PELeon, LEAlgorithm):

    def __init__(self, problem: LEProblem, **kwargs):
        """
        Complexity estimate of Leons algorithm [Leo82]_
        Estimates are adapted versions of the scripts derived in [Beu20]_ with the code accessible at
        https://github.com/WardBeullens/LESS_Attack

        INPUT:

        - ``problem`` -- PEProblem object including all necessary parameters
        - ``codewords_needed_for_success`` -- Number of low word codewords needed for success (default = 100)
        - ``sd_parameters`` -- dictionary of parameters for SDFqEstimator used as a subroutine (default: {})

        EXAMPLES::

            sage: from cryptographic_estimators.LEEstimator.LEAlgorithms import Leon
            sage: from cryptographic_estimators.LEEstimator import LEProblem
            sage: Leon(LEProblem(n=100,k=50,q=3))
            Leon estimator for permutation equivalence problem with (n,k,q) = (100,50,3)

        """
        LEAlgorithm.__init__(self, problem, **kwargs)
        self._name = "Leon"
        n, k, q = self.problem.get_parameters()
        PELeon.__init__(self, PEProblem(n=n, k=k, q=q), **kwargs)

    def __repr__(self):
        rep = "Leon estimator for " + str(self.problem)
        return rep
