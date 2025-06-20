# *****************************************************************************
# Multivariate Quadratic (MQ) Estimator
# Copyright (C) 2021-2022 Emanuele Bellini, Rusydi H. Makarim, Javier Verbel
# Cryptography Research Centre, Technology Innovation Institute LLC
#
# This file is part of MQ Estimator
#
# MQ Estimator is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# MQ Estimator is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# MQ Estimator. If not, see <https://www.gnu.org/licenses/>.
# *****************************************************************************


"""
Module to compute the time and memory complexity of the algorithms BooleanSolve and FXL

The BooleanSolve and the FXL are algorithms to solve the MQ problem

[BFS+11] Bardet, M., Faugère, J.-C., Salvy, B., and Spaenlehauer, P.-J. On the complexity of solving quadratic
boolean systems. CoRR,abs/1112.6263, 2011.

[YC04]  Courtois, N., and Klimov, A., and Patarin, J., and Shamir, A. Efficient  algorithms  for  solving overdefined
systems of multivariate polynomial equations, In B. Preneel, editor,Advancesin Cryptology — EUROCRYPT 2000,
pages 392–407, Berlin, Heidelberg, 2000. SpringerBerlin Heidelberg.

For the space complexity of the variant las_vegas

[Nie12] Niederhagen, R. Parallel Cryptanalysis. PhD thesis, Eindhoven University of Technology, 2012.
http://polycephaly.org/thesis/index.shtml.30

"""
from sage.all import Integer
from sage.arith.misc import binomial
from sage.functions.log import log
from sage.rings.infinity import Infinity
from .base import BaseAlgorithm, optimal_parameter
from .. import witness_degree


class BooleanSolveFXL(BaseAlgorithm):
    """
    Construct an instance of BooleanSolve and FXL estimator

    BooleanSolve and FXL are algorithms to solve the MQ problem over GF(2) and GF(q), respectively [BFSS11]_ [CKPS]_.
    They work by guessing the value of $k$ variables and computing the consistency of the resulting subsystem.

    INPUT:

    - ``n`` -- no. of variables
    - ``m`` -- no. of polynomials
    - ``q`` -- order of the finite field
    - ``w`` -- linear algebra constant (2 <= w <= 3) (default: 2)
    - ``h`` -- external hybridization parameter (default: 0)

    EXAMPLES::

        sage: from mpkc.algorithms import BooleanSolveFXL
        sage: E = BooleanSolveFXL(n=10, m=12, q=7)
        sage: E
        BooleanSolve and FXL estimators for the MQ problem
    """
    _variants = ("las_vegas", "deterministic")

    def __init__(self, n, m, q, w=2, h=0):
        if not isinstance(q, (int, Integer)):
            raise TypeError("q must be an integer")
        super().__init__(n=n, m=m, q=q, w=w, h=h)

        if self.is_defined_over_finite_field():
            if not self.npolynomials_reduced() >= self.nvariables_reduced() and not self.npolynomials_reduced() == self.nvariables_reduced():
                raise ValueError("the no. of polynomials must be >= than the no. of variables")
        else:
            if not self.npolynomials_reduced() >= self.nvariables_reduced():
                raise ValueError("the no. of polynomials must be > than the no. of variables")

        self._k = None
        self._variant = None
        self._time_complexity = None
        self._memory_complexity = None
        self._compute_optimal_k_ = self._compute_time_complexity_
        self._compute_optimal_variant_ = self._compute_time_complexity_

    @optimal_parameter
    def k(self):
        """
        Return the optimal `k`

        EXAMPLES::

            sage: from mpkc.algorithms import BooleanSolveFXL
            sage: E = BooleanSolveFXL(n=10, m=12, q=7)
            sage: E.k()
            4
        """
        if self._k is None:
            self._compute_optimal_k_()
        return self._k

    @optimal_parameter
    def variant(self):
        """
        Return the optimal variant

        EXAMPLES::

            sage: from mpkc.algorithms import BooleanSolveFXL
            sage: E = BooleanSolveFXL(n=10, m=12, q=7)
            sage: E.variant()
            'deterministic'
        """
        if self._variant is None:
            self._compute_optimal_variant_()
        return self._variant

    def time_complexity(self, **kwargs):
        """
        Return the time complexity of BooleanSolve and FXL algorithms

        INPUT:

        - ``k`` -- the optimal `k` (default: None)
        - ``variant`` -- the selected variant (default: None)

        If `k` and `variant` are specified, the function returns the time complexity w.r.t the given parameters

        EXAMPLES::

            sage: from mpkc.algorithms import BooleanSolveFXL
            sage: E = BooleanSolveFXL(n=10, m=12, q=7)
            sage: float(log(E.time_complexity(), 2))
            27.599017034509096
            sage: float(log(E.time_complexity(k=2, variant="las_vegas"), 2))
            33.35111811760744
        """

        k = kwargs.get('k', None)
        variant = kwargs.get('variant', None)

        if k is not None and variant is not None:
            time_complexity = self._time_complexity_(k, variant)
        else:
            self._compute_time_complexity_()
            time_complexity = self._time_complexity

        h = self._h
        q = self.order_of_the_field()
        time_complexity *= q ** h
        return time_complexity

    def memory_complexity(self):
        """
        Return the memory complexity of BooleanSolve and FXL algorithms

        EXAMPLES::

            sage: from mpkc.algorithms import BooleanSolveFXL
            sage: E = BooleanSolveFXL(n=10, m=12, q=7)
            sage: E.memory_complexity()
            3136
        """
        if self._memory_complexity is None:
            n, m = self.nvariables_reduced(), self.npolynomials_reduced()
            q = self.order_of_the_field()
            k = self.k()
            wit_deg = witness_degree.quadratic_system(n=n - k, m=m, q=q)
            if self.variant() == "las_vegas":
                a = binomial(n - k + 2, 2)
                T = binomial(n - k + wit_deg - 2, wit_deg)
                N = binomial(n - k + wit_deg, wit_deg)
                self._memory_complexity = m * a + (T * a * log(N, 2) + N * log(m, 2)) / log(q, 2)
            else:
                self._memory_complexity = max(binomial(n - k + wit_deg - 1, wit_deg) ** 2, m * n ** 2)

        return self._memory_complexity

    def tilde_o_time(self):
        """
        Return the Ō time complexity of BooleanSolve and FXL algorithms

        EXAMPLES::

            sage: from mpkc.algorithms import BooleanSolveFXL
            sage: E = BooleanSolveFXL(n=10, m=12, q=7)
            sage: float(log(E.tilde_o_time(), 2))
            24.014054533787938
        """
        n, m = self.nvariables_reduced(), self.npolynomials_reduced()
        q = self.order_of_the_field()
        w = self.linear_algebra_constant()
        k = self.k()
        variant = self.variant()
        wit_deg = witness_degree.quadratic_system(n=n - k, m=m, q=q)

        if n == m and q == 2:
            return 2 ** (0.792 * m)
        elif variant == 'las_vegas':
            complexity = q ** k * binomial(n - k + wit_deg, wit_deg) ** 2
        else:
            complexity = q ** k * binomial(n - k + wit_deg, wit_deg) ** w

        h = self._h
        return q ** h * complexity

    def _compute_time_complexity_(self):
        min_time_complexity = Infinity

        n, m = self.nvariables_reduced(), self.npolynomials_reduced()

        optimal_k = optimal_variant = None

        for variant in BooleanSolveFXL._variants:
            a = 0 if self.is_overdefined_system() else 1
            for k in range(a, n):

                time_complexity = self._time_complexity_(k, variant)

                if time_complexity < min_time_complexity:
                    min_time_complexity = time_complexity
                    optimal_k = k
                    optimal_variant = variant

        self._time_complexity = min_time_complexity
        self._k = optimal_k
        self._variant = optimal_variant

    def _time_complexity_(self, k, variant):
        """
        Return the time complexity for the given parameter

        INPUT:

        - ``k`` -- the value `k`
        - ``variant`` -- the variant of the algorithm
        """
        n, m = self.nvariables_reduced(), self.npolynomials_reduced()
        q = self.order_of_the_field()
        w = self.linear_algebra_constant()

        wit_deg = witness_degree.quadratic_system(n=n - k, m=m, q=q)

        if variant == "las_vegas":
            time_complexity = 3 * binomial(n - k + 2, 2) * q ** k * binomial(n - k + wit_deg, wit_deg) ** 2
        elif variant == "deterministic":
            time_complexity = q ** k * m * binomial(n - k + wit_deg, wit_deg) ** w
        else:
            raise ValueError("variant must either be las_vegas or deterministic")

        return time_complexity

    def __repr__(self):
        return f"BooleanSolve and FXL estimators for the MQ problem"

    # all methods below are implemented to overwrite the parent's docstring while keeping the implementation

    def has_optimal_parameter(self):
        """
        Return `True` if the algorithm has optimal parameter

        EXAMPLES::

            sage: from mpkc.algorithms import BooleanSolveFXL
            sage: H = BooleanSolveFXL(q=256, n=5, m=10)
            sage: H.has_optimal_parameter()
            True
        """
        return super().has_optimal_parameter()

    def is_defined_over_finite_field(self):
        """
        Return `True` if the algorithm is defined over a finite field

        EXAMPLES::

            sage: from mpkc.algorithms import BooleanSolveFXL
            sage: H = BooleanSolveFXL(q=256, n=5, m=10)
            sage: H.is_defined_over_finite_field()
            True
        """
        return super().is_defined_over_finite_field()

    def is_overdefined_system(self):
        """
        Return `True` if the system is overdefined

        EXAMPLES::

            sage: from mpkc.algorithms import BooleanSolveFXL
            sage: H = BooleanSolveFXL(q=256, n=5, m=10)
            sage: H.is_overdefined_system()
            True
            sage: E = BooleanSolveFXL(q=256, n=10, m=10)
            sage: E.is_overdefined_system()
            False
        """
        return super().is_overdefined_system()

    def is_square_system(self):
        """
        Return `True` if the system is square, there are equal no. of variables and polynomials

        EXAMPLES::

            sage: from mpkc.algorithms import BooleanSolveFXL
            sage: H = BooleanSolveFXL(q=256, n=5, m=10)
            sage: H.is_square_system()
            False
            sage: E = BooleanSolveFXL(q=256, n=10, m=10)
            sage: E.is_square_system()
            True
        """
        return super().is_square_system()

    def is_underdefined_system(self):
        """
        Return `True` if the system is underdefined

        EXAMPLES::

            sage: from mpkc.algorithms import BooleanSolveFXL
            sage: H = BooleanSolveFXL(q=256, n=5, m=10)
            sage: H.is_underdefined_system()
            False
        """
        return super().is_underdefined_system()

    def linear_algebra_constant(self):
        """
        Return the linear algebra constant

        EXAMPLES::

            sage: from mpkc.algorithms import BooleanSolveFXL
            sage: H = BooleanSolveFXL(q=256, n=5, m=10, w=2)
            sage: H.linear_algebra_constant()
            2
        """
        return super().linear_algebra_constant()

    def npolynomials(self):
        """
        Return the number of polynomials

        EXAMPLES::

            sage: from mpkc.algorithms import BooleanSolveFXL
            sage: H = BooleanSolveFXL(q=256, n=5, m=10)
            sage: H.npolynomials()
            10
        """
        return super().npolynomials()

    def nvariables(self):
        """
        Return the number of variables

        EXAMPLES::

            sage: from mpkc.algorithms import BooleanSolveFXL
            sage: H = BooleanSolveFXL(q=256, n=10, m=10)
            sage: H.nvariables()
            10
        """
        return super().nvariables()

    def nvariables_reduced(self):
        """
        Return the no. of variables after fixing some values

        EXAMPLES::

            sage: from mpkc.algorithms import BooleanSolveFXL
            sage: H = BooleanSolveFXL(q=256, n=10, m=10)
            sage: H.nvariables_reduced()
            10
        """
        return super().nvariables_reduced()

    def npolynomials_reduced(self):
        """
        Return the no. of polynomials after applying the Thomae and Wolf strategy

        EXAMPLES::

            sage: from mpkc.algorithms import BooleanSolveFXL
            sage: H = BooleanSolveFXL(q=256, n=5, m=10)
            sage: H.npolynomials_reduced()
            10
        """
        return super().npolynomials_reduced()

    def optimal_parameters(self):
        """
        Return a dictionary of optimal parameters

        EXAMPLES::

            sage: from mpkc.algorithms import BooleanSolveFXL
            sage: H = BooleanSolveFXL(q=256, n=10, m=10)
            sage: H.optimal_parameters()
            {'k': 2, 'variant': 'deterministic'}
        """
        return super().optimal_parameters()

    def order_of_the_field(self):
        """
        Return the order of the field

        EXAMPLES::

            sage: from mpkc.algorithms import BooleanSolveFXL
            sage: H = BooleanSolveFXL(q=256, n=10, m=10)
            sage: H.order_of_the_field()
            256
        """
        return super().order_of_the_field()