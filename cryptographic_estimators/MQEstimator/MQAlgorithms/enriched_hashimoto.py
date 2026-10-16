# ****************************************************************************
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
# ****************************************************************************


from cryptographic_estimators.base_algorithm import optimal_parameter
from ...MQEstimator.mq_algorithm import MQAlgorithm
from ...MQEstimator.mq_problem import MQProblem
from ...MQEstimator.mq_estimator import MQEstimator
from functools import cache
from math import log2, inf


@cache
def _mq(n: int, m: int, q: int, w: float, theta: float):
    """Return the bit cost of the fastest MQEstimator algorithm for MQ(n, m) over GF(q); cached, as it is slow."""
    try:
        return MQEstimator(n=n, m=m, q=q, w=w, theta=theta).fastest_algorithm().time_complexity()
    except Exception:
        return inf


class EnrichedHashimoto(MQAlgorithm):
    def __init__(self, problem: MQProblem, **kwargs):
        """Construct an instance of Enriched Hashimoto estimator.

        Enriched Hashimoto solves the underdetermined MQ problem through pseudo-oil subspaces [POS26]_: k
        variables are guessed, p blocks of almost equal size b_1 <= ... <= b_p summing to B are solved as
        square systems, and the remaining m - B - l equations as an overdetermined system.

        Args:
            problem (MQProblem): MQProblem object including all necessary parameters.
            w (float): Linear algebra constant (2 <= w <= 3). Default is 2.81
            h (Optional[float]): External hybridization parameter (default: 0).
            memory_access (int): Specifies the memory access cost model.
                0 - constant (default)
                1 - logarithmic
                2 - square-root
                3 - cube-root
                Alternatively, deploy a custom function which takes as input the logarithm of the total memory usage and returns the logarithm of the memory access cost.
            complexity_type (int): Complexity type to consider.
                0 - estimate (default)
                1 - tilde O complexity

        Examples:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.enriched_hashimoto import EnrichedHashimoto
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = EnrichedHashimoto(MQProblem(q=16, n=924, m=67))
            >>> E
            EnrichedHashimoto estimator for the MQ problem with 924 variables and 67 polynomials

            >>> E = EnrichedHashimoto(MQProblem(q=16, n=45, m=10))
            >>> E.optimal_parameters()
            {'k': 0, 'l': 0, 'B': 10, 'p': 3}
        """
        n, m, q = problem.get_problem_parameters()

        if not isinstance(q, int):
            raise TypeError("q must be an integer")

        if not problem.is_underdefined_system():
            raise ValueError("The MQ problem should be underdefined, i.e., m must be <= n")

        super().__init__(problem, **kwargs)
        self._name = "EnrichedHashimoto"

        self.set_parameter_ranges("k", 0, m)
        self.set_parameter_ranges("l", 0, m)
        self.set_parameter_ranges("B", 0, m)
        self.set_parameter_ranges("p", 1, m)

    @optimal_parameter
    def k(self):
        """Return the optimal number k of guessed variables."""
        return self._get_optimal_parameter("k")

    @optimal_parameter
    def l(self):
        """Return the optimal value of l."""
        return self._get_optimal_parameter("l")

    @optimal_parameter
    def B(self):
        """Return the optimal sum B of the block sizes."""
        return self._get_optimal_parameter("B")

    @optimal_parameter
    def p(self):
        """Return the optimal number p of blocks."""
        return self._get_optimal_parameter("p")

    def _valid_choices(self):
        """Yield all k, l, B and p with k + l + B <= m and p <= max(B, 1)."""
        _, m, _ = self.problem.get_problem_parameters()
        r = self._fix_ranges_for_already_set_parameters()
        values = lambda name, upper: range(r[name]["min"], min(r[name]["max"], upper) + 1)
        for k in values("k", m):
            for l in values("l", m - k):
                for B in values("B", m - k - l):
                    for p in values("p", max(B, 1)):
                        yield {"k": k, "l": l, "B": B, "p": p}

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.

        Args:
            parameters (dict): A dictionary including the parameters.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.enriched_hashimoto import EnrichedHashimoto
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = EnrichedHashimoto(MQProblem(q=16, n=45, m=10))
            >>> E.time_complexity()
            18.508599491009466
        """
        n, m, q = self.problem.get_problem_parameters()
        k, l, B, p = parameters["k"], parameters["l"], parameters["B"], parameters["p"]
        offset = self.problem.to_bitcomplexity_time(0)
        bs = [B // p] * (p - B % p) + [B // p + 1] * (B % p)
        Bs = [sum(bs[:i]) for i in range(p)]

        if n - (m - B - k) < (m - B - k) * (B + l):
            # too aggressive for last vector of O0
            return inf
        if n - m < sum(bs[j] * (m - Bs[j] - bs[j] - k) for j in range(p)):
            # too aggressive for last vector of Otilde
            return inf
        if self._is_early_abort_possible(k * log2(q) - offset):
            return inf

        def square(size):
            return 1 if size <= 2 else _mq(size, size, q, self._w, self.problem.theta)

        # field multiplications and additions for u^tAu, the matrix vector product and the inner product
        polys = sum(
            (Bs[i] + k) ** 2 + 2 * (Bs[i] + k) - 1 + (m - Bs[i] - k) * (2 * (Bs[i] + k) - 1) + 2 * m - 1
            for i in range(p)
        )
        centrifugation = (m - B - k) * 2 ** square(B + l)
        centrifugation += sum((m - Bs[i] - k) * 2 ** square(Bs[i]) for i in range(p - 1))
        squares = sum(2 ** square(b) for b in bs)
        if self._is_early_abort_possible(log2(centrifugation + q**k * (squares + polys)) - offset):
            return inf

        over = 1
        if m - B - k - l > 2 and m - B - l > 2:
            over = _mq(m - B - k - l, m - B - l, q, self._w, self.problem.theta)
        # Centrifugation, then Guess times (Square + Overdetermined + Polys)
        return log2(centrifugation + q**k * (2**over + squares + polys)) - offset

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.

        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.enriched_hashimoto import EnrichedHashimoto
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = EnrichedHashimoto(MQProblem(q=16, n=45, m=10))
            >>> E.memory_complexity()
            16.30563428754671
        """
        n, m, _ = self.problem.get_problem_parameters()
        return log2(m * n**2)
