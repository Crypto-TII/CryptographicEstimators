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


from ..mayo_algorithm import MAYOAlgorithm
from ..mayo_problem import MAYOProblem
from ...MQEstimator.mq_estimator import MQEstimator
from ...MQEstimator.MQAlgorithms import ExhaustiveSearch, Lokshtanov
from ...base_algorithm import optimal_parameter
from ...base_constants import BASE_FORGERY_ATTACK
from functools import cache
from math import log2, inf


@cache
def _mq(n: int, m: int, q: int, w: float, theta: float):
    """Return the bit cost of MQ(n, m) over GF(q) of the fastest MQEstimator algorithm.

    Cached, as _compute_time_complexity queries the same few systems for every parameter set.
    """
    try:
        # ExhaustiveSearch and Lokshtanov do not support a single variable.
        excluded = [ExhaustiveSearch, Lokshtanov] if n == 1 else []
        E = MQEstimator(n=n, m=m, q=q, w=w, theta=theta, nsolutions=0, excluded_algorithms=excluded)
        return E.fastest_algorithm().time_complexity()
    except Exception:
        # Zero-variable systems are outside MQEstimator capabilities, so
        # we count an exhaustive search instead.
        return n * log2(q) + log2(max(1, m)) + theta * log2(log2(q))


class GeometricAttack(MAYOAlgorithm):
    def __init__(self, problem: MAYOProblem, **kwargs):
        """Construct an instance of the structural forgery attack estimator [GF26]_.

        The positional kappa of [GF26]_ is the whipping parameter k of MAYO. The optimized k is the paper's
        additional guessing parameter: structural Reduced work uses q^(k+h-u) assignments, whereas the
        endpoint is reached q^(h-u) times in expectation. Round 2 structural modes use w = u + r.

        Args:
            problem (MAYOProblem): MAYOProblem object including all necessary parameters
            **kwargs: Additional keyword arguments
                w (float): Linear algebra constant (default: 2.81)

        Examples:
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.geometric import GeometricAttack
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> E = GeometricAttack(MAYOProblem(n=22, m=20, o=4, k=5, q=16))
            >>> E.optimal_parameters()
            {'a': 0, 'B1': 3, 'b0': 3, 'k': 2, 'p': 2, 'ell': 2}
        """
        super().__init__(problem, **kwargs)
        self._name = "GeometricAttack"
        self._attack_type = BASE_FORGERY_ATTACK
        self._theta = float(self.problem.theta if self.problem.theta is not None else 2)

        n, m, _, _, _ = self.problem.get_parameters()
        # Section 3.1 allows a <= kappa and assumes a third independent base vector.
        self.set_parameter_ranges("a", 0, 0 if m <= 2 else min(n - 2, max(0, 2 * (n - m) - 4)))
        for name, lower in (("B1", 1), ("b0", 0), ("k", 0), ("p", 1), ("ell", 0)):
            self.set_parameter_ranges(name, lower, m)

    @optimal_parameter
    def a(self):
        """Return the optimal number a of additional base vectors."""
        return self._get_optimal_parameter("a")

    @optimal_parameter
    def B1(self):
        """Return the optimal total size B1 of the blocks."""
        return self._get_optimal_parameter("B1")

    @optimal_parameter
    def b0(self):
        """Return the optimal size b0 of the initial block."""
        return self._get_optimal_parameter("b0")

    @optimal_parameter
    def k(self):
        """Return the optimal additional guessing parameter k."""
        return self._get_optimal_parameter("k")

    @optimal_parameter
    def p(self):
        """Return the optimal number p of blocks."""
        return self._get_optimal_parameter("p")

    @optimal_parameter
    def ell(self):
        """Return the optimal parameter ell, with 0 <= ell <= b0."""
        return self._get_optimal_parameter("ell")

    def _valid_choices(self):
        """Search all nonnegative k,b0,ell on the quotient K_H/U.

        Use NH=N-u*(m-h), the dimension lower bound for K_H, and P=sum_{i<j} b_i*b_j.
        The accepted boundary conventions are:
            NH >= m,
            b0*(B1+ell+1) <= NH-u+1,
            b0*B1+P <= NH-m+1.
        Here h=m-k-B1-b0 and the Reduced guessing exponent is g=k+h-u.
        """
        n, m, _, kappa, _ = self.problem.get_parameters()
        N = kappa * n
        r = self._fix_ranges_for_already_set_parameters()
        values = lambda name, upper: range(r[name]["min"], min(r[name]["max"], upper) + 1)
        for a in values("a", m):
            u, w = 2 * kappa + a, 2 * kappa + 3 * a + a * (a - 1) // 2
            for B1 in values("B1", min(m - w, (N - m) // u)):
                for b0 in values("b0", min(m - w - B1, (N - m) // u - B1)):
                    for k in values("k", min(m - w - B1 - b0, (N - m) // u - B1 - b0)):
                        NH = N - u * (k + B1 + b0)
                        for p in values("p", B1):
                            P = (B1 * B1 - (B1 % p) * (B1 // p + 1) ** 2 - (p - B1 % p) * (B1 // p) ** 2) // 2
                            for ell in values("ell", b0):
                                if b0 * (B1 + ell + 1) <= NH - u + 1 and b0 * B1 + P <= NH - m + 1:
                                    yield {"a": a, "B1": B1, "b0": b0, "k": k, "p": p, "ell": ell}

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.

        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.geometric import GeometricAttack
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> GeometricAttack(MAYOProblem(n=22, m=20, o=4, k=5, q=16)).time_complexity()
            25.914621552692825
        """
        n, m, _, kappa, q = self.problem.get_parameters()
        a, B1, b0, k, p, ell = (parameters[i] for i in ("a", "B1", "b0", "k", "p", "ell"))
        e, log_q = int(log2(q)), log2(q)

        # Use the chosen Table 2 bounds as the dimension model for (u, r, w).
        u, r = 2 * kappa + a, 2 * a + a * (a - 1) // 2
        w = u + r
        h = m - k - B1 - b0
        # g does not depend on k: increasing k lowers h equally.
        g = k + h - u
        blocks = [B1 // p + 1] * (B1 % p) + [B1 // p] * (p - B1 % p)

        # Centrifugation is paid once: there is no additional inverse factor.
        terms = [log2(b0) + _mq(B1 + ell, B1 + ell, q, self._w, self._theta) if b0 else -inf]
        for i, block in enumerate(blocks):
            suffix = sum(blocks[i + 1 :])
            terms += [log2(block) + _mq(suffix, suffix, q, self._w, self._theta) if suffix else -inf]
            terms += [g * log_q + _mq(block, block, q, self._w, self._theta)]

        # Reduced terminal MQ(b0-ell,b0+k-ell), in structural bit units.
        if b0 - ell > 0 or b0 == 0:
            terminal = _mq(b0 - ell, b0 - ell + k, q, self._w, self._theta) if b0 or k else -inf
        else:
            # Eliminating a nonempty initial block is not free even when no
            # variables remain. Reuse the reference operation count, then convert
            # its field operations to bits consistently with structural GB costs.
            terminal = log2(2 * b0**3 + b0**2 + k * (b0**2 + 2 * b0)) + self._theta * log2(log2(q))
        terms += [g * log_q + terminal]

        # Expected stage costs per Reduced solution, times the q^(h-u) factor.
        zero_rows = h - w
        sigma = min(zero_rows, u)
        columns, square_rows, equations = e * (u - sigma), e * (w - r), e * r
        rho = min(square_rows, columns)
        if equations <= 0:
            finishing = -inf
        elif columns - rho <= 0:
            finishing = log2(equations)
        else:
            finishing = _mq(columns - rho, equations, 2, self._w, self._theta)
        log_p_zero = (sigma - zero_rows) * log_q
        terms += [(h - u) * log_q + self._linear_algebra(zero_rows, u, e)]
        terms += [(h - u) * log_q + log_p_zero + self._linear_algebra(square_rows, columns, 1)]
        terms += [(h - u) * log_q + log_p_zero + rho - square_rows + finishing]

        top = max(terms)
        return top + log2(sum(2.0 ** (t - top) for t in terms)) - self.problem.to_bitcomplexity_time(0)

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.

        [GF26]_ gives no memory complexity. We report the number of field elements needed to store the
        whipped-up public map, namely m quadratic polynomials in kappa * n variables.

        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.geometric import GeometricAttack
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> GeometricAttack(MAYOProblem(n=22, m=20, o=4, k=5, q=16)).memory_complexity()
            18.897703674762127
        """
        n, m, _, kappa, _ = self.problem.get_parameters()
        return log2(m * kappa * n * (kappa * n + 1) // 2)

    def _linear_algebra(self, rows: int, columns: int, extension_degree: int):
        """Rectangular elimination estimate in bit operations.

        The field-operation count is rows*columns*min(rows,columns)^(omega-2). A GF(2^e) operation is
        charged e^theta bit operations, matching the estimator conversion. With zero columns this reduces
        to checking rows constants.
        """
        if rows <= 0:
            return -inf
        columns = max(1, columns)
        pivots = (self._w - 2) * log2(min(rows, columns))
        return log2(rows) + log2(columns) + pivots + self._theta * log2(extension_degree)
