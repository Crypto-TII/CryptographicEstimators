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
    - ``excluded_algorithms`` -- a list/tuple of MQ algorithms to be excluded (default: [Lokshtanov])
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
            sage: A = UOVEstimator(n=14, m=12, q=8)
            sage: A.table()
            +--------------+---------------+
            |              |    estimate   |
            +--------------+------+--------+
            | algorithm    | time | memory |
            +--------------+------+--------+
            | DirectAttack | 33.2 |   21.8 |
            +--------------+------+--------+

        TESTS::

            sage: from cryptographic_estimators.UOVEstimator import UOVEstimator
            sage: A = UOVEstimator(n=112, m=44, q=256) # long time
            sage: A.table()
            +--------------+----------------+
            |              |    estimate    |
            +--------------+-------+--------+
            | algorithm    |  time | memory |
            +--------------+-------+--------+
            | DirectAttack | 144.5 |   59.5 |
            +--------------+-------+--------+

            sage: A = UOVEstimator(n=66, m=64, q=16)
            sage: A.table(show_tilde_o_time=1) # long time
            +--------------+----------------+------------------+
            |              |    estimate    | tilde_o_estimate |
            +--------------+-------+--------+-------+----------+
            | algorithm    |  time | memory |  time |   memory |
            +--------------+-------+--------+-------+----------+
            | DirectAttack | 166.1 |   48.1 | 150.2 |     45.1 |
            +--------------+-------+--------+-------+----------+

            sage: A = UOVEstimator(n=78, m=64, q=16)
            sage: A.table(show_tilde_o_time=1) # long time
            +--------------+----------------+------------------+
            |              |    estimate    | tilde_o_estimate |
            +--------------+-------+--------+-------+----------+
            | algorithm    |  time | memory |  time |   memory |
            +--------------+-------+--------+-------+----------+
            | DirectAttack | 166.1 |   48.1 | 150.2 |     45.1 |
            +--------------+-------+--------+-------+----------+
        """
        super(UOVEstimator, self).table(show_quantum_complexity=show_quantum_complexity,
                                          show_tilde_o_time=show_tilde_o_time,
                                          show_all_parameters=show_all_parameters,
                                          precision=precision, truncate=truncate)
