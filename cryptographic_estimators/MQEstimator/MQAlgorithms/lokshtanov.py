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


from cryptographic_estimators.MQEstimator.series.nmonomial import NMonomialSeries
from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
from cryptographic_estimators.MQEstimator.mq_algorithm import MQAlgorithm
from cryptographic_estimators.base_algorithm import optimal_parameter
from cryptographic_estimators.helper import (
    is_power_of_two,
    gf_order_to_characteristic,
    gf_order_to_degree,
)
from math import log2, inf, ceil, floor


class Lokshtanov(MQAlgorithm):
    def __init__(self, problem: MQProblem, **kwargs):
        """Construct an instance of Lokshtanov et al.'s estimator.

        Lokshtanov et al.'s is a probabilistic algorithm to solve the MQ problem over GF(q) [LPTWY17]_. It describes an
        algorithm to determine the consistency of a given system of polynomial equations.

        Args:
            problem (MQProblem): An MQProblem object including all necessary parameters.
            h (int, optional): The external hybridization parameter. Defaults to 0.
            memory_access (int, optional): Specifies the memory access cost model. Defaults to 0 (constant),
                choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function
                which takes as input the logarithm of the total memory usage.
            complexity_type (int, optional): The complexity type to consider. Defaults to 0 (estimate),
                choices: 0 - estimate, 1 - tilde O complexity.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.lokshtanov import Lokshtanov
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = Lokshtanov(MQProblem(n=10, m=12, q=9))
            >>> E
            Lokshtanov et al. estimator for the MQ problem with 10 variables and 12 polynomials
        """

        q = problem.order_of_the_field()
        if not isinstance(q, int):
            raise TypeError("q must be an integer")

        if q > 1024:
            raise TypeError("q too big to run this algorithm")

        super().__init__(problem, **kwargs)
        self._name = "Lokshtanov et al."

        self.set_parameter_ranges("delta", 0, 1)

    @optimal_parameter
    def delta(self):
        """Return the optimal delta for Lokshtanov et al.'s algorithm.
    
        Returns:
            float: The optimal delta value.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.lokshtanov import Lokshtanov
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = Lokshtanov(MQProblem(n=10, m=12, q=9))
            >>> E.delta()
            0.1
        """
        return self._get_optimal_parameter("delta")

    def _valid_choices(self):
        """Yields valid values for delta.
    
        Each call increments `l`.
    
        Yields:
            float: A valid value for delta.
        """
        n, _, _ = self.get_reduced_parameters()
        ranges = self._parameter_ranges
        l_min = max(1, floor(ranges["delta"]["min"] * n))
        l_max = min(ceil(ranges["delta"]["max"] * n), n - 1)
        l = l_min
        stop = False
        while not stop:
            delta_ = l / n
            yield {"delta": delta_}
            l += 1
            if l > l_max:
                stop = True

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): A dictionary including the parameters.
    
        Tests:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.lokshtanov import Lokshtanov
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = Lokshtanov(MQProblem(n=10, m=12, q=9), bit_complexities=False)
            >>> E.time_complexity(delta=2/10)
            210.99786719362038
        """
        delta = parameters["delta"]
        n, _, q = self.get_reduced_parameters()
        if delta is None:
            return inf
        else:
            if not 0 < delta < 1:
                raise ValueError("delta must be in the range 0 < delta < 1")
            else:
                n_temp = n - 1
                np = floor(delta * n_temp)
                k = 2  # Degree of the polynomials
                time = log2(100 * log2(q) * (q - 1))
                time1 = (n_temp - np) * log2(q)
                resulting_degree = k * (q - 1) * (np + 2)
                if self._is_early_abort_possible(time1):
                    return inf
                serie = NMonomialSeries(
                    n=n_temp - np, q=q, max_prec=resulting_degree + 1
                )
                M = serie.nmonomials_up_to_degree(resulting_degree)
                time2 = log2(M) + np * log2(q) + 6 * q * log2(n_temp)
                a = 0
                if abs(time1 - time2) < 1:
                    a = 1
                time += max(time1, time2) + a
        h = self._h
        return h * log2(q) + time

    def _compute_memory_complexity(self, parameters: dict):
        """Compute the memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): A dictionary containing the parameters.
    
        Tests:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.lokshtanov import Lokshtanov
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = Lokshtanov(MQProblem(n=10, m=12, q=9), bit_complexities=False)
            >>> E.memory_complexity(delta=2/10)
            27.471075081419315
        """
        delta = parameters["delta"]
        n, _, q = self.get_reduced_parameters()

        if delta is None:
            return inf

        else:
            np = floor(n * delta)
            resulting_degree = 2 * (q - 1) * (np + 2)
            serie = NMonomialSeries(n=n - np, q=q, max_prec=resulting_degree + 1)
            M = serie.nmonomials_up_to_degree(resulting_degree)
            memory = M + log2(n) * q ** (n - np)

        return log2(memory)

    def _compute_tilde_o_time_complexity(self, parameters: dict):
        """Return the Ō time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): A dictionary including the parameters.
    
        Tests:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.lokshtanov import Lokshtanov
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = Lokshtanov(MQProblem(n=10, m=12, q=9), complexity_type=1)
            >>> E.time_complexity(delta=2/10)
            6.339850002884624
        """
        delta = parameters["delta"]
        e = 2.718
        n, _, q = self.get_reduced_parameters()
        if log2(gf_order_to_characteristic(q)) < 8 * e:
            time = delta * n * log2(q)
        else:
            d = gf_order_to_degree(q)
            time = n * log2(q) + (-d * n) * log2((log2(q) / (2 * e * d)))

        h = self._h
        return h * log2(q) + time

    def _compute_tilde_o_memory_complexity(self, parameters: dict):
        """Return the Ō time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): A dictionary including the parameters.
    
        Tests:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.lokshtanov import Lokshtanov
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = Lokshtanov(MQProblem(n=10, m=12, q=9), complexity_type=1)
            >>> E.memory_complexity(delta=2/10)
            25.359400011538497
        """
        delta = parameters["delta"]
        n, _, q = self.get_reduced_parameters()
        return (1 - delta) * n * log2(q)

    def _find_optimal_tilde_o_parameters(self):
        """Return the optimal parameters to achieve the optimal Ō time complexity.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.lokshtanov import Lokshtanov
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = Lokshtanov(MQProblem(n=10, m=12, q=9), complexity_type=1)
            >>> E.optimal_parameters()
            {'delta': 0.9975}
        """
        _, _, q = self.get_reduced_parameters()
        e = 2.718
        if q == 2:
            delta = 0.8765
        elif is_power_of_two(q):
            delta = 0.9
        elif log2(gf_order_to_characteristic(q)) < 8 * e:
            delta = 0.9975
        else:
            delta = None
        self._optimal_parameters["delta"] = delta
