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


from ..mayo_algorithm import MAYOAlgorithm
from ..mayo_problem import MAYOProblem
from ...base_constants import BASE_KEY_RECOVERY_ATTACK
from math import log2


class KipnisShamir(MAYOAlgorithm):
    def __init__(self, problem: MAYOProblem, **kwargs):
        """Construct an instance of KipnisShamir estimator.

        First attack on the Oil and Vinegar problem, proposed by Kipnis and Shamir.
        The attack attempts to find vectors in the oil space O, by exploiting the fact
        that these vectors are more likely to be eigenvectors of some publicy-known matrices.

        Note:
            The linear algebra constant `w_ks` is set by default to 2.8 since this is the
            suggested choice in Section 5.4 of [BCCHK23]_

        Args:
            problem (MAYOProblem): Object including all necessary parameters
            w_ks (float, optional): Linear algebra constant (only for kipnis-shamir algorithm). Defaults to 2.8.
            h (int, optional): External hybridization parameter. Defaults to 0.
            excluded_algorithms (list, optional): A list/tuple of MQ algorithms to be excluded. Defaults to [Lokshtanov].
            memory_access (int, optional): Specifies the memory access cost model. Defaults to 0.
                Choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root
                or deploy custom function which takes as input the logarithm of the total memory usage.
            complexity_type (int, optional): Complexity type to consider. Defaults to 0 (estimate).
            bit_complexities (int, optional): Determines if complexity is given in bit operations or basic operations. Defaults to 1 (in bit).
        """
        super().__init__(problem, **kwargs)

        self._name = "KipnisShamir"
        self._attack_type = BASE_KEY_RECOVERY_ATTACK

        self._w_ks = kwargs.get("w_ks", 2.8)
        n, _, o, _, _ = self.problem.get_parameters()
        if n <= 2 * o:
            raise ValueError('n should be greater than 2 * o')

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.kipnis_shamir import KipnisShamir
            >>> E = KipnisShamir(MAYOProblem(n=24, m=20, o=8, k=9, q=16))
            >>> E.time_complexity()
            50.007820003461546
        """
        n, _, o, _, q = self.problem.get_parameters()
        w_ks = self._w_ks
        time = (n - 2 * o) * log2(q)
        return time + log2(n) * w_ks

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.kipnis_shamir import KipnisShamir
            >>> E = KipnisShamir(MAYOProblem(n=24, m=20, o=8, k=9, q=16))
            >>> E.memory_complexity()
            14.169925001442312
        """
        n, _, o, _, _ = self.problem.get_parameters()
        return log2(o * (n ** 2))
