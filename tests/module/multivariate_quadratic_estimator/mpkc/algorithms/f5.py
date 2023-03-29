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


from sage.functions.other import binomial
from .base import BaseAlgorithm
from .. import degree_of_regularity


class F5(BaseAlgorithm):
    """
    Return an instance of F5 complexity estimator

    INPUT:

    - ``n`` -- no. of variables
    - ``m`` -- no. of polynomials
    - ``q`` -- order of the base field (default: None)
    - ``w`` -- linear algebra constant (default: 2)
    - ``nsolutions`` -- no. of solutions (default: 1)
    - ``degrees`` -- a list/tuple of degree of the polynomials (default: [2]*m)
    - ``h`` -- external hybridization parameter (default: 0)

    EXAMPLES::

        sage: from mpkc.algorithms import F5
        sage: F5_ = F5(n=10, m=5)
        sage: F5_
        Complexity estimator for F5 with 10 variables and 5 polynomials
    """
    def __init__(self, n, m, q=None, w=2, nsolutions=1, h=0, **kwargs):
        if not nsolutions >= 1:
            raise ValueError("nsolutions must be >= 1")

        degrees = kwargs.get('degrees', [2]*m)
        if len(degrees) != m:
            raise ValueError(f"len(degrees) must be equal to {m}")

        super().__init__(n, m, q=q, w=w, h=h)
        self._nsolutions = nsolutions
        if degrees == [2]*m:
            self._degrees = [2]*self.npolynomials_reduced()
        else:
            self._degrees = degrees
        self._time_complexity = None
        self._memory_complexity = None

    def degree_of_polynomials(self):
        """
        Return a list of degree of the polynomials

        EXAMPLES::

            sage: from mpkc.algorithms import F5
            sage: F5_ = F5(n=10, m=5, degrees=[3]*5)
            sage: F5_.degree_of_polynomials()
            [3, 3, 3, 3, 3]
        """
        return self._degrees

    def nsolutions(self):
        """
        Return the no. of solutions

        EXAMPLES::

            sage: from mpkc.algorithms import F5
            sage: F5_ = F5(n=10, m=5, nsolutions=3)
            sage: F5_.nsolutions()
            3
        """
        return self._nsolutions

    def time_complexity(self, **kwargs):
        """
        Return the time complexity of the F5 algorithm

        EXAMPLES::

            sage: from mpkc.algorithms import F5
            sage: F5_ = F5(n=10, m=15, degrees=[3]*15, q=31)
            sage: F5_.time_complexity()
            128005423260

        TESTS::

            sage: F5(n=10, m=15, q=3, degrees=[3]*15).time_complexity()
            961920960
            sage: F5(n=10, m=12, q=5).time_complexity()
            769536768
            sage: F0 = F5(n=15, m=12, q=5)
            sage: F1 = F5(n=17, m=12, q=5)
            sage: F0.time_complexity() == F1.time_complexity()
            True
        """
        if self._time_complexity is None:
            if self.is_overdefined_system():
                complexity = self.time_complexity_semi_regular_system()
            else:
                complexity = self.time_complexity_regular_system()

            if self.nsolutions() == 1:
                fglm_complexity = 0
            else:
                fglm_complexity = self.time_complexity_fglm()

            self._time_complexity = complexity + fglm_complexity

        return self._time_complexity

    def time_complexity_fglm(self):
        """
        Return the time complexity of the FGLM algorithm for this system

        EXAMPLES::

            sage: from mpkc.algorithms import F5
            sage: F5_ = F5(n=10, m=15, nsolutions=2)
            sage: F5_.time_complexity_fglm()
            80
        """
        n = self.nvariables_reduced()
        D = self.nsolutions()
        return n * D ** 3

    def time_complexity_regular_system(self):
        """
        Return the time complexity for regular system

        EXAMPLES::

            sage: from mpkc.algorithms import F5
            sage: F5_ = F5(n=10, m=5, q=31)
            sage: F5_.time_complexity_regular_system()
            63504

        TESTS::

            sage: F5(n=15, m=5, degrees=[2]*5, q=31).time_complexity_regular_system()
            3675
        """
        if not (self.is_square_system() or self.is_underdefined_system()):
            raise ValueError("regularity assumption is valid only on square or underdefined system")

        n, m = self.nvariables_reduced(), self.npolynomials_reduced()
        q = self.order_of_the_field()
        w = self.linear_algebra_constant()
        dreg = degree_of_regularity.quadratic_system(n, m, q=q)
        h = self._h
        return q ** h * m * binomial(n + dreg, dreg) ** w

    def time_complexity_semi_regular_system(self):
        """
        Return the time complexity for semi-regular system

        EXAMPLES::

            sage: from mpkc.algorithms import F5
            sage: F5_ = F5(n=5, m=10, q=7)
            sage: F5_.time_complexity_semi_regular_system()
            31360

        TESTS::

            sage: F5(n=5, m=15, degrees=[2]*15, q=7).time_complexity_semi_regular_system()
            6615
        """
        if not self.is_overdefined_system():
            raise ValueError("semi regularity assumption is valid only on overdefined system")

        n, m = self.nvariables_reduced(), self.npolynomials_reduced()
        w = self.linear_algebra_constant()
        q = self.order_of_the_field()
        degrees = self.degree_of_polynomials()
        dreg = degree_of_regularity.semi_regular_system(n, degrees, q)
        h = self._h
        return q ** h * m * binomial(n + dreg, dreg) ** w

    def memory_complexity(self):
        """
        Return the memory complexity of the F5 algorithm

        EXAMPLES::

            sage: from mpkc.algorithms import F5
            sage: F5_ = F5(n=10, m=12, q=5)
            sage: F5_.memory_complexity()
            25050025

        TESTS::

            sage: F0 = F5(n=15, m=12)
            sage: F1 = F5(n=17, m=12)
            sage: F0.memory_complexity() == F1.memory_complexity()
            True
        """
        if self._memory_complexity is None:
            n, m = self.nvariables_reduced(), self.npolynomials_reduced()
            q = self.order_of_the_field()
            degrees = self.degree_of_polynomials()
            dreg = degree_of_regularity.generic_system(n=n, degrees=degrees, q=q)
            self._memory_complexity = max(binomial(n + dreg - 1, dreg) ** 2, m * n ** 2)
        return self._memory_complexity

    def tilde_o_time(self):
        """
        Return the Ō time complexity of F5 algorithm

        EXAMPLES::

            sage: from mpkc.algorithms import F5
            sage: E = F5(n=10, m=12, q=5)
            sage: E.tilde_o_time()
            64128064
        """
        return self.time_complexity()/self.npolynomials()

    def __repr__(self):
        n, m = self.nvariables(), self.npolynomials()
        return f"Complexity estimator for F5 with {n} variables and {m} polynomials"
