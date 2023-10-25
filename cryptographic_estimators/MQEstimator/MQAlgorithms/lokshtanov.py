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


from ...MQEstimator.series.nmonomial import NMonomialSeries
from ...MQEstimator.mq_problem import MQProblem
from ...MQEstimator.mq_algorithm import MQAlgorithm
from ...base_algorithm import optimal_parameter
from math import log2, inf
from sage.functions.other import ceil, floor
from sage.all import Integer
from sage.arith.misc import is_power_of_two
from sage.functions.other import floor
from sage.rings.infinity import Infinity
from sage.rings.finite_rings.finite_field_constructor import GF


class Lokshtanov(MQAlgorithm):
    r"""
    Construct an instance of Lokshtanov et al.'s estimator
    Lokshtanov et al.'s is a probabilistic algorithm to solve the MQ problem over GF(q) [LPTWY17]_. It describes an
    algorithm to determine the consistency of a given system of polynomial equations.

    INPUT:

   - ``problem`` --MQProblem object including all necessary parameters
    - ``h`` -- external hybridization parameter (default: 0)
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
    - ``complexity_type`` -- complexity type to consider (0: estimate, 1: tilde O complexity, default: 0)


    EXAMPLES::

        sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.lokshtanov import Lokshtanov
        sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
        sage: E = Lokshtanov(MQProblem(n=10, m=12, q=9))
        sage: E
        Lokshtanov et al. estimator for the MQ problem with 10 variables and 12 polynomials
    """

    def __init__(self, problem: MQProblem, **kwargs):
        q = problem.order_of_the_field()
        if not isinstance(q, (int, Integer)):
            raise TypeError("q must be an integer")

        if q > 1024:
            raise TypeError("q too big to run this algorithm")

        super().__init__(problem, **kwargs)
        self._name = "Lokshtanov et al."

        self.set_parameter_ranges('delta', 0, 1)

    @optimal_parameter
    def delta(self):
        r"""
        Return the optimal `\delta` for Lokshtanov et al.'s algorithm

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.lokshtanov import Lokshtanov
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = Lokshtanov(MQProblem(n=10, m=12, q=9))
            sage: E.delta()
            1/10
        """
        return self._get_optimal_parameter('delta')

    def _valid_choices(self):
        """
        Yields valid values for `delta`.
        Each call incremetns `l`
        """
        n, _, _ = self.get_reduced_parameters()
        ranges = self._parameter_ranges
        l_min = max(1, floor(ranges['delta']['min'] * n))
        l_max = min(ceil(ranges['delta']['max'] * n), n - 1)
        l = l_min
        stop = False
        while not stop:
            delta_ = l / n
            yield {'delta': delta_}
            l += 1
            if l > l_max:
                stop = True

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.lokshtanov import Lokshtanov
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = Lokshtanov(MQProblem(n=10, m=12, q=9), bit_complexities=False)
            sage: E.time_complexity(delta=2/10)
            214.1677921950627
        """
        delta = parameters['delta']
        n, _, q = self.get_reduced_parameters()
        if delta is None:
            return Infinity
        else:
            if not 0 < delta < 1:
                raise ValueError("delta must be in the range 0 < delta < 1")
            else:
                n_temp = n - 1
                np = floor(delta * n_temp)
                k = 2  # Degree of the polynomials
                time = log2(100 * log2(q) * (q - 1))
                time1 = log2(n_temp) + (n_temp - np) * log2(q)
                resulting_degree = k * (q - 1) * (np + 2)
                if  self._is_early_abort_possible(time1):
                    return inf
                M = NMonomialSeries(n=n_temp - np, q=q, max_prec=resulting_degree +
                                                            1).nmonomials_up_to_degree(resulting_degree)
                time2 = log2(n_temp) +  log2(M) + np * log2(q) + 6 * q * log2(n_temp)
                a = 0
                if abs(time1 - time2) < 1:
                    a = 1
                time += max(time1, time2) + a
        h = self._h
        return h * log2(q) + time

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.lokshtanov import Lokshtanov
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = Lokshtanov(MQProblem(n=10, m=12, q=9), bit_complexities=False)
            sage: E.memory_complexity(delta=2/10)
            27.471075081419315
        """
        delta = parameters['delta']
        n, _, q = self.get_reduced_parameters()

        if delta is None:
            return Infinity

        else:
            np = floor(n * delta)
            resulting_degree = 2 * (q - 1) * (np + 2)
            M = NMonomialSeries(n=n - np, q=q, max_prec=resulting_degree +
                                1).nmonomials_up_to_degree(resulting_degree)
            memory = M + log2(n) * q ** (n - np)

        return log2(memory)

    def _compute_tilde_o_time_complexity(self, parameters: dict):
        """
        Return the Ō time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.lokshtanov import Lokshtanov
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = Lokshtanov(MQProblem(n=10, m=12, q=9), complexity_type=1)
            sage: E.time_complexity(delta=2/10)
            6.339850002884624
        """
        delta = parameters['delta']
        e = 2.718
        n, _, q = self.get_reduced_parameters()
        if log2(GF(q).characteristic()) < 8 * e:
            time = delta * n * log2(q)
        else:
            d = GF(q).degree()
            time = n * log2(q) + (-d * n) * log2((log2(q) / (2 * e * d)))

        h = self._h
        return h * log2(q) + time

    def _compute_tilde_o_memory_complexity(self, parameters: dict):
        r"""
        Return the Ō time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TEST::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.lokshtanov import Lokshtanov
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = Lokshtanov(MQProblem(n=10, m=12, q=9), complexity_type=1)
            sage: E.memory_complexity(delta=2/10)
            25.359400011538497
        """
        delta = parameters['delta']
        n, _, q = self.get_reduced_parameters()
        return (1 - delta) * n * log2(q)

    def _find_optimal_tilde_o_parameters(self):
        """
        Return the optimal parameters to achieve the optimal Ō time complexity.

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.lokshtanov import Lokshtanov
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = Lokshtanov(MQProblem(n=10, m=12, q=9), complexity_type=1)
            sage: E.optimal_parameters()
            {'delta': 0.9975}
        """
        n, _, q = self.get_reduced_parameters()
        e = 2.718
        if q == 2:
            delta = 0.8765
        elif is_power_of_two(q):
            delta = 0.9
        elif log2(GF(q).characteristic()) < 8 * e:
            delta = 0.9975
        else:
            delta = None
        self._optimal_parameters['delta'] = delta
