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


import inspect
from prettytable import PrettyTable
from sage.functions.log import log
from .algorithms.base import BaseAlgorithm
from .algorithms import HybridF5
from .utils import ngates, nbits, truncate


class MQEstimator(object):
    """
    Construct an instance of MQ Estimator

    INPUT:

    - ``n`` -- no. of variables
    - ``m`` -- no. of polynomials
    - ``q`` -- order of the finite field (default: None)
    - ``w`` -- linear algebra constant (default: 2)
    - ``theta`` -- bit complexity exponent (default: 0)
    - ``h`` -- external hybridization parameter (default: 0)
    - ``nsolutions`` -- no. of solutions (default: 1)
    - ``excluded_algorithms`` -- a list/tuple of excluded algorithms (default: None)

    EXAMPLES::

        sage: from mpkc import MQEstimator
        sage: MQEstimator(n=10, m=5)
        MQ Estimator for system with 10 variables and 5 equations
    """
    def __init__(self, n, m, q=None, w=2, theta=0, h=0, nsolutions=1, **kwargs):
        constructor_args = {arg: value for (arg, value) in locals().items()
                            if arg in ('n', 'm', 'q', 'w', 'h', 'nsolutions')}

        excluded_algorithms = kwargs.get("excluded_algorithms", tuple())
        if excluded_algorithms and any(not issubclass(Algorithm, BaseAlgorithm) for Algorithm in excluded_algorithms):
            raise TypeError(f"all excluded algorithms must be a subclass of {BaseAlgorithm.__name__}")

        self._algorithms = []
        included_algorithms = (Algorithm for Algorithm in BaseAlgorithm.__subclasses__()
                               if Algorithm not in excluded_algorithms)

        for Algorithm in included_algorithms:
            alg_constructor_args = inspect.getargs(Algorithm.__init__.__code__).args
            arg_and_values = {arg: constructor_args[arg] for arg in alg_constructor_args
                              if arg in constructor_args and arg != 'self'}

            try:
                algorithm = Algorithm(**arg_and_values)
            except (ValueError, TypeError):
                continue

            if algorithm.is_defined_over_finite_field() and q != algorithm.order_of_the_field():
                continue

            self._algorithms.append(algorithm)
            self._q = q
            self._theta = theta
            self._h = h
            setattr(self, algorithm.__module__.split('.')[-1], algorithm)

    def algorithms(self):
        """
        Return a list of considered algorithms

        EXAMPLES::

            sage: from mpkc import MQEstimator
            sage: E = MQEstimator(n=10, m=15, q=2)
            sage: E.algorithms()
            [Complexity estimator for F5 with 10 variables and 15 polynomials,
             Complexity estimator for hybrid approach with 10 variables and 15 polynomials,
             Dinur's first estimator for the MQ problem,
             Dinur's second estimator for the MQ problem,
             Exhaustive search estimator for the MQ problem,
             Björklund et al.'s estimator for the MQ problem,
             Lokshtanov et al.'s estimator for the MQ problem,
             BooleanSolve and FXL estimators for the MQ problem,
             Crossbred estimator for the MQ problem]

        TESTS::

            sage: E = MQEstimator(n=10, m=15, q=3)
            sage: E.algorithms()
            [Complexity estimator for F5 with 10 variables and 15 polynomials,
             Complexity estimator for hybrid approach with 10 variables and 15 polynomials,
             Exhaustive search estimator for the MQ problem,
             Lokshtanov et al.'s estimator for the MQ problem,
             BooleanSolve and FXL estimators for the MQ problem,
             Crossbred estimator for the MQ problem]
        """
        return self._algorithms

    def algorithm_names(self):
        """
        Return a list of the name of considered algorithms

        EXAMPLES::

            sage: from mpkc import MQEstimator
            sage: E = MQEstimator(n=10, m=15, q=2)
            sage: E.algorithm_names()
            ['F5',
             'HybridF5',
             'DinurFirst',
             'DinurSecond',
             'ExhaustiveSearch',
             'Bjorklund',
             'Lokshtanov',
             'BooleanSolveFXL',
             'Crossbred']

        TESTS::

            sage: E = MQEstimator(n=10, m=15, q=3)
            sage: E.algorithm_names()
            ['F5',
             'HybridF5',
             'ExhaustiveSearch',
             'Lokshtanov',
             'BooleanSolveFXL',
             'Crossbred']
        """
        return [algorithm.__class__.__name__ for algorithm in self.algorithms()]

    def nalgorithms(self):
        """
        Return the number of considered algorithms

        EXAMPLES::

            sage: from mpkc import MQEstimator
            sage: E0 = MQEstimator(n=10, m=15, q=2)
            sage: E0.nalgorithms()
            9
            sage: E1 = MQEstimator(n=183, m=12, q=4)
            sage: E1.nalgorithms()
            9

        TESTS::

            sage: E = MQEstimator(n=10, m=15, q=3)
            sage: E.nalgorithms()
            6
        """
        return len(self.algorithms())

    def table(self, use_tilde_o_time=False, precision=3):
        """
        Return the table describing the complexity of each algorithm and its optimal parameters

        INPUT:

        - ``use_tilde_o_time`` -- use Ō time complexity (default: False)
        - ``precision`` -- number of decimal places in the complexities exponent

        EXAMPLES::

            sage: from mpkc import MQEstimator
            sage: E = MQEstimator(n=15, m=15, q=2)
            sage: table = E.table()
            sage: print(table)
            +------------------+--------+--------+---------------------------+
            |    algorithm     |  time  | memory |         parameters        |
            +------------------+--------+--------+---------------------------+
            |        F5        | 27.747 | 23.158 |                           |
            |     HybridF5     | 21.076 | 3.906  |           k: 14           |
            |    DinurFirst    | 32.111 | 21.493 |      λ: 1/14, κ: 1/7      |
            |   DinurSecond    | 20.349 | 15.801 |           n1: 2           |
            | ExhaustiveSearch | 17.966 | 11.72  |                           |
            |    Bjorklund     | 42.451 | 15.316 |           λ: 1/5          |
            |    Lokshtanov    | 67.123 | 16.105 |          δ: 1/15          |
            | BooleanSolveFXL  | 20.339 | 5.825  | k: 14, variant: las_vegas |
            |    Crossbred     | 17.672 | 16.785 |      D: 4, k: 9, d: 1     |
            +------------------+--------+--------+---------------------------+


        TESTS::

            sage: E = MQEstimator(n=15, m=15, q=3)  # DinurFirst, DinurSecond, and Bjorklund are skipped for q != 2
            sage: print(E.table())
            +------------------+--------+--------+---------------------------+
            |    algorithm     |  time  | memory |         parameters        |
            +------------------+--------+--------+---------------------------+
            |        F5        | 35.362 | 30.484 |                           |
            |     HybridF5     | 28.541 |  8.55  |           k: 10           |
            | ExhaustiveSearch | 24.076 | 11.72  |                           |
            |    Lokshtanov    | 98.227 | 24.266 |          δ: 1/15          |
            | BooleanSolveFXL  | 28.529 | 5.711  | k: 14, variant: las_vegas |
            |    Crossbred     | 23.36  | 22.091 |      D: 5, k: 7, d: 1     |
            +------------------+--------+--------+---------------------------+


            sage: from mpkc.algorithms import F5, HybridF5
            sage: E = MQEstimator(n=15, m=15, q=3, excluded_algorithms=[F5, HybridF5])  # tests excluded algorithms
            sage: print(E.table())
            +------------------+--------+--------+---------------------------+
            |    algorithm     |  time  | memory |         parameters        |
            +------------------+--------+--------+---------------------------+
            | ExhaustiveSearch | 24.076 | 11.72  |                           |
            |    Lokshtanov    | 98.227 | 24.266 |          δ: 1/15          |
            | BooleanSolveFXL  | 28.529 | 5.711  | k: 14, variant: las_vegas |
            |    Crossbred     | 23.36  | 22.091 |      D: 5, k: 7, d: 1     |
            +------------------+--------+--------+---------------------------+
        """
        table = PrettyTable()
        table.field_names = ['algorithm', 'time', 'memory', 'parameters']

        #h = self._h
        for algorithm in self.algorithms():
            name = algorithm.__class__.__name__
            time_complexity = algorithm.tilde_o_time() if use_tilde_o_time else algorithm.time_complexity()
            memory_complexity = algorithm.memory_complexity()
            optimal_parameters = ', '.join([f"{k}: {v}" for k, v in algorithm.optimal_parameters().items()])

 #           time_complexity *= 2 ** h
            if self._q is not None and self._theta > 0:
                time_complexity = ngates(self._q, time_complexity, theta=self._theta)
                memory_complexity = nbits(self._q, memory_complexity)

            table.add_row([name,
                           truncate(log(time_complexity, 2), precision),
                           truncate(log(memory_complexity, 2), precision),
                           optimal_parameters])

        return table

    def fastest_algorithm(self, use_tilde_o_time=False):
        """
         Return the algorithm with the smallest time complexity

         INPUT:

         - ``use_tilde_o_time`` -- use Ō time complexity (default: False)

         EXAMPLES::

             sage: from mpkc import MQEstimator
             sage: E = MQEstimator(n=15, m=15, q=2)
             sage: E.fastest_algorithm()
             Crossbred estimator for the MQ problem
         """
        key = lambda algorithm: algorithm.tilde_o_time() if use_tilde_o_time else algorithm.time_complexity()
        return min(self.algorithms(), key=key)

    def __repr__(self):
        algorithm = self.algorithms()[0]
        n = algorithm.nvariables()
        m = algorithm.npolynomials()
        return f"MQ Estimator for system with {n} variables and {m} equations"


def min_npolynomials(security_level, q, w=2):
    """
    Return a minimum number of equations in a determined system that satisfies the given security level

    INPUT:

    - ``security_level`` -- the intended security level (in bits) (80/100/128/192/256)
    - ``q`` -- order of the finite field
    - ``w`` -- linear algebra constant (2 <= w <= 3) (default: 2)

    EXAMPLES::

        sage: from mpkc.mq_estimator import min_npolynomials
        sage: min_npolynomials(security_level=80, q=16)
        31

    TESTS::

        sage: min_npolynomials(security_level=80, q=31)
        30
        sage: min_npolynomials(security_level=80, q=256)
        26
        sage: min_npolynomials(security_level=100, q=16)
        40
        sage: min_npolynomials(security_level=100, q=31)
        38
        sage: min_npolynomials(security_level=100, q=256)
        35
    """
    if security_level not in (80, 100, 128, 192, 256):
        raise ValueError("the valid parameter for security_level is {80, 100, 128, 192, 256}")

    m = 2
    while log(HybridF5(n=m, m=m, q=q, w=w).time_complexity(), 2) < security_level:
        m += 1

    return m


def min_nvariables(security_level, q, w=2):
    """
    Return a minimum number of variables in a determined system that satisfies the given security level

    INPUT:

    - ``security_level`` -- the intended security level (in bits) (80/100/128/192/256)
    - ``q`` -- order of the finite field
    - ``w`` -- linear algebra constant (2 <= w <= 3) (default: 2)

    EXAMPLES::

        sage: from mpkc.mq_estimator import min_nvariables
        sage: min_nvariables(security_level=80, q=16)
        31
    """
    return min_npolynomials(security_level, q, w)
