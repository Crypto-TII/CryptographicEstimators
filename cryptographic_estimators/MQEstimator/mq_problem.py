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


from cryptographic_estimators.base_problem import BaseProblem
from cryptographic_estimators.MQEstimator.mq_helper import ngates
from cryptographic_estimators.MQEstimator.mq_constants import (
    MQ_NUMBER_VARIABLES,
    MQ_NUMBER_POLYNOMIALS,
    MQ_FIELD_SIZE,
)
from cryptographic_estimators.helper import is_prime_power
from math import log2, ceil


class MQProblem(BaseProblem):
    """
    Construct an instance of MQProblem

    INPUT:

    - ``n`` -- number of variables
    - ``m`` -- number of polynomials
    - ``q`` -- order of the finite field (default: None)
    - ``theta`` -- exponent of the conversion factor (default: 2)
        - If ``0 <= theta <= 2``, every multiplication in GF(q) is counted as `log2(q) ^ theta` binary operation.
        - If ``theta = None``, every multiplication in GF(q) is counted as `2 * log2(q) ^ 2 + log2(q)` binary operation.
    - ``nsolutions`` --  number of solutions in logarithmic scale (default: max(expected_number_solutions, 0))
    - ``memory_bound`` -- maximum allowed memory to use for solving the problem (default: inf)

    """

    def __init__(self, n: int, m: int, q: int, **kwargs):
        super().__init__(**kwargs)
        self.parameters[MQ_NUMBER_VARIABLES] = n
        self.parameters[MQ_NUMBER_POLYNOMIALS] = m
        self.parameters[MQ_FIELD_SIZE] = q
        self.nsolutions = kwargs.get("nsolutions", self.expected_number_solutions())
        self._theta = kwargs.get("theta", 2)

        if n < 1:
            raise ValueError("n must be >= 1")

        if m < 1:
            raise ValueError("m must be >= 1")

        if q is not None and not is_prime_power(q):
            raise ValueError("q must be a prime power")

        if self._theta is not None and not (0 <= self._theta <= 2):
            raise ValueError("theta must be either None or 0<=theta <= 2")

        if self.nsolutions < 0:
            raise ValueError("nsolutions must be >= 0")

    def to_bitcomplexity_time(self, basic_operations: float):
        """
        Returns the bit-complexity corresponding to basic_operations field multiplications

        INPUT:

        - ``basic_operations`` -- Number of field additions (logarithmic)

        """
        q = self.parameters[MQ_FIELD_SIZE]
        theta = self._theta
        return ngates(q, basic_operations, theta=theta)

    @property
    def theta(self):
        """
        Returns the runtime of the algorithm

        """
        return self._theta

    @theta.setter
    def theta(self, value: float):
        """
        Sets the runtime

        """
        self._theta = value

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """
        Returns the memory bit-complexity associated to a given number of elements to store

        INPUT:

        -``elements_to_store`` -- number of basic memory operations (logarithmic)

        """
        q = self.parameters[MQ_FIELD_SIZE]
        if q is None:
            return elements_to_store
        return log2(ceil(log2(q))) + elements_to_store

    def expected_number_solutions(self):
        """
        Returns the logarithm of the expected number of existing solutions to the problem

        """
        n, m, q = self.get_problem_parameters()
        return max(0, log2(q) * (n - m))

    def order_of_the_field(self):
        """
        Return the order of the field

        """
        q = self.parameters[MQ_FIELD_SIZE]
        return q

    def is_defined_over_finite_field(self):
        """
        Return `True` if the algorithm is defined over a finite field

        """
        return self.order_of_the_field()

    def npolynomials(self):
        """ "
        Return the number of polynomials

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: MQProblem(n=10, m=5, q=4).npolynomials()
            5
        """
        return self.parameters[MQ_NUMBER_POLYNOMIALS]

    def nvariables(self):
        """
        Return the number of variables

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: MQProblem(n=10, m=5, q=4).nvariables()
            10
        """
        return self.parameters[MQ_NUMBER_VARIABLES]

    def get_problem_parameters(self):
        """
        Returns n, m, q

        """
        return (
            self.parameters[MQ_NUMBER_VARIABLES],
            self.parameters[MQ_NUMBER_POLYNOMIALS],
            self.parameters[MQ_FIELD_SIZE],
        )

    def is_overdefined_system(self):
        """
        Return `True` if the system is overdefined

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: MQProblem(n=10, m=15, q=4).is_overdefined_system()
            True
            sage: MQProblem(n=10, m=5, q=4).is_overdefined_system()
            False
            sage: MQProblem(n=10, m=5, q=4).is_overdefined_system()
            False
        """
        return self.npolynomials() > self.nvariables()

    def is_underdefined_system(self):
        """
        Return `True` if the system is underdefined

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: MQProblem(n=10, m=5, q=4).is_underdefined_system()
            True
            sage: MQProblem(n=5, m=10, q=4).is_underdefined_system()
            False
            sage: MQProblem(n=10, m=10, q=4).is_underdefined_system()
            False
        """
        return self.nvariables() > self.npolynomials()

    def is_square_system(self):
        """
        Return `True` is the system is square, i.e. there are equal no. of variables and polynomials

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: MQProblem(n=10, m=10, q=4).is_square_system()
            True
            sage: MQProblem(n=10, m=5, q=4).is_square_system()
            False
        """
        return self.nvariables() == self.npolynomials()

    def __repr__(self):
        """ """
        n, m, q = self.get_problem_parameters()
        rep = (
            "MQ problem with (n,m,q) = "
            + "("
            + str(n)
            + ","
            + str(m)
            + ","
            + str(q)
            + ") over "
            + str(self.baseField)
        )

        return rep
