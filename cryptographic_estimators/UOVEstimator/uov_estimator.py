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


from .uov_algorithm import UOVAlgorithm
from .uov_problem import UOVProblem
from ..base_estimator import BaseEstimator
from math import inf
from ..MQEstimator.MQAlgorithms.lokshtanov import Lokshtanov

class UOVEstimator(BaseEstimator):
    """
    Construct an instance of UOVEstimator

    INPUT:

    - ``n`` -- number of variables
    - ``m`` -- number of polynomials
    - ``q`` -- order of the finite field (default: None)
    - ``w`` -- linear algebra constant (default: 2)
    - ``theta`` -- exponent of the conversion factor (default: 2)
        - If ``0 <= theta <= 2``, every multiplication in GF(q) is counted as `log2(q) ^ theta` binary operation.
        - If ``theta = None``, every multiplication in GF(q) is counted as `2 * log2(q) ^ 2 + log2(q)` binary operation.
    - ``h`` -- external hybridization parameter (default: 0)
    - ``excluded_algorithms`` -- a list/tuple of algorithms to be excluded (default: [])
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
    - ``complexity_type`` -- complexity type to consider (0: estimate, 1: tilde O complexity, default: 0)
    - ``bit_complexities`` -- determines if complexity is given in bit operations or basic operations (default 1: in bit)

    """
    excluded_algorithms_by_default = []

    def __init__(self, n: int, m: int, q:int, memory_bound=inf, **kwargs):
        super(UOVEstimator, self).__init__(
            UOVAlgorithm,
            UOVProblem(n=n, m=m, q=q, memory_bound=memory_bound, **kwargs),
            **kwargs
        )
        self._estimator_type = "scheme"

    def table(self, show_quantum_complexity=0, show_tilde_o_time=0,
              show_all_parameters=0, precision=1, truncate=0):
        """
        Print table describing the complexity of each algorithm and its optimal parameters

        INPUT:

        - ``show_quantum_complexity`` -- show quantum time complexity (default: False)
        - ``show_tilde_o_time`` -- show Ō time complexity (default: False)
        - ``show_all_parameters`` -- show all optimization parameters (default: False)
        - ``precision`` -- number of decimal digits output (default: 1)
        - ``truncate`` -- truncate rather than round the output (default: False)

        EXAMPLES::

            sage: from cryptographic_estimators.UOVEstimator import UOVEstimator
            sage: A = UOVEstimator(n=24, m=10, q=2)
            sage: A.table() # long time
            +--------------------+--------------+---------------+------------------+
            |                    |              |    estimate   | tilde_o_estimate |
            +--------------------+--------------+------+--------+-------+----------+
            | algorithm          | attack_type  | time | memory |  time |   memory |
            +--------------------+--------------+------+--------+-------+----------+
            | DirectAttack       | key-recovery | 11.2 |    9.5 |   8.0 |      9.5 |
            | KipnisShamir       |   forgery    | 14.1 |   12.5 |    -- |       -- |
            | CollisionAttack    |   forgery    |  7.8 |   12.5 |    -- |       -- |
            | IntersectionAttack | key-recovery | 35.3 |   13.2 |    -- |       -- |
            +--------------------+--------------+------+--------+-------+----------+

        TESTS::

            from cryptographic_estimators.UOVEstimator import UOVEstimator
            sage: A = UOVEstimator(n=112, m=44, q=256)
            sage: A.table() # long time
            +--------------------+--------------+----------------+
            |                    |              |    estimate    |
            +--------------------+--------------+-------+--------+
            | algorithm          | attack_type  |  time | memory |
            +--------------------+--------------+-------+--------+
            | DirectAttack       | key-recovery | 144.5 |   59.5 |
            | KipnisShamir       |   forgery    | 211.4 |   22.1 |
            | CollisionAttack    |   forgery    | 186.1 |   22.1 |
            | IntersectionAttack | key-recovery | 180.5 |   76.4 |
            +--------------------+--------------+-------+--------+

            sage: A = UOVEstimator(n=160, m=64, q=16)
            sage: A.table() # long time
            +--------------------+--------------+----------------+
            |                    |              |    estimate    |
            +--------------------+--------------+-------+--------+
            | algorithm          | attack_type  |  time | memory |
            +--------------------+--------------+-------+--------+
            | DirectAttack       | key-recovery | 164.0 |   53.0 |
            | KipnisShamir       |   forgery    | 146.2 |   22.6 |
            | CollisionAttack    |   forgery    | 136.4 |   22.6 |
            | IntersectionAttack | key-recovery | 208.6 |   94.0 |
            +--------------------+--------------+-------+--------+

            sage: A = UOVEstimator(n=184, m=72, q=256)
            sage: A.table() # long time
            +--------------------+--------------+----------------+
            |                    |              |    estimate    |
            +--------------------+--------------+-------+--------+
            | algorithm          | attack_type  |  time | memory |
            +--------------------+--------------+-------+--------+
            | DirectAttack       | key-recovery | 216.9 |   87.0 |
            | KipnisShamir       |   forgery    | 340.4 |   24.2 |
            | CollisionAttack    |   forgery    | 298.5 |   24.2 |
            | IntersectionAttack | key-recovery | 264.6 |  117.8 |
            +--------------------+--------------+-------+--------+

            sage: A = UOVEstimator(n=244, m=96, q=256)
            sage: A.table() # long time
            +--------------------+--------------+----------------+
            |                    |              |    estimate    |
            +--------------------+--------------+-------+--------+
            | algorithm          | attack_type  |  time | memory |
            +--------------------+--------------+-------+--------+
            | DirectAttack       | key-recovery | 276.8 |  108.6 |
            | KipnisShamir       |   forgery    | 437.0 |   25.4 |
            | CollisionAttack    |   forgery    | 394.8 |   25.4 |
            | IntersectionAttack | key-recovery | 326.1 |  148.1 |
            +--------------------+--------------+-------+--------+

        """
        super(UOVEstimator, self).table(show_quantum_complexity=show_quantum_complexity,
                                          show_tilde_o_time=show_tilde_o_time,
                                          show_all_parameters=show_all_parameters,
                                          precision=precision, truncate=truncate)
