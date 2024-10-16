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


from ..rsd_algorithm import RSDAlgorithm
from ..rsd_problem import RSDProblem
from ...base_algorithm import optimal_parameter
from math import log2, ceil
from math import comb as binomial


class MaxMinors(RSDAlgorithm):
    """
    Construct an instance of RSDAlgorithm1 estimator

    Add reference to correponding paper here.

    INPUT:

    - ``problem`` -- an instance of the RSDProblem class
    """

    def __init__(self, problem: RSDProblem, **kwargs):
        super(MaxMinors, self).__init__(problem, **kwargs)

        q, m, n, k, r = self.problem.get_parameters()
        self.set_parameter_ranges('a', 0, k)
        self.set_parameter_ranges('p', 0, n)
        self._name = "MaxMinors"

    @optimal_parameter
    def a(self):
        return self._get_optimal_parameter("a")

    @optimal_parameter
    def p(self):
        return self._get_optimal_parameter("p")

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """

        q, m, n, k, r = self.problem.get_parameters()
        a = parameters['a']
        p = parameters['p']
        print(a, p)
        w = self.w
        bin1 = binomial(n - p - k - 1, r)
        bin2 = binomial(n - p - a, r)
        time_complexity = a * r * log2(q) + log2(m) + log2(bin1) + (w - 1) * log2(bin2)

        return time_complexity

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        return 0

    # def _are_parameters_invalid(self, parameters: dict):
    #    """
    #    Specifies constraints on the parameters
    #    """
    #    q, m, n, k, r = self.problem.get_parameters()
    #    p = parameters['p']
    #    a = parameters['a']
    #    if n - p - k - 1 >= r:
    #        bin1 = m * binomial(n - p - k - 1, r)
    #        bin2 = binomial(n - p, r)-1

    #       #print("condition1", q,m,n,k,r,a,p, bin1 >= bin2)

    #    if n - a - p < r:
    #        return True

    #    #print("condition2", a, p, n - a - p >= r)

    #    return False

    def _valid_choices(self):
        """
        Generator which yields on each call a new set of valid parameters based on the `_parameter_ranges` and already
        set parameters in `_optimal_parameters`

        """
        print('valid_choices')
        new_ranges = self._fix_ranges_for_already_set_parameters()

        q, m, n, k, r = self.problem.get_parameters()

        for p in range(0, new_ranges['p']["max"] + 1):
            bin1 = m * binomial(n - p - k - 1, r)
            bin2 = binomial(n - p, r) - 1
            if bin1 >= bin2:
                for a in range(0, new_ranges['a']["max"] + 1):
                    if n - p - a >= r:
                        print({"a": a, "p": p})
                        yield {"a": a, "p": p}
            else:
                break
