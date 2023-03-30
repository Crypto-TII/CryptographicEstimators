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


from sage.all import Integer
from sage.functions.other import sqrt, floor
from sage.misc.functional import numerical_approx
from .base import BaseAlgorithm
from sage.functions.other import binomial


class CGMTA(BaseAlgorithm):
    r"""
    Construct an instance of CGMT-A estimator

    CGMT-A is an algorithm to solve the MQ problem over any finite field. It works when there is an integer $k$ such
    that $m - 2k < 2k^2 \leq n - 2k$ [CGMT02]_.

    NOTE::

        In this module the compleixties are computed
        for k=  min(m / 2, floor(sqrt(n / 2 - sqrt(n / 2)))).


    INPUT:

    - ``n`` -- no. of variables
    - ``m`` -- no. of polynomials
    - ``q`` -- order of the finite field

    EXAMPLES::

        sage: from mpkc.algorithms import CGMTA
        sage: E = CGMTA(n=41, m=10, q=3)
        sage: E
        CGMT-A estimator for the MQ problem

    TESTS::

        sage: E.nvariables() == E.nvariables_reduced()
        True
    """
    def __init__(self, n, m, q):
        if not isinstance(q, (int, Integer)):
            raise TypeError("q must be an integer")

        if not m <= n:
            raise ValueError("m must be <= n")

        super().__init__(n=n, m=m, q=q)
        self._k = min(m / 2, floor(sqrt(n / 2 - sqrt(n / 2))))

        if not 2 * self._k ** 2 <= n - 2 * self._k or not m - 2 * self._k < 2 * self._k ** 2:
            raise ValueError(f'The condition m - 2k < 2k^2 <= n - 2k must be satisfied')

        self._n_reduced = n
        self._m_reduced = m

    def time_complexity(self):
        """
        Return the time complexity of CGMT-A algorithm

        EXAMPLES::

            sage: from mpkc.algorithms import CGMTA
            sage: E = CGMTA(n=41, m=10, q=3)
            sage: float(log(E.time_complexity(),2))
            23.137080884841783
        """
        n = self.nvariables()
        m = self.npolynomials()
        q = self.order_of_the_field()
        k = self._k
        return numerical_approx(2 * k * binomial(n - k, 2) * q ** (m - k))

    def memory_complexity(self):
        """
        Return the memory complexity of CGMT-A algorithm

        EXAMPLES::

            sage: from mpkc.algorithms import CGMTA
            sage: E = CGMTA(n=41, m=10, q=3)
            sage: E.memory_complexity()
            162.000000000000
        """
        q = self.order_of_the_field()
        k = self._k
        return numerical_approx(2 * k * q ** k)

    def tilde_o_time(self):
        """
        Return the Ō time complexity of of CGMT-A algorithm

        EXAMPLES::

            sage: from mpkc.algorithms import CGMTA
            sage: E = CGMTA(n=41, m=10, q=3)
            sage: E.tilde_o_time()
            2187.00000000000
        """
        m = self.npolynomials()
        q = self.order_of_the_field()
        k = self._k
        return numerical_approx(q ** (m - k))

    def __repr__(self):
        return f"CGMT-A estimator for the MQ problem"

    # all methods below are implemented to overwrite the parent's docstring while keeping the implementation

    def has_optimal_parameter(self):
        """
        Return `True` if the algorithm has optimal parameter

        EXAMPLES::

            sage: from mpkc.algorithms import CGMTA
            sage: H = CGMTA(n=41, m=10, q=3)
            sage: H.has_optimal_parameter()
            False
        """
        return super().has_optimal_parameter()

    def is_defined_over_finite_field(self):
        """
        Return `True` if the algorithm is defined over a finite field

        EXAMPLES::

            sage: from mpkc.algorithms import CGMTA
            sage: H = CGMTA(n=41, m=10, q=3)
            sage: H.is_defined_over_finite_field()
            True
        """
        return super().is_defined_over_finite_field()

    def is_overdefined_system(self):
        """
        Return `True` if the system is overdefined

        EXAMPLES::

            sage: from mpkc.algorithms import CGMTA
            sage: H = CGMTA(n=41, m=10, q=3)
            sage: H.is_overdefined_system()
            False
        """
        return super().is_overdefined_system()

    def is_square_system(self):
        """
        Return `True` if the system is square, there are equal no. of variables and polynomials

        EXAMPLES::

            sage: from mpkc.algorithms import CGMTA
            sage: H = CGMTA(n=41, m=10, q=3)
            sage: H.is_square_system()
            False
        """
        return super().is_square_system()

    def is_underdefined_system(self):
        """
        Return `True` if the system is underdefined

        EXAMPLES::

            sage: from mpkc.algorithms import CGMTA
            sage: E = CGMTA(n=41, m=10, q=3)
            sage: E.is_underdefined_system()
            True
        """
        return super().is_underdefined_system()

    def linear_algebra_constant(self):
        """
        Return the linear algebra constant

        EXAMPLES::

            sage: from mpkc.algorithms import CGMTA
            sage: H = CGMTA(n=41, m=10, q=3)
            sage: H.linear_algebra_constant()
            <BLANKLINE>
        """
        return super().linear_algebra_constant()

    def npolynomials(self):
        """
        Return the number of polynomials

        EXAMPLES::

            sage: from mpkc.algorithms import CGMTA
            sage: H = CGMTA(n=41, m=10, q=3)
            sage: H.npolynomials()
            10
        """
        return super().npolynomials()

    def nvariables(self):
        """
        Return the number of variables

        EXAMPLES::

            sage: from mpkc.algorithms import CGMTA
            sage: H = CGMTA(n=41, m=10, q=3)
            sage: H.nvariables()
            41
        """
        return super().nvariables()

    def nvariables_reduced(self):
        """
        Return the no. of variables after fixing some values

        EXAMPLES::

            sage: from mpkc.algorithms import CGMTA
            sage: H = CGMTA(n=41, m=10, q=3)
            sage: H.nvariables_reduced()
            41
        """
        return super().nvariables_reduced()

    def npolynomials_reduced(self):
        """
        Return the no. of polynomials after applying the Thomae and Wolf strategy

        EXAMPLES::

            sage: from mpkc.algorithms import CGMTA
            sage: H = CGMTA(n=41, m=10, q=3)
            sage: H.npolynomials_reduced()
            10
        """
        return super().npolynomials_reduced()

    def optimal_parameters(self):
        """
        Return a dictionary of optimal parameters

        EXAMPLES::

            sage: from mpkc.algorithms import CGMTA
            sage: H = CGMTA(n=41, m=10, q=3)
            sage: H.optimal_parameters()
            {}
        """
        return super().optimal_parameters()

    def order_of_the_field(self):
        """
        Return the order of the field

        EXAMPLES::

            sage: from mpkc.algorithms import CGMTA
            sage: H = CGMTA(n=41, m=10, q=3)
            sage: H.order_of_the_field()
            3
        """
        return super().order_of_the_field()