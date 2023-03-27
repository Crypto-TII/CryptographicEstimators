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

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.f5 import F5
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = F5(MQProblem(n=10, m=15, q=3), bit_complexities=False)
            sage: E.time_complexity()
            23.841343113280505

        TESTS::

            sage: F5(MQProblem(n=10, m=12, q=5)).time_complexity()
            31.950061609866715

        """
        if self.problem.is_overdefined_system():
            time = self._time_complexity_semi_regular_system()
        else:
            time = self._time_complexity_regular_system()

        return max(time, self._time_complexity_fglm())

    def _time_complexity_fglm(self):
        """
        Return the time complexity of the FGLM algorithm for this system

        TEST::

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

        TEST::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.f5 import F5
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = F5(MQProblem(n=10, m=5, q=31), bit_complexities=False)
            sage: E.time_complexity()
            15.954559846999834
        """
        if not (self.problem.is_square_system() or self.problem.is_underdefined_system()):
            raise ValueError(
                "regularity assumption is valid only on square or underdefined system")

        n, m, q = self.get_reduced_parameters()
        w = self.linear_algebra_constant()
        if self._dreg is None:
            self._dreg = degree_of_regularity.quadratic_system(n, m, q)
        dreg = self._dreg
        time = w * log2(binomial(n + dreg, dreg))
        time += log2(m)
        h = self._h
        return h * log2(q) + time

    def _time_complexity_semi_regular_system(self):
        """
        Return the time complexity for semi-regular system

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.f5 import F5
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: F5_ = F5(MQProblem(n=5, m=10, q=31), bit_complexities=False)
            sage: F5_.time_complexity()
            14.93663793900257
        """
        if not self.problem.is_overdefined_system():
            raise ValueError(
                "semi regularity assumption is valid only on overdefined system")

        n, m, q = self.get_reduced_parameters()
        w = self.linear_algebra_constant()
        if self._dreg is None:
            self._dreg = degree_of_regularity.quadratic_system(n, m, q)
        dreg = self._dreg
        time = w * log2(binomial(n + dreg, dreg))
        time += log2(m)
        h = self._h
        return h * log2(q) + time

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.f5 import F5
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: F5_ = F5(MQProblem(n=10, m=12, q=5), bit_complexities=False)
            sage: F5_.memory_complexity()
            24.578308707446713

        """
        n, m, q = self.get_reduced_parameters()
        if self._dreg is None:
            self._dreg = degree_of_regularity.quadratic_system(n, m, q)
        dreg = self._dreg
        memory = max(log2(binomial(n + dreg - 1, dreg)) * 2, log2(m * n ** 2))
        return memory


    def _compute_tilde_o_time_complexity(self, parameters: dict):
        """
        Return the Ō time complexity of the algorithm for a given set of parameters

        """
        if self.problem.is_overdefined_system():
            time = self._tilde_o_time_complexity_semi_regular_system(parameters)
        else:
            time = self._tilde_o_time_complexity_regular_system(parameters)

        return max(time, self._tilde_o_time_complexity_fglm(parameters))

    def _tilde_o_time_complexity_fglm(self, parameters: dict):
        """
        Return the Ō time complexity of the FGLM algorithm for this system

        """
        _, _, q = self.get_reduced_parameters()
        D = 2 ** self.problem.nsolutions
        h = self._h
        return h * log2(q) + log2(D ** 3)

    def _tilde_o_time_complexity_regular_system(self, parameters: dict):
        """
        Return the Ō time complexity for regular system

        """
        if not (self.problem.is_square_system() or self.problem.is_underdefined_system()):
            raise ValueError(
                "regularity assumption is valid only on square or underdefined system")

        n, m, q = self.get_reduced_parameters()
        w = self.linear_algebra_constant()
        if self._dreg is None:
            self._dreg = degree_of_regularity.quadratic_system(n, m, q)
        dreg = self._dreg
        time = w * log2(binomial(n + dreg, dreg))
        h = self._h
        return h * log2(q) + time

    def _tilde_o_time_complexity_semi_regular_system(self,  parameters: dict):
        """
        Return the Ō time complexity for semi-regular system

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

    def _compute_tilde_o_memory_complexity(self, parameters: dict):
        """
        Return the Ō  memory complexity of the algorithm for a given set of parameters

        """
        n, m, q = self.get_reduced_parameters()
        if self._dreg is None:
            self._dreg = degree_of_regularity.quadratic_system(n, m, q)
        dreg = self._dreg
        return log2(binomial(n + dreg - 1, dreg)) * 2