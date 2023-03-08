
# Copyright 2023 


import collections
from .scipy_model import ScipyModel
from ..sd_problem import SDProblem
from .workfactor_helper import representations_asymptotic, binomial_approximation, may_ozerov_near_neighbor_time


class PrangeScipyModel(ScipyModel):
    def __init__(self, par_names: list, problem: SDProblem, iterations, accuracy):
        """
        Optimization model for workfactor computation of Prange's algorithm
        """
        par_names += ["p"]
        super().__init__(par_names, problem, iterations, accuracy)


    def _build_model_and_set_constraints(self):
        self.constraints = [
            {'type': 'ineq', 'fun': self._inject_vars(lambda x: 1 - self.rate(x) - self.w(x) - x.p)},
            {'type': 'ineq', 'fun': self._inject_vars(lambda x: self.rate(x) - x.p)},
            {'type': 'ineq', 'fun': self._inject_vars(lambda x: self.w(x) - x.p)},
        ]

    def _memory(self, x):
        return 0

    def _time_lists(self, x):
        return [binomial_approximation(self.rate(x), x.p)]

    def _time_perms(self, x):
        return max(0,
                   binomial_approximation(1., self.w(x))
                   - binomial_approximation(self.rate(x), x.p)
                   - binomial_approximation(1 - self.rate(x), self.w(x) - x.p)
                   - self.nsolutions
                   )

    def _time(self, x):
        x = self.set_vars(*x)
        return self._time_perms(x) + max(self._time_lists(x))
