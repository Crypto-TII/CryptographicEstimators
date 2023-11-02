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


from sage.rings.infinity import Infinity
from sage.functions.log import log
from sage.functions.other import floor
from .base import BaseAlgorithm, optimal_parameter
from ..utils import sum_of_binomial_coefficients


class Bjorklund(BaseAlgorithm):
    r"""
    Construct an instance of Bjorklund et al.'s estimator

    Bjorklund et al.'s is a probabilistic algorithm to solve the MQ problem of GF(2) [BKW19]_. It finds a solution of a qudractic
    system by computing the parity of it number of solutions.

    INPUT:

    - ``n`` -- no. of variables
    - ``m`` -- no. of polynomials
    - ``nsolutions`` -- number of solutions (default: 1)

    EXAMPLES::

        sage: from mpkc.algorithms import Bjorklund
        sage: E = Bjorklund(n=10, m=12)
        sage: E
        Björklund et al.'s estimator for the MQ problem
    """
    def __init__(self, n, m, nsolutions=1, h=0):
        super().__init__(n=n, m=m, q=2, h=h)
        self._nsolutions = nsolutions
        self._k = floor(log(nsolutions + 1, 2))
        self._time_complexity = None
        self._memory_complexity = None
        self._λ = None

    def nsolutions(self):
        """
        Return the number of solutions

        EXAMPLES::

            sage: from mpkc.algorithms import Bjorklund
            sage: B = Bjorklund(n=10, m=12, nsolutions=3)
            sage: B.nsolutions()
            3
        """
        return self._nsolutions

    @optimal_parameter
    def λ(self):
        """
        Return the optimal λ

        EXAMPLES::

            sage: from mpkc.algorithms import Bjorklund
            sage: E = Bjorklund(n=10, m=12)
            sage: E.λ()
            3/10
        """
        if self._λ is not None:
            return self._λ

        n, m = self.nvariables_reduced(), self.npolynomials_reduced()
        k = self._k
        min_complexity = Infinity
        optimal_λ = None

        for l in range(3, min(m, n - 1)):
            λ_ = l / n
            complexity = self._time_complexity_(λ_)
            if complexity < min_complexity:
                min_complexity = complexity
                optimal_λ = λ_

        self._λ = optimal_λ
        return self._λ

    def time_complexity(self, **kwargs):
        """
        Return the time complexity of Bjorklund et al.'s algorithm

        INPUT:

        - ``λ`` -- the λ value (default: None)

        If λ is specified, the function returns the time complexity w.r.t. the given parameter

        EXAMPLES::

            sage: from mpkc.algorithms import Bjorklund
            sage: E = Bjorklund(n=10, m=12)
            sage: float(log(E.time_complexity(), 2))
            35.48523010807851
            sage: float(log(E.time_complexity(λ=7/10), 2))
            49.97565549640329

        TESTS::

            sage: E0 = Bjorklund(n=15, m=12)
            sage: E1 = Bjorklund(n=16, m=12)
            sage: E0.time_complexity().numerical_approx() == E1.time_complexity().numerical_approx()
            True
        """
        λ = kwargs.get('λ', None)

        if λ is not None:
            time_complexity = self._time_complexity_(λ)
        else:
            if self._time_complexity is not None:
                time_complexity = self._time_complexity
            else:
                time_complexity = self._time_complexity = self._time_complexity_(self.λ())

        h = self._h
        time_complexity *= 2 ** h
        return time_complexity

    def memory_complexity(self):
        """
        Return the memory complexity of Bjorklund et al.'s algorithm

        EXAMPLES::

            sage: from mpkc.algorithms import Bjorklund
            sage: E = Bjorklund(n=10, m=12)
            sage: float(log(E.memory_complexity(), 2))
            10.89550378006907

        TESTS::

            sage: E0 = Bjorklund(n=15, m=12)
            sage: E1 = Bjorklund(n=16, m=12)
            sage: E0.memory_complexity().numerical_approx() == E1.memory_complexity().numerical_approx()
            True
        """
        if self._memory_complexity is not None:
            return self._memory_complexity

        def S(_n, _m, _λ):
            if _n <= 1:
                return 0
            else:
                s = 48 * _n + 1
                l = floor(_λ * _n)
                return S(l, l + 2, _λ) + 2 ** (_n - l) * log(s, 2) + _m * sum_of_binomial_coefficients(_n, 2)

        n, m = self.nvariables_reduced(), self.npolynomials_reduced()
        λ = self.λ()
        self._memory_complexity = S(n, m, λ)
        return self._memory_complexity

    def tilde_o_time(self):
        """
        Return the Ō time complexity of Bjorklund et al.'s algorithm

        EXAMPLES::

            sage: from mpkc.algorithms import Bjorklund
            sage: E = Bjorklund(n=10, m=12)
            sage: float(log(E.tilde_o_time(), 2))
            8.03225
        """
        n = self.nvariables_reduced()
        h = self._h
        return 2 ** h * 2 ** (0.803225 * n)

    @staticmethod
    def _T(n, m, λ):
        if n <= 1:
            return 1
        else:
            l = floor(λ * n)
            T1 = (n + (l + 2) * m * sum_of_binomial_coefficients(n, 2) + (n - l) * 2 ** (n - l))
            s = 48 * n + 1
            return s * sum_of_binomial_coefficients(n - l, l + 4) * (Bjorklund._T(l, l + 2, λ) + T1)

    def _time_complexity_(self, λ):
        """
        Return the time complexity w.r.t. λ

        INPUT:

        - ``λ`` -- the λ value
        """
        n, m = self.nvariables_reduced(), self.npolynomials_reduced()
        k = self._k

        return 8 * k * log(n, 2) * sum([Bjorklund._T(n - i, m + k + 2, λ) for i in range(1, n)])

    def __repr__(self):
        return f"Björklund et al.'s estimator for the MQ problem"

    # all methods below are implemented to overwrite the parent's docstring while keeping the implementation

    def has_optimal_parameter(self):
        """
        Return `True` if the algorithm has optimal parameter

        EXAMPLES::

            sage: from mpkc.algorithms import Bjorklund
            sage: H = Bjorklund(n=5, m=10)
            sage: H.has_optimal_parameter()
            True
        """
        return super().has_optimal_parameter()

    def is_defined_over_finite_field(self):
        """
        Return `True` if the algorithm is defined over a finite field

        EXAMPLES::

            sage: from mpkc.algorithms import Bjorklund
            sage: H = Bjorklund(n=5, m=10)
            sage: H.is_defined_over_finite_field()
            True
        """
        return super().is_defined_over_finite_field()

    def is_overdefined_system(self):
        """
        Return `True` if the system is overdefined

        EXAMPLES::

            sage: from mpkc.algorithms import Bjorklund
            sage: H = Bjorklund(n=5, m=10)
            sage: H.is_overdefined_system()
            True
            sage: E = Bjorklund(n=10, m=10)
            sage: E.is_overdefined_system()
            False
        """
        return super().is_overdefined_system()

    def is_square_system(self):
        """
        Return `True` if the system is square, there are equal no. of variables and polynomials

        EXAMPLES::

            sage: from mpkc.algorithms import Bjorklund
            sage: H = Bjorklund(n=5, m=10)
            sage: H.is_square_system()
            False
            sage: E = Bjorklund(n=10, m=10)
            sage: E.is_square_system()
            True
        """
        return super().is_square_system()

    def is_underdefined_system(self):
        """
        Return `True` if the system is underdefined

        EXAMPLES::

            sage: from mpkc.algorithms import Bjorklund
            sage: H = Bjorklund(n=5, m=10)
            sage: H.is_underdefined_system()
            False
            sage: E = Bjorklund(n=10, m=5)
            sage: E.is_underdefined_system()
            True
        """
        return super().is_underdefined_system()

    def linear_algebra_constant(self):
        """
        Return the linear algebra constant

        EXAMPLES::

            sage: from mpkc.algorithms import Bjorklund
            sage: H = Bjorklund(n=5, m=10)
            sage: H.linear_algebra_constant()
            <BLANKLINE>
        """

    def npolynomials(self):
        """
        Return the number of polynomials

        EXAMPLES::

            sage: from mpkc.algorithms import Bjorklund
            sage: H = Bjorklund(n=5, m=10)
            sage: H.npolynomials()
            10
        """
        return super().npolynomials()

    def nvariables(self):
        """
        Return the number of variables

        EXAMPLES::

            sage: from mpkc.algorithms import Bjorklund
            sage: H = Bjorklund(n=5, m=10)
            sage: H.nvariables()
            5
        """
        return super().nvariables()

    def nvariables_reduced(self):
        """
        Return the no. of variables after fixing some values

        EXAMPLES::

            sage: from mpkc.algorithms import Bjorklund
            sage: H = Bjorklund(n=5, m=10)
            sage: H.nvariables_reduced()
            5
            sage: E = Bjorklund(n=12, m=10)
            sage: E.nvariables_reduced()
            10
        """
        return super().nvariables_reduced()

    def npolynomials_reduced(self):
        """
        Return the no. of polynomials after applying the Thomae and Wolf strategy

        EXAMPLES::

            sage: from mpkc.algorithms import Bjorklund
            sage: H = Bjorklund(n=5, m=10)
            sage: H.npolynomials_reduced()
            10
            sage: E = Bjorklund(n=12, m=10)
            sage: E.npolynomials_reduced()
            10
        """
        return super().npolynomials_reduced()

    def optimal_parameters(self):
        """
        Return a dictionary of optimal parameters

        EXAMPLES::

            sage: from mpkc.algorithms import Bjorklund
            sage: H = Bjorklund(n=15, m=10)
            sage: H.optimal_parameters()
            {'λ': 3/10}
        """
        return super().optimal_parameters()

    def order_of_the_field(self):
        """
        Return the order of the field

        EXAMPLES::

            sage: from mpkc.algorithms import Bjorklund
            sage: H = Bjorklund(n=15, m=10)
            sage: H.order_of_the_field()
            2
        """
        return super().order_of_the_field()
