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


from .mayo_algorithm import MAYOAlgorithm
from .mayo_problem import MAYOProblem
from ..base_estimator import BaseEstimator
from math import inf


class MAYOEstimator(BaseEstimator):
    """
    Construct an instance of MAYOEstimator

    INPUT:

    - ``n`` -- number of variables
    - ``m`` -- number of polynomials
    - ``o`` -- dimension of the oil space
    - ``k`` -- whipping parameter
    - ``q`` -- order of the finite field
    - ``theta`` -- exponent of the conversion factor (default: 2)
        - If ``0 <= theta <= 2``, every multiplication in GF(q) is counted as `log2(q) ^ theta` binary operation.
        - If ``theta = None``, every multiplication in GF(q) is counted as `2 * log2(q) ^ 2 + log2(q)` binary operation.
    - ``w`` -- linear algebra constant (default: 2)
    - ``h`` -- external hybridization parameter (default: 0)
     - ``excluded_algorithms`` -- a list/tuple of algorithms to be excluded (default: [])
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
    - ``complexity_type`` -- complexity type to consider (0: estimate, 1: tilde O complexity, default: 0)
    - ``bit_complexities`` -- determines if complexity is given in bit operations or basic operations (default 1: in bit)

    """

    def __init__(self, n: int, m: int, o: int, k: int, q: int, memory_bound=inf, **kwargs):
        super(MAYOEstimator, self).__init__(
            MAYOAlgorithm, 
            MAYOProblem(n=n, m=m, o=o, k=k, q=q, memory_bound=memory_bound, **kwargs), 
            **kwargs
        )
        self._estimator_type = "scheme"

    def table(self, show_quantum_complexity=0, show_tilde_o_time=0,
              show_all_parameters=0, precision=1, truncate=0):
        """
        Print table describing the complexity of each algorithm and its optimal parameters

        INPUT:

        - ``show_quantum_complexity`` -- show quantum time complexity (default: false)
        - ``show_tilde_o_time`` -- show Ō time complexity (default: false)
        - ``show_all_parameters`` -- show all optimization parameters (default: false)
        - ``precision`` -- number of decimal digits output (default: 1)
        - ``truncate`` -- truncate rather than round the output (default: false)

        TESTS::

            sage: from cryptographic_estimators.MAYOEstimator import MAYOEstimator
            sage: E = MAYOEstimator(n=66, m=64, o=8, k=9, q=16)
            sage: E.table() # long time
            +--------------+-------------+----------------+
            |              |             |    estimate    |
            +--------------+-------------+-------+--------+
            | algorithm    | attack_type |  time | memory |
            +--------------+-------------+-------+--------+
            | DirectAttack |   forgery   | 144.8 |   99.3 |
            +--------------+-------------+-------+--------+

            sage: E = MAYOEstimator(n=78, m=64, o=18, k=4, q=16)
            sage: E.table(show_all_parameters=1) # long time
            +--------------+-------------+-----------------------------+
            |              |             |           estimate          |
            +--------------+-------------+-------+--------+------------+
            | algorithm    | attack_type |  time | memory | parameters |
            +--------------+-------------+-------+--------+------------+
            | DirectAttack |   forgery   | 158.1 |  101.7 | {'K': 15}  |
            +--------------+-------------+-------+--------+------------+

            sage: E = MAYOEstimator(n=99, m=96, o=10, k=11, q=16)
            sage: E.table(show_all_parameters=1) # long time 
            +--------------+-------------+-----------------------------+
            |              |             |           estimate          |
            +--------------+-------------+-------+--------+------------+
            | algorithm    | attack_type |  time | memory | parameters |
            +--------------+-------------+-------+--------+------------+
            | DirectAttack |   forgery   | 209.6 |  136.9 | {'K': 20}  |
            +--------------+-------------+-------+--------+------------+

            sage: E = MAYOEstimator(n=133, m=128, o=12, k=12, q=16)
            sage: E.table(show_all_parameters=1) # long time
            +--------------+-------------+-----------------------------+
            |              |             |           estimate          |
            +--------------+-------------+-------+--------+------------+
            | algorithm    | attack_type |  time | memory | parameters |
            +--------------+-------------+-------+--------+------------+
            | DirectAttack |   forgery   | 274.7 |  175.0 | {'K': 24}  |
            +--------------+-------------+-------+--------+------------+

            sage: E = MAYOEstimator(n=90, m=56, o=8, k=10, q=16)
            sage: E.table(show_all_parameters=1) # long time
            +--------------+-------------+----------------------------+
            |              |             |          estimate          |
            +--------------+-------------+------+--------+------------+
            | algorithm    | attack_type | time | memory | parameters |
            +--------------+-------------+------+--------+------------+
            | DirectAttack |   forgery   | 21.4 |   56.9 | {'K': 10}  |
            +--------------+-------------+------+--------+------------+

            sage: E = MAYOEstimator(n=64, m=60, o=10, k=21, q=16)
            sage: E.table(show_all_parameters=1) # long time
            +--------------+-------------+-----------------------------+
            |              |             |           estimate          |
            +--------------+-------------+-------+--------+------------+
            | algorithm    | attack_type |  time | memory | parameters |
            +--------------+-------------+-------+--------+------------+
            | DirectAttack |   forgery   | 102.2 |   72.8 | {'K': 13}  |
            +--------------+-------------+-------+--------+------------+
        
        """
        super(MAYOEstimator, self).table(show_quantum_complexity=show_quantum_complexity,
                                          show_tilde_o_time=show_tilde_o_time,
                                          show_all_parameters=show_all_parameters,
                                          precision=precision, truncate=truncate)
