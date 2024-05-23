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


from cryptographic_estimators.base_algorithm import optimal_parameter
from cryptographic_estimators.MQEstimator.mq_algorithm import MQAlgorithm
from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
from cryptographic_estimators.MQEstimator import witness_degree
from cryptographic_estimators.MQEstimator.mq_constants import (
    MQ_VARIANT,
    MQ_LAS_VEGAS,
    MQ_DETERMINISTIC,
)
from math import log2, comb as binomial

# TODO: Remove at final step
from sage.all import Integer


class BooleanSolveFXL(MQAlgorithm):
    """
    Construct an instance of BooleanSolve and FXL estimator

    BooleanSolve and FXL are algorithms to solve the MQ problem over GF(2) and GF(q), respectively [BFSS11]_ [CKPS]_.
    They work by guessing the value of $k$ variables and computing the consistency of the resulting subsystem.

    INPUT:

    - ``problem`` -- MQProblem object including all necessary parameters
    - ``w`` -- linear algebra constant (2 <= w <= 3) (default: 2.81)
    - ``h`` -- external hybridization parameter (default: 0)
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
    - ``complexity_type`` -- complexity type to consider (0: estimate, 1: tilde O complexity, default: 0)

    NOTE:
        - For the memory complexity of `las_vegas` variant, which is XL with the block Wiedemann algorithm, this module
        follows the analysis in [BBC+22]_ (Section 8). There it is stated that any row of the Macaulay matrix can be
        build on the fly. Hence the memory demand of this algorithm is dominated by the memory needed to store two
        vectors of length `N` over `GF(q)`, where N is the number of columns of the Macaulay Matrix.

    EXAMPLES::

        sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.booleansolve_fxl import BooleanSolveFXL
        sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
        sage: E = BooleanSolveFXL(MQProblem(n=10, m=12, q=7))
        sage: E
        BooleanSolveFXL estimator for the MQ problem with 10 variables and 12 polynomials
    """

    _variants = (MQ_LAS_VEGAS, MQ_DETERMINISTIC)

    def __init__(self, problem: MQProblem, **kwargs):
        q = problem.order_of_the_field()
        if not isinstance(q, (int, Integer)):
            raise TypeError("q must be an integer")
        super(BooleanSolveFXL, self).__init__(problem, **kwargs)
        n, m, _ = self.get_reduced_parameters()
        self._name = "BooleanSolveFXL"
        if self.problem.is_defined_over_finite_field():
            if m < n and m != n:
                raise ValueError(
                    "the no. of polynomials must be >= than the no. of variables"
                )
        else:
            if m < n:
                raise ValueError(
                    "the no. of polynomials must be > than the no. of variables"
                )

        a = 0 if self.problem.is_overdefined_system() else 1
        self.set_parameter_ranges("k", a, max(n - 1, 1))

    @optimal_parameter
    def k(self):
        """
        Return the optimal `k`

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.booleansolve_fxl import BooleanSolveFXL
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = BooleanSolveFXL(MQProblem(n=10, m=12, q=7))
            sage: E.k()
            4
        """
        return self._get_optimal_parameter("k")

    @optimal_parameter
    def variant(self):
        """
        Return the optimal variant

        EXAMPLES::

            sage: from  cryptographic_estimators.MQEstimator.MQAlgorithms.booleansolve_fxl import BooleanSolveFXL
            sage: from  cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = BooleanSolveFXL(MQProblem(n=10, m=12, q=7))
            sage: E.variant()
            'las_vegas'
        """
        return self._get_optimal_parameter(MQ_VARIANT)

    def _valid_choices(self):
        """
        Generator which yields on each call a new set of valid parameters for the optimization routine based.
        """
        new_ranges = self._fix_ranges_for_already_set_parameters()
        _ = new_ranges.pop(MQ_VARIANT)

        variant = MQ_LAS_VEGAS
        indices = {i: new_ranges[i]["min"] for i in new_ranges}
        stop = False
        while not stop:
            aux = indices.copy()
            aux.update({MQ_VARIANT: variant})
            yield aux
            indices["k"] += 1
            if indices["k"] > new_ranges["k"]["max"] and variant != MQ_DETERMINISTIC:
                indices["k"] = new_ranges["k"]["min"]
                variant = MQ_DETERMINISTIC
            elif indices["k"] > new_ranges["k"]["max"] and variant == MQ_DETERMINISTIC:
                stop = True

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.booleansolve_fxl import BooleanSolveFXL
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = BooleanSolveFXL(MQProblem(n=10, m=12, q=7), bit_complexities=False)
            sage: E.time_complexity(k=2, variant = 'las_vegas')
            33.35111811760744

            sage: E = BooleanSolveFXL(MQProblem(n=594, m=64, q=16, theta=None), complexity_type=0)
            sage: E.optimal_parameters()
            {'k': 13, 'variant': 'las_vegas'}

            sage: E.time_complexity()
            150.2690857321659

            sage: E = BooleanSolveFXL(MQProblem(n=312, m=64, q=16, theta=None), complexity_type=0)
            sage: E.optimal_parameters()
            {'k': 11, 'variant': 'las_vegas'}

            sage: E.time_complexity()
            160.33500724355238

        """
        k = parameters["k"]
        variant = parameters[MQ_VARIANT]
        n, m, q = self.get_reduced_parameters()
        w = self.linear_algebra_constant()

        wit_deg = witness_degree.quadratic_system(n=n - k, m=m, q=q)

        if variant == MQ_LAS_VEGAS:
            time_complexity = (
                3
                * binomial(n - k + 2, 2)
                * q**k
                * binomial(n - k + wit_deg, wit_deg) ** 2
            )
        elif variant == MQ_DETERMINISTIC:
            time_complexity = q**k * m * binomial(n - k + wit_deg, wit_deg) ** w
        else:
            raise ValueError("variant must either be las_vegas or deterministic")

        h = self._h
        return log2(time_complexity) + h * log2(q)

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from  cryptographic_estimators.MQEstimator.MQAlgorithms.booleansolve_fxl import BooleanSolveFXL
            sage: from  cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = BooleanSolveFXL(MQProblem(n=10, m=12, q=7), bit_complexities=False)
            sage: E.memory_complexity(k=2, variant='las_vegas')
            11.329796338220701

            sage: E.memory_complexity()
            10.228818690495881

            sage: E = BooleanSolveFXL(MQProblem(n=594, m=64, q=16), complexity_type=0, theta=None)
            sage: E.memory_complexity()
            43.78145675751773

            sage: E = BooleanSolveFXL(MQProblem(n=312, m=64, q=16), complexity_type=0, theta=None)
            sage: E.memory_complexity()
            52.603627340638155

        """
        k = parameters["k"]
        variant = parameters[MQ_VARIANT]
        n, m, q = self.get_reduced_parameters()

        wit_deg = witness_degree.quadratic_system(n=n - k, m=m, q=q)
        if variant == MQ_LAS_VEGAS:
            N = binomial(n - k + wit_deg, wit_deg)
            memory_complexity = max(2 * N, m * n**2)
        elif variant == MQ_DETERMINISTIC:
            memory_complexity = max(
                binomial(n - k + wit_deg - 1, wit_deg) ** 2, m * n**2
            )
        else:
            raise ValueError("variant must either be las_vegas or deterministic")

        return log2(memory_complexity)

    def _compute_tilde_o_time_complexity(self, parameters: dict):
        """
        Return the Ō time complexity of BooleanSolve and FXL algorithms

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from  cryptographic_estimators.MQEstimator.MQAlgorithms.booleansolve_fxl import BooleanSolveFXL
            sage: from  cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = BooleanSolveFXL(MQProblem(n=10, m=12, q=7), complexity_type=1)
            sage: E.time_complexity(k=2, variant='las_vegas')
            26.274302520556613

            sage: E.time_complexity()
            24.014054533787938

        """
        n, m, q = self.get_reduced_parameters()
        w = self.linear_algebra_constant()
        k = parameters["k"]
        variant = parameters[MQ_VARIANT]
        wit_deg = witness_degree.quadratic_system(n=n - k, m=m, q=q)

        if n == m and q == 2:
            return 0.792 * m
        elif variant == MQ_LAS_VEGAS:
            complexity = log2(q**k * binomial(n - k + wit_deg, wit_deg) ** 2)
        else:
            complexity = log2(q**k * binomial(n - k + wit_deg, wit_deg) ** w)

        complexity += self._h * log2(q)
        return complexity

    def _compute_tilde_o_memory_complexity(self, parameters: dict):
        """
        Return the Ō time complexity of BooleanSolve and FXL algorithms

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from  cryptographic_estimators.MQEstimator.MQAlgorithms.booleansolve_fxl import BooleanSolveFXL
            sage: from  cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = BooleanSolveFXL(MQProblem(n=10, m=12, q=7), complexity_type=1)
            sage: E.memory_complexity(k=2, variant='las_vegas')
            10.329796338220701

        """
        n, m, q = self.get_reduced_parameters()
        k = parameters["k"]
        variant = parameters[MQ_VARIANT]
        wit_deg = witness_degree.quadratic_system(n=n - k, m=m, q=q)
        memory = log2(binomial(n - k + wit_deg, wit_deg))
        if variant == MQ_DETERMINISTIC:
            memory *= 2
        return memory

    def _find_optimal_tilde_o_parameters(self):
        """
        Finds the optimal parameters.

        TESTS::

            sage: from  cryptographic_estimators.MQEstimator.MQAlgorithms.booleansolve_fxl import BooleanSolveFXL
            sage: from  cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = BooleanSolveFXL(MQProblem(n=10, m=12, q=7), complexity_type=1)
            sage: E.optimal_parameters()
            {'k': 4, 'variant': 'las_vegas'}
        """
        self._find_optimal_parameters()
