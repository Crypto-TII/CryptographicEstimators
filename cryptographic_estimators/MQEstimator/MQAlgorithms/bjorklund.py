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


from ...MQEstimator.mq_algorithm import MQAlgorithm
from ...MQEstimator.mq_problem import MQProblem
from ...MQEstimator.mq_helper import sum_of_binomial_coefficients
from ...base_algorithm import optimal_parameter
from math import log2, floor, ceil


class Bjorklund(MQAlgorithm):
    def __init__(self, problem: MQProblem, **kwargs):
        """Construct an instance of Bjorklund et al.'s estimator.

        Bjorklund et al.'s is a probabilistic algorithm to solve the MQ problem over GF(2) [BKW19]_. It finds a solution of a quadratic
        system by computing the parity of its number of solutions.

        Args:
            problem (MQProblem): MQProblem object including all necessary parameters.
            h (int, optional): External hybridization parameter (default: 0).
            memory_access (int, optional): Specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage).
            complexity_type (int, optional): Complexity type to consider (0: estimate, 1: tilde O complexity, default: 0).

        Examples:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.bjorklund import Bjorklund
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = Bjorklund(MQProblem(n=10, m=12, q=2))
            >>> E
            Björklund et al. estimator for the MQ problem with 10 variables and 12 polynomials
        """
        if problem.order_of_the_field() != 2:
            raise TypeError("q must be equal to 2")
        super().__init__(problem, **kwargs)
        self._name = "Björklund et al."
        n, m, _ = self.get_reduced_parameters()
        self._k = floor(log2(2**self.problem.nsolutions + 1))

        if 3 / n <= 0.196774680497:
            self.set_parameter_ranges("lambda_", 3 / n, 0.196774680497)
        else:  # case if n<=15
            self.set_parameter_ranges("lambda_", 3 / n, min(m, n - 1) / n)

        self._time_complexity_is_convex = True

    @optimal_parameter
    def lambda_(self):
        """Return the optimal lambda\_.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.bjorklund import Bjorklund
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = Bjorklund(MQProblem(n=10, m=12, q=2))
            >>> E.lambda_()
            0.3
        """

        return self._get_optimal_parameter("lambda_")

    def _valid_choices(self):
        n, _, _ = self.get_reduced_parameters()
        ranges = self._parameter_ranges
        l_min = max(3, ceil(ranges["lambda_"]["min"] * n))
        l_max = min(ceil(ranges["lambda_"]["max"] * n), n)
        l = l_max
        stop = False
        while not stop:
            temp_lambda = l / n
            yield {"lambda_": temp_lambda}
            l -= 1
            if l < l_min:
                stop = True

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.

        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.bjorklund import Bjorklund
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = Bjorklund(MQProblem(n=10, m=12, q=2), bit_complexities=False)
            >>> E.time_complexity(lambda_=7/10)
            49.55664699444167
        """
        lambda_ = parameters["lambda_"]
        n, m, _ = self.get_reduced_parameters()
        k = self._k
        h = self._h
        time = (
            8
            * k
            * log2(n)
            * sum(
                [
                    Bjorklund._internal_time_complexity_(n - i, m + k + 2, lambda_)
                    for i in range(1, n)
                ]
            )
        )
        return h + log2(time)

    def _compute_memory_complexity(self, parameters: dict):
        """Compute the memory complexity of the algorithm for a given set of parameters.

        Args:
            parameters (dict): A dictionary containing the relevant parameters.

        Tests:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.bjorklund import Bjorklund
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = Bjorklund(MQProblem(n=10, m=12, q=2), bit_complexities=False)
            >>> E.memory_complexity(lambda_=7/10)
            10.225233514599497
        """

        # TODO:Find a better way to handle high precision calculations. See https://github.com/Crypto-TII/CryptographicEstimators/pull/143
        def _custom_floor(number, epsilon):
            return floor(number + epsilon)

        lambda_ = parameters["lambda_"]

        def _internal_memory_complexity_(_n, _m, _lambda):
            if _n <= 1:
                return 0
            else:
                s = 48 * _n + 1
                l = _custom_floor(_lambda * _n, 1e-10)
                return (
                    _internal_memory_complexity_(l, l + 2, _lambda)
                    + 2 ** (_n - l) * log2(s)
                    + _m * sum_of_binomial_coefficients(_n, 2)
                )

        n, m, _ = self.get_reduced_parameters()
        return log2(_internal_memory_complexity_(n, m, lambda_))

    def _compute_tilde_o_time_complexity(self, parameters: dict):
        """Return the Ō time complexity of Bjorklund et al.'s algorithm.

        Tests:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.bjorklund import Bjorklund
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = Bjorklund(MQProblem(n=10, m=12, q=2), complexity_type=1)
            >>> E.time_complexity(lambda_=7/10)
            8.03225
        """
        n = self.nvariables_reduced()
        h = self._h
        return h + 0.803225 * n

    def _compute_tilde_o_memory_complexity(self, parameters: dict):
        """Return the Ō time complexity of Bjorklund et al.'s algorithm.

        Tests:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.bjorklund import Bjorklund
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = Bjorklund(MQProblem(n=10, m=12, q=2), complexity_type=1)
            >>> E.memory_complexity(lambda_=7/10)
            3.0000000000000004
        """
        n = self.nvariables_reduced()
        lambda_ = parameters["lambda_"]
        return (1 - lambda_) * n

    def _find_optimal_tilde_o_parameters(self):
        """Return the Ō time complexity of Bjorklund et al.'s algorithm.

        Tests:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.bjorklund import Bjorklund
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = Bjorklund(MQProblem(n=10, m=12, q=2), complexity_type=1)
            >>> E.optimal_parameters()
            {'lambda_': 0.19677}
        """
        self._optimal_parameters["lambda_"] = 0.19677

    @staticmethod
    def _internal_time_complexity_(n: int, m: int, lambda_: float):
        """Helper function. Computes the runtime of the algorithm for given n, m and lambda.

        ALgorithm taken from: Stefano Barbero et al. Practical complexities of probabilistic algorithms for solving
        Boolean polynomial systems. Cryptology ePrint Archive, Paper 2021/913. https://
        eprint . iacr . org / 2021 / 913. 2021. doi: 10 . 1016 / j . dam . 2021 . 11 . 014. url:
        https://eprint.iacr.org/2021/913.
        """
        # uses brute force
        if n <= 1:
            return 1
        T = 0  # Time complexity
        l = floor(lambda_ * n)  # n1, l from Björklund.
        s = 48 * n + 1  # number of iterations
        sumbin_n_2 = sum_of_binomial_coefficients(n, 2)
        sumbin_B = sum_of_binomial_coefficients(n - l, l + 4)
        T += 2 ** (n - l)  # Line 5, initialize array of size 2^{n-l}
        # Lines 6-12: Enters for loop, so each summand is multiplied by s
        T += (
            s * (l + 2) * m * sumbin_n_2
        )  # Line 7, generate alphas, multiply and add coefficients
        # Line 8: No need to fill with zeros V at this point
        # Line 9-10: enters a for loop, so each term inside is multiplied by sumbin_B
        # Line 10:
        T += s * sumbin_B * sumbin_n_2 * (l + 2)  # Partially evaluate R_i's
        T += (
            s * sumbin_B * Bjorklund._internal_time_complexity_(l, l + 2, lambda_)
        )  # Recursive call
        # Line 11: Interpolation: this function makes two calls to the Z-transform
        T += (
            s * (n - l) * sumbin_B
        )  # The first Z-transform takes (n-l) * sumbin_B * O(1)
        T += s * (2 ** (n - l) - sumbin_B)  # Fill with zeros the rest of the table
        T += s * (n - l) * 2 ** (n - l)  # The second Z-transform takes over all space
        T += s * 2 ** (n - l)  # Line 12: update the score table of size 2 ** (n-l)
        T += 2 ** (
            n - l
        )  # line 14-17 does a for of size 2 ** (n-l), inside the for takes O(1)
        return T

