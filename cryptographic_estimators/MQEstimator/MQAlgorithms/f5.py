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


from ...MQEstimator.mq_algorithm import MQAlgorithm
from ...MQEstimator.mq_problem import MQProblem
from ...MQEstimator import degree_of_regularity
from ...helper import ComplexityType
from math import log2, inf
from sage.functions.other import binomial


class F5(MQAlgorithm):
    """
    Construct an instance of F5 complexity estimator

    INPUT:

    - ``problem`` -- MQProblem object including all necessary parameters
    - ``h`` -- external hybridization parameter (default: 0)
    - ``w`` -- linear algebra constant (default: 2)
    - ``degrees`` -- a list/tuple of degree of the polynomials (default: [2]*m)

    EXAMPLES::

        sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.f5 import F5
        sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
        sage: E = F5(MQProblem(n=10, m=5, q=3))
        sage: E
        F5 estimator for the MQ problem with 10 variables and 5 polynomials
    """

    def __init__(self, problem: MQProblem, **kwargs):
        m = problem.npolynomials()
        degrees = kwargs.get('degrees', [2]*m)
        if len(degrees) != m:
            raise ValueError(f"len(degrees) must be equal to {m}")

        super().__init__(problem, **kwargs)
        if degrees == [2]*m:
            self._degrees = [2]*self.npolynomials_reduced()
        else:
            self._degrees = degrees

        self._name = "F5"
        self._time_complexity = None
        self._memory_complexity = None
        self._dreg = None

    def degree_of_polynomials(self):
        """
        Return a list of degree of the polynomials

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.f5 import F5
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = F5(MQProblem(n=10, m=5, q=3))
            sage: E.degree_of_polynomials()
            [2, 2, 2, 2]

        """
        return self._degrees

    def time_complexity(self):
        """
        Return the time complexity of the F5 algorithm

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.f5 import F5
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = F5(MQProblem(n=10, m=15, q=3))
            sage: E.time_complexity()
            19.934452517671986

        TESTS::

            sage: F5(MQProblem(n=10, m=12, q=5)).time_complexity()
            25.934452517671986

        """
        memory = self.memory_complexity()
        if self.bit_complexities:
            memory = self.problem.to_bitcomplexity_memory(memory)
        if memory > self.problem.memory_bound:
            self._time_complexity = inf
            self._memory_complexity = inf
            return inf

        if self._time_complexity is None:
            if self.problem.is_overdefined_system():
                self._time_complexity = self._time_complexity_semi_regular_system()
            else:
                self._time_complexity = self._time_complexity_regular_system()

            if self.complexity_type == ComplexityType.ESTIMATE.value:
                self._time_complexity = max(
                    self._time_complexity, self._time_complexity_fglm())

        return self._time_complexity

    def _time_complexity_fglm(self):
        """
        Return the time complexity of the FGLM algorithm for this system

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.f5 import F5
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = F5(MQProblem(n=10, m=15, q=3, nsolutions=1))
            sage: E._time_complexity_fglm()
            6.321928094887363
        """
        n, _, q = self.get_reduced_parameters()
        D = 2 ** self.problem.nsolutions
        h = self._h
        return h * log2(q) + log2(n * D ** 3)

    def _time_complexity_regular_system(self):
        """
        Return the time complexity for regular system

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.f5 import F5
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = F5(MQProblem(n=10, m=5, q=3))
            sage: E._time_complexity_regular_system()
            12.643856189774725
        """
        if not (self.problem.is_square_system() or self.problem.is_underdefined_system()):
            raise ValueError(
                "regularity assumption is valid only on square or underdefined system")

        n, m, q = self.get_reduced_parameters()
        w = self.linear_algebra_constant()
        if self._dreg is None:
            self._dreg = degree_of_regularity.quadratic_system(n, m, q)
        dreg = self._dreg
        time = w * log2(binomial(n + dreg - 1, dreg))
        if self.complexity_type == ComplexityType.ESTIMATE.value:
            time += w * log2(m)
        h = self._h
        return h * log2(q) + time

    def _time_complexity_semi_regular_system(self):
        """
        Return the time complexity for semi-regular system

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.f5 import F5
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: F5_ = F5(MQProblem(n=5, m=10, q=3))
            sage: F5_._time_complexity_semi_regular_system()
            11.614709844115207
        """
        if not self.problem.is_overdefined_system():
            raise ValueError(
                "semi regularity assumption is valid only on overdefined system")

        n, m, q = self.get_reduced_parameters()
        w = self.linear_algebra_constant()
        if self._dreg is None:
            self._dreg = degree_of_regularity.quadratic_system(n, m, q)
        dreg = self._dreg
        h = self._h
        return h * log2(q) + w * log2(binomial(n + dreg, dreg))

    def memory_complexity(self):
        """
        Return the memory complexity of the F5 algorithm

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.f5 import F5
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: F5_ = F5(MQProblem(n=10, m=12, q=5))
            sage: F5_.memory_complexity()
            24.578308707446713
        """
        if self._memory_complexity is None:
            n, m, q = self.get_reduced_parameters()
            if self._dreg is None:
                self._dreg = degree_of_regularity.quadratic_system(n, m, q)
            dreg = self._dreg
            self._memory_complexity = log2(
                max(binomial(n + dreg - 1, dreg) ** 2, m * n ** 2))
            if self._memory_complexity == m * n ** 2 and self.complexity_type == ComplexityType.TILDEO.value:
                self._memory_complexity = 0
        return self._memory_complexity
