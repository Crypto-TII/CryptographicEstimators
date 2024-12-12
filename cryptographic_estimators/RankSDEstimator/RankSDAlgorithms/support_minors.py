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


from ..ranksd_algorithm import RankSDAlgorithm
from ..ranksd_constants import RANKSD_NUMBER_OF_PUNCTURED_POSITIONS, \
    RANKSD_NUMBER_OF_COLUMNS_X_TO_GUESS, RANKSD_LINEAR_VARIABLES_DEGREE
from ..ranksd_helper import find_valid_choices_param_sm_fqm
from ..ranksd_problem import RankSDProblem
from ...base_algorithm import optimal_parameter


class SupportMinors(RankSDAlgorithm):
    """Construct an instance of SupportMinors estimator

       This algorithm tries to solve a given instance by solving the system from the
       Support Minors over Fq^m combined with MaxMinors over Fq modelling introduced in [BBBGT23]_

       Args:
           problem (RankSDAlgorithm): An instance of the RankSDAlgorithm class.
           **kwargs: Additional keyword arguments.
              w (int): Linear algebra constant (default: 3).
              theta (int): Exponent of the conversion factor (default: 2).

       Examples:
           >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.support_minors import SupportMinors
           >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
           >>> SM = SupportMinors(RankSDProblem(q=2,m=31,n=33,k=15,r=10))
           >>> SM
           SupportMinors estimator for the Rank Syndrome Decoding problem with (q, m, n, k, r) = (2, 31, 33, 15, 10)
    """

    def __init__(self, problem: RankSDProblem, **kwargs):
        super(SupportMinors, self).__init__(problem, **kwargs)
        _, n, _, k, _ = self.problem.get_parameters()
        self.set_parameter_ranges(RANKSD_LINEAR_VARIABLES_DEGREE, 1, 100)
        self.set_parameter_ranges(RANKSD_NUMBER_OF_COLUMNS_X_TO_GUESS, 0, k)
        self.set_parameter_ranges(RANKSD_NUMBER_OF_PUNCTURED_POSITIONS, 0, n)
        self.on_base_field = False
        self._name = "SupportMinors"

    @optimal_parameter
    def b(self):
        """Return the optimal `b`, such that Nb>=Mb-1,where Nb is the number rows and Mb is the number of columns.

           Examples:
                >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.support_minors import SupportMinors
                >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
                >>> SM = SupportMinors(RankSDProblem(q=2,m=31,n=33,k=15,r=10), w=2)
                >>> SM.b()
                1

           Tests:
                >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.support_minors import SupportMinors
                >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
                >>> SM = SupportMinors(RankSDProblem(q=2,m=37,n=41,k=18,r=13), w=2)
                >>> SM.b()
                2
        """
        return self._get_optimal_parameter(RANKSD_LINEAR_VARIABLES_DEGREE)

    @optimal_parameter
    def a(self):
        """Return the optimal `a`, i.e. the number of columns specialized in X.

           Examples:
                >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.support_minors import SupportMinors
                >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
                >>> SM = SupportMinors(RankSDProblem(q=2,m=31,n=33,k=15,r=10), w=2)
                >>> SM.a()
                11

           Tests:
                >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.support_minors import SupportMinors
                >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
                >>> SM = SupportMinors(RankSDProblem(q=2,m=37,n=41,k=18,r=13), w=2)
                >>> SM.a()
                14
        """
        return self._get_optimal_parameter(RANKSD_NUMBER_OF_COLUMNS_X_TO_GUESS)

    @optimal_parameter
    def p(self):
        """Return the optimal `p`, i.e. the number of positions to puncture the code.

           Examples:
                >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.support_minors import SupportMinors
                >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
                >>> SM = SupportMinors(RankSDProblem(q=2,m=31,n=33,k=15,r=10), w=2)
                >>> SM.p()
                0

           Tests:
                >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.support_minors import SupportMinors
                >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
                >>> SM = SupportMinors(RankSDProblem(q=2,m=37,n=41,k=18,r=13), w=2)
                >>> SM.p()
                0

                >>> SM = SupportMinors(RankSDProblem(q=2,m=37,n=41,k=18,r=6), w=2)
                >>> SM.p()
                0
        """
        return self._get_optimal_parameter(RANKSD_NUMBER_OF_PUNCTURED_POSITIONS)

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.

           Args:
              parameters (dict): Dictionary including the parameters.

           Tests:
              >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.support_minors import SupportMinors
              >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
              >>> SM = SupportMinors(RankSDProblem(q=2,m=31,n=33,k=15,r=10), w=2)
              >>> SM.time_complexity()
              155.10223904640839
        """

        a = parameters[RANKSD_NUMBER_OF_COLUMNS_X_TO_GUESS]
        b = parameters[RANKSD_LINEAR_VARIABLES_DEGREE]
        p = parameters[RANKSD_NUMBER_OF_PUNCTURED_POSITIONS]
        return self.compute_time_complexity_helper(a, b, p, self.on_base_field)

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters

           Args:
               parameters (dict): Dictionary including the parameters.

           Tests:
               >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.support_minors import SupportMinors
               >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
               >>> SM = SupportMinors(RankSDProblem(q=2,m=31,n=33,k=15,r=10), w=2)
               >>> SM.memory_complexity()
               40.148042736021516
        """
        a = parameters[RANKSD_NUMBER_OF_COLUMNS_X_TO_GUESS]
        b = parameters[RANKSD_LINEAR_VARIABLES_DEGREE]
        p = parameters[RANKSD_NUMBER_OF_PUNCTURED_POSITIONS]
        return self.compute_memory_complexity_helper(a, b, p, self.on_base_field)

    def _valid_choices(self):
        """Generator yielding new sets of valid parameters.
        """
        new_ranges = self._fix_ranges_for_already_set_parameters()
        a_min = new_ranges[RANKSD_NUMBER_OF_COLUMNS_X_TO_GUESS]["min"]
        a_max = new_ranges[RANKSD_NUMBER_OF_COLUMNS_X_TO_GUESS]["max"]
        p_min = new_ranges[RANKSD_NUMBER_OF_PUNCTURED_POSITIONS]["min"]
        p_max = new_ranges[RANKSD_NUMBER_OF_PUNCTURED_POSITIONS]["max"]
        b_min = new_ranges[RANKSD_LINEAR_VARIABLES_DEGREE]["min"]
        b_max = new_ranges[RANKSD_LINEAR_VARIABLES_DEGREE]["max"]
        _, m, n, k, r = self.problem.get_parameters()

        valid_choices = find_valid_choices_param_sm_fqm(m, n, k, r, a_min, a_max, p_min, p_max, b_min, b_max)

        if len(valid_choices) > 0:
            for valid_choice in valid_choices:
                yield {RANKSD_LINEAR_VARIABLES_DEGREE: valid_choice[RANKSD_LINEAR_VARIABLES_DEGREE],
                       RANKSD_NUMBER_OF_COLUMNS_X_TO_GUESS: valid_choice[RANKSD_NUMBER_OF_COLUMNS_X_TO_GUESS],
                       RANKSD_NUMBER_OF_PUNCTURED_POSITIONS: valid_choice[RANKSD_NUMBER_OF_PUNCTURED_POSITIONS]}
