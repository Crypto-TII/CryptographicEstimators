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


from ..uov_algorithm import UOVAlgorithm
from ..uov_problem import UOVProblem
from math import log2
from sage.arith.misc import is_power_of_two


class KipnisShamir(UOVAlgorithm):
    """
    Construct an instance of Kipnis-Shamir estimator

    in []_, Kipnis and Shamir proposed a powerful attack against the balanced Oil
    and Vinegar signature scheme (n = 2v), which finds an equivalent private key in
    polynomial time. This key can then be used to generate signatures for arbitrary
    messages.

    INPUT:

    - ``problem`` -- an instance of the UOVProblem class
    - ``gray_code_eval_cost`` -- logarithm of the cost to evaluate one polynomial using Gray-code enumeration (default: log(n))
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
    - ``complexity_type`` -- complexity type to consider (0: estimate, 1: tilde O complexity, default: 0)

    EXAMPLES::


    """

    def __init__(self, problem: UOVProblem, **kwargs):
        super().__init__(problem, **kwargs)

        n, m, _ = self.problem.get_parameters()
        
        if n <= 2 * m:
            raise ValueError('n should be greater than 2 * m')

        self._name = "Kipnis-Shamir"
        self._gray_code_eval_cost = kwargs.get("gray_code_eval_cost", log2(n))
        self._attack_type = "forgery"

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.UOVEstimator.UOVAlgorithms.kipnis_shamir import KipnisShamir
            sage: from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            sage: E = KipnisShamir(UOVProblem(n=24, m=10, q=2))
            sage: E.time_complexity()
            13.251283982314517

        """
        n, m, q = self.problem.get_parameters()
        r = self._gray_code_eval_cost
        time = (n - 2*m) * log2(q) 
        time += log2(2 * (r ** 2) + r)
        return time + log2(n)

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.UOVEstimator.UOVAlgorithms.kipnis_shamir import KipnisShamir
            sage: from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            sage: E = KipnisShamir(UOVProblem(n=24, m=10, q=2))
            sage: E.memory_complexity()
            12.491853096329674

        """
        n, m, _ = self.problem.get_parameters()
        return log2(m * (n ** 2))
    
    def _compute_tilde_o_time_complexity(self, parameters: dict):
        """
        Return the Ō time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters
        """
        raise NotImplementedError
    
    def _compute_tilde_o_memory_complexity(self, parameters: dict):
        """
        Return the Ō memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters
        """
        raise NotImplementedError
