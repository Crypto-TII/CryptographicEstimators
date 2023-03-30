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
Module to compute the time and memory complexity of the algorithm Exhaustive Search

The Exhaustive Search is an algorithm to solve the MQ problem

[BCC+10] Bouillaguet, C., Chen, H., Cheng, C., Chou, T., Niederhagen, R., Shamir, A., and Yang, B.
Fast  exhaustive  search  for  polynomial  systems  in F2.   In Cryptographic  Hardware  andEmbedded Systems,
CHES 2010, 12th International Workshop, Santa Barbara, CA, USA,August 17-20, 2010. Proceedings, pages 203–218, 2010.
"""



from sage.all import Integer
from sage.functions.log import log
from sage.misc.functional import numerical_approx
from .base import BaseAlgorithm


class ExhaustiveSearch(BaseAlgorithm):
    r"""
    Construct an instance of Exhaustive Search estimator

    ExhaustiveSearch solves the MQ problem by evaluating all possible solutions until one is found.
    The formulas used in this module are generalizations of one shown in [BCCCNSY10]_

    INPUT:

    - ``n`` -- no. of variables
    - ``m`` -- no. of polynomials
    - ``q`` -- order of the finite field
    - ``nsolutions`` -- number of solutions (default: 1)

    EXAMPLES::

        sage: from mpkc.algorithms import ExhaustiveSearch
        sage: E = ExhaustiveSearch(q=3, n=10, m=12)
        sage: E
        Exhaustive search estimator for the MQ problem
    """
    def __init__(self, n, m, q, nsolutions=1):
        if not isinstance(q, (int, Integer)):
            raise TypeError("q must be an integer")

        super().__init__(n=n, m=m, q=q)
        self._nsolutions = nsolutions

    def nsolutions(self):
        """
        Return the number of solutions

        EXAMPLES::

            sage: from mpkc.algorithms import ExhaustiveSearch
            sage: E = ExhaustiveSearch(q=3, n=10, m=12, nsolutions=3)
            sage: E.nsolutions()
            3
        """
        return self._nsolutions

    def time_complexity(self):
        """
        Return the time complexity of the exhaustive search algorithm

        EXAMPLES::

            sage: from mpkc.algorithms import ExhaustiveSearch
            sage: E = ExhaustiveSearch(q=3, n=10, m=12)
            sage: E.time_complexity()
            61880.4962217569

        TESTS::

            sage: E0 = ExhaustiveSearch(n=15, m=12, q=3)
            sage: E1 = ExhaustiveSearch(n=17, m=12, q=3)
            sage: E0.time_complexity() == E1.time_complexity()
            True
        """
        n = self.nvariables_reduced()
        nsolutions = self.nsolutions()
        q = self.order_of_the_field()
        if q == 2:
            complexity = 4 * log(n, 2) * (2 ** n / (nsolutions + 1))
        else:
            complexity = log(n, q) * (q ** n / (nsolutions + 1))

        return numerical_approx(complexity)

    def memory_complexity(self):
        """
        Return the memory complexity of the exhaustive search algorithm

        EXAMPLES::

            sage: from mpkc.algorithms import ExhaustiveSearch
            sage: E = ExhaustiveSearch(q=3, n=10, m=12)
            sage: E.memory_complexity()
            1200

        TESTS::

            sage: E0 = ExhaustiveSearch(n=15, m=12, q=3)
            sage: E1 = ExhaustiveSearch(n=17, m=12, q=3)
            sage: E0.memory_complexity() == E1.memory_complexity()
            True
        """
        n, m = self.nvariables_reduced(), self.npolynomials_reduced()
        return m * n ** 2

    def tilde_o_time(self):
        """
        Return the Ō time complexity of the exhaustive search algorithm

        EXAMPLES::

            sage: from mpkc.algorithms import ExhaustiveSearch
            sage: E = ExhaustiveSearch(q=3, n=10, m=12)
            sage: E.tilde_o_time()
            59049
        """
        q = self.order_of_the_field()
        n = self.nvariables_reduced()
        return q ** n

    def __repr__(self):
        return f"Exhaustive search estimator for the MQ problem"

    # all methods below are implemented to overwrite the parent's docstring while keeping the implementation

    def has_optimal_parameter(self):
        """
        Return `True` if the algorithm has optimal parameter

        EXAMPLES::

            sage: from mpkc.algorithms import ExhaustiveSearch
            sage: H = ExhaustiveSearch(q=256, n=5, m=10)
            sage: H.has_optimal_parameter()
            False
        """
        return super().has_optimal_parameter()

    def is_defined_over_finite_field(self):
        """
        Return `True` if the algorithm is defined over a finite field

        EXAMPLES::

            sage: from mpkc.algorithms import ExhaustiveSearch
            sage: H = ExhaustiveSearch(q=256, n=5, m=10)
            sage: H.is_defined_over_finite_field()
            True
        """
        return super().is_defined_over_finite_field()

    def is_overdefined_system(self):
        """
        Return `True` if the system is overdefined

        EXAMPLES::

            sage: from mpkc.algorithms import ExhaustiveSearch
            sage: H = ExhaustiveSearch(q=256, n=5, m=10)
            sage: H.is_overdefined_system()
            True
            sage: E = ExhaustiveSearch(q=256, n=10, m=10)
            sage: E.is_overdefined_system()
            False
        """
        return super().is_overdefined_system()

    def is_square_system(self):
        """
        Return `True` if the system is square, there are equal no. of variables and polynomials

        EXAMPLES::

            sage: from mpkc.algorithms import ExhaustiveSearch
            sage: H = ExhaustiveSearch(q=256, n=5, m=10)
            sage: H.is_square_system()
            False
            sage: E = ExhaustiveSearch(q=256, n=10, m=10)
            sage: E.is_square_system()
            True
        """
        return super().is_square_system()

    def is_underdefined_system(self):
        """
        Return `True` if the system is underdefined

        EXAMPLES::

            sage: from mpkc.algorithms import ExhaustiveSearch
            sage: H = ExhaustiveSearch(q=256, n=5, m=10)
            sage: H.is_underdefined_system()
            False
            sage: E = ExhaustiveSearch(q=256, n=10, m=5)
            sage: E.is_underdefined_system()
            True
        """
        return super().is_underdefined_system()

    def linear_algebra_constant(self):
        """
        Return the linear algebra constant

        EXAMPLES::

            sage: from mpkc.algorithms import ExhaustiveSearch
            sage: H = ExhaustiveSearch(q=256, n=5, m=10)
            sage: H.linear_algebra_constant()
            <BLANKLINE>
        """
        return super().linear_algebra_constant()

    def npolynomials(self):
        """
        Return the number of polynomials

        EXAMPLES::

            sage: from mpkc.algorithms import ExhaustiveSearch
            sage: H = ExhaustiveSearch(q=256, n=5, m=10)
            sage: H.npolynomials()
            10
        """
        return super().npolynomials()

    def nvariables(self):
        """
        Return the number of variables

        EXAMPLES::

            sage: from mpkc.algorithms import ExhaustiveSearch
            sage: H = ExhaustiveSearch(q=256, n=10, m=10)
            sage: H.nvariables()
            10
        """
        return super().nvariables()

    def nvariables_reduced(self):
        """
        Return the no. of variables after fixing some values

        EXAMPLES::

            sage: from mpkc.algorithms import ExhaustiveSearch
            sage: H = ExhaustiveSearch(q=256, n=10, m=10)
            sage: H.nvariables_reduced()
            10
        """
        return super().nvariables_reduced()

    def npolynomials_reduced(self):
        """
        Return the no. of polynomials after applying the Thomae and Wolf strategy

        EXAMPLES::

            sage: from mpkc.algorithms import ExhaustiveSearch
            sage: H = ExhaustiveSearch(q=256, n=10, m=10)
            sage: H.npolynomials_reduced()
            10
        """
        return super().npolynomials_reduced()

    def optimal_parameters(self):
        """
        Return a dictionary of optimal parameters

        EXAMPLES::

            sage: from mpkc.algorithms import ExhaustiveSearch
            sage: H = ExhaustiveSearch(q=256, n=10, m=10)
            sage: H.optimal_parameters()
            {}
        """
        return super().optimal_parameters()

    def order_of_the_field(self):
        """
        Return the order of the field

        EXAMPLES::

            sage: from mpkc.algorithms import ExhaustiveSearch
            sage: H = ExhaustiveSearch(q=256, n=10, m=10)
            sage: H.order_of_the_field()
            256
        """
        return super().order_of_the_field()