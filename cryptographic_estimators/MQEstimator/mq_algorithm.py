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


from cryptographic_estimators.base_algorithm import BaseAlgorithm
from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
from cryptographic_estimators.helper import is_prime_power
from math import floor


class MQAlgorithm(BaseAlgorithm):
    def __init__(self, problem: MQProblem, **kwargs):
        """Base class for MQ algorithms complexity estimator.

        Args:
            problem (MQProblem): BaseProblem object including all necessary parameters.
            w (float, optional): Linear algebra constant. Defaults to 2.81.
            h (int, optional): External hybridization parameter. Defaults to 0.
            memory_access (int, optional): Specifies the memory access cost model.
                Defaults to 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root,
                3 - cube-root or deploy custom function which takes as input the
                logarithm of the total memory usage.
            complexity_type (int, optional): Complexity type to consider.
                Defaults to 0 (estimate), 1 (tilde O complexity).
        """
        super(MQAlgorithm, self).__init__(problem, **kwargs)

        h = kwargs.get("h", 0)
        w = kwargs.get("w", 2.81)
        n = self.problem.nvariables()
        m = self.problem.npolynomials()
        q = self.problem.order_of_the_field()
        self._name = "BaseMQAlgorithm"

        if n < 1:
            raise ValueError("n must be >= 1")

        if m < 1:
            raise ValueError("m must be >= 1")

        if q is not None and not is_prime_power(q):
            raise ValueError("q must be a prime power")

        if w < 2 or 3 < w:
            raise ValueError("w must be in the range 2 <= w <= 3")

        if h < 0:
            raise ValueError("h must be >= 0")

        self._n = n
        self._m = m
        self._q = q
        self._w = w
        self._h = h
        self._n_reduced = None
        self._m_reduced = None

    def nvariables_reduced(self):
        """Return the number of variables after fixing some values.

        Tests:
            >>> from cryptographic_estimators.MQEstimator.mq_algorithm import MQAlgorithm
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> MQAlgorithm(MQProblem(n=5, m=10, q=2)).nvariables_reduced()
            5
            >>> MQAlgorithm(MQProblem(n=25, m=20, q=2)).nvariables_reduced()
            20
        """
        if self._n_reduced is not None:
            return self._n_reduced

        n, m = self.problem.nvariables(), self.problem.npolynomials()
        if self.problem.is_underdefined_system():
            alpha = floor(n / m)
            if m - alpha + 1 > 1:
                self._n_reduced = m - alpha + 1
            else:
                self._n_reduced = m
        else:
            self._n_reduced = n

        self._n_reduced -= self._h

        if self.problem.is_underdefined_system():
            self.problem.nsolutions = 0
        return self._n_reduced

    def npolynomials_reduced(self):
        """Return the number of polynomials after applying the Thomae and Wolf strategy.
    
        Returns:
            int: The number of polynomials after applying the Thomae and Wolf strategy.

        Tests:
            >>> from cryptographic_estimators.MQEstimator.mq_algorithm import MQAlgorithm
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> MQAlgorithm(MQProblem(n=5, m=10, q=2)).npolynomials_reduced()
            10
            >>> MQAlgorithm(MQProblem(n=60, m=20, q=2)).npolynomials_reduced()
            18
        """
        if self._m_reduced is not None:
            return self._m_reduced

        m = self.problem.npolynomials()
        if self.problem.is_underdefined_system():
            self._m_reduced = self.nvariables_reduced()
        else:
            self._m_reduced = m
        return self._m_reduced

    def get_reduced_parameters(self):
        return (
            self.nvariables_reduced(),
            self.npolynomials_reduced(),
            self.problem.order_of_the_field(),
        )

    def linear_algebra_constant(self):
        """Returns the linear algebra constant.
    
        Tests:
            >>> from cryptographic_estimators.MQEstimator.mq_algorithm import MQAlgorithm
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> MQAlgorithm(MQProblem(n=10, m=5, q=4), w=2).linear_algebra_constant()
            2
        """
        return self._w

    def __repr__(self):
        n, m = self.problem.nvariables(), self.problem.npolynomials()
        return f"{self._name} estimator for the MQ problem with {n} variables and {m} polynomials"
