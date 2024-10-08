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


from cryptographic_estimators.MQEstimator.mq_algorithm import MQAlgorithm
from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
from cryptographic_estimators.MQEstimator import degree_of_regularity
from math import log2, comb as binomial


class F5(MQAlgorithm):
    def __init__(self, problem: MQProblem, **kwargs):
        """Construct an instance of the F5 complexity estimator.

        Note:
            The complexity formula is taken from Proposition 1 in [BFP09]_.

        Args:
            problem (MQProblem): The MQProblem object including all necessary parameters.
            h (int, optional): The external hybridization parameter. Defaults to 0.
            w (float, optional): The linear algebra constant. Defaults to 2.81.
            degrees (list, tuple, optional): A list or tuple of the degrees of the polynomials. Defaults to [2] * m.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.f5 import F5
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = F5(MQProblem(n=10, m=5, q=3))
            >>> E
            F5 estimator for the MQ problem with 10 variables and 5 polynomials
        """

        m = problem.npolynomials()
        degrees = kwargs.get("degrees", [2] * m)
        if len(degrees) != m:
            raise ValueError(f"len(degrees) must be equal to {m}")

        super().__init__(problem, **kwargs)
        if degrees == [2] * m:
            self._degrees = [2] * self.npolynomials_reduced()
        else:
            self._degrees = degrees

        self._name = "F5"
        self._time_complexity = None
        self._memory_complexity = None
        self._dreg = None
        self._ncols_at_degree_dreg = None

    def degree_of_polynomials(self):
        """Return a list of degree of the polynomials.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.f5 import F5
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = F5(MQProblem(n=10, m=5, q=3))
            >>> E.degree_of_polynomials()
            [2, 2, 2, 2]
        """
        return self._degrees

    def _get_degree_of_regularity(self):
        if self._dreg is None:
            n, m, q = self.get_reduced_parameters()
            self._dreg = degree_of_regularity.quadratic_system(n, m, q)
        return self._dreg

    def _get_number_of_columns_at_degree_of_regularity(self):
        if self._ncols_at_degree_dreg is None:
            n, _, _ = self.get_reduced_parameters()
            dreg = self._get_degree_of_regularity()
            self._ncols_at_degree_dreg = max(binomial(n + dreg - 1, dreg), 1)
        return self._ncols_at_degree_dreg

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.f5 import F5
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = F5(MQProblem(n=10, m=15, q=3), bit_complexities=False)
            >>> E.time_complexity()
            30.550746998589286

        Tests:
            >>> F5(MQProblem(n=10, m=12, q=5)).time_complexity()
            40.548132826157364
            >>> E = F5(MQProblem(n=1, m=15, q=2), bit_complexities=False)
            >>> E.time_complexity()
            3.9068905956085187
        """
        _, m, q = self.get_reduced_parameters()
        w = self.linear_algebra_constant()
        ncols = self._get_number_of_columns_at_degree_of_regularity()
        time = w * log2(ncols)
        time += log2(m)
        h = self._h
        return h * log2(q) + max(time, self._time_complexity_fglm())

    def _time_complexity_fglm(self):
        """Return the time complexity of the FGLM algorithm for this system.

        Tests:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.f5 import F5
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = F5(MQProblem(n=10, m=15, q=3, nsolutions=1))
            >>> E._time_complexity_fglm()
            6.321928094887363
        """
        n, _, q = self.get_reduced_parameters()
        D = 2**self.problem.nsolutions
        h = self._h
        return h * log2(q) + log2(n * D**3)

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.f5 import F5
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> F5_ = F5(MQProblem(n=10, m=12, q=5), bit_complexities=False)
            >>> F5_.memory_complexity()
            24.578308707446713
        """
        n, m, _ = self.get_reduced_parameters()
        ncols = self._get_number_of_columns_at_degree_of_regularity()
        memory = max(log2(ncols) * 2, log2(m * n**2))
        return memory

    def _compute_tilde_o_time_complexity(self, parameters: dict):
        """Return the Ō time complexity of the algorithm for a given set of parameters."""
        q = self.problem.order_of_the_field()
        w = self.linear_algebra_constant()
        ncols = self._get_number_of_columns_at_degree_of_regularity()
        time = w * log2(ncols)
        h = self._h
        return h * log2(q) + max(time, self._tilde_o_time_complexity_fglm(parameters))

    def _tilde_o_time_complexity_fglm(self, parameters: dict):
        """Return the Ō time complexity of the FGLM algorithm for this system."""
        q = self.problem.order_of_the_field()
        D = 2**self.problem.nsolutions
        h = self._h
        return h * log2(q) + log2(D**3)

    def _compute_tilde_o_memory_complexity(self, parameters: dict):
        """Return the Ō memory complexity of the algorithm for a given set of parameters."""
        ncols = self._get_number_of_columns_at_degree_of_regularity()
        return log2(ncols) * 2
