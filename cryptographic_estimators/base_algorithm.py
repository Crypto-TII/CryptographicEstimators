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


from typing import Union, Callable
from .helper import ComplexityType
import functools
from math import inf, log2
from .base_constants import BASE_BIT_COMPLEXITIES, BASE_COMPLEXITY_TYPE, BASE_ESTIMATE, BASE_MEMORY_ACCESS, BASE_TILDEO, BASE_ATTACK_TYPE


class BaseAlgorithm:
    def __init__(self, problem, **kwargs):
        """Base class for algorithms complexity estimator.

        Args:
            problem (BaseProblem): BaseProblem object including all necessary parameters
            memory_access (int, optional): Specifies the memory access cost model. Defaults to 0.
                Choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root
                or deploy custom function which takes as input the logarithm of the total memory usage.
            complexity_type (int, optional): Complexity type to consider. Defaults to 0.
                0: estimate, 1: tilde O complexity
            bit_complexities (int, optional): Determines if complexity is given in bit operations
                or basic operations. Defaults to 1 (in bit).
        """

        self.bit_complexities = kwargs.get(BASE_BIT_COMPLEXITIES, 1)
        self._complexity_type = kwargs.get(
            BASE_COMPLEXITY_TYPE, ComplexityType.ESTIMATE.value)
        self._memory_access = kwargs.get(BASE_MEMORY_ACCESS, 0)

        if not callable(self._memory_access) and self._memory_access not in [0, 1, 2, 3]:
            raise ValueError("memory_access must either 0, 1, 2, 3 or a sage function")

        if self._complexity_type not in [0, 1]:
            raise ValueError("complexity_type must either 0 or 1")

        if self.bit_complexities not in [0, 1]:
            raise ValueError("bit_complexities must either 0 or 1")


        self._optimal_parameters = dict()
        self._verbose_information = dict()
        self.problem = problem
        self._time_complexity = None
        self._memory_complexity = None
        self._parameter_ranges = dict()
        self._optimal_parameters_methods = self._get_optimal_parameter_methods_()
        self._current_minimum_for_early_abort = inf
        for i in self._optimal_parameters_methods:
            self._parameter_ranges[i.__name__] = {}

        self._attack_type = BASE_ATTACK_TYPE
        self._time_complexity_is_convex = False

    @property
    def parameter_ranges(self):
        """Returns the set ranges for optimal parameter search.
    
        Returns the set ranges in which optimal parameters are searched by the
        optimization algorithm (used only for complexity type estimate).
        """
        if self.complexity_type == ComplexityType.ESTIMATE.value:
            return self._parameter_ranges

    @property
    def memory_access(self):
        """Returns the attribute _memory_access."""
        return self._memory_access

    @memory_access.setter
    def memory_access(self, new_memory_access: Union[int, Callable[[float], float]]):
        """Sets the attribute _memory_access and resets internal state respectively.
    
        Args:
            new_memory_access (Union[int, Callable[[float], float]]): New memory_access value.
        """
        if new_memory_access not in [0, 1, 2, 3] and not callable(self.memory_access):
            raise ValueError("invalid value for memory_access")
        if self._memory_access != new_memory_access:
            self.reset()
            self._memory_access = new_memory_access

    @property
    def complexity_type(self):
        """Returns the attribute _complexity_type."""
        return self._complexity_type
    
    @property
    def attack_type(self):
        """Returns the attack type of the algorithm."""
        return self._attack_type

    @complexity_type.setter
    def complexity_type(self, input_type: Union[int, str]):
        """Sets the attribute _complexity_type and resets internal state respectively.
    
        Args:
            input_type (Union[int, str]): New complexity_type value.
        """
        if type(input_type) is str:
            if input_type == BASE_ESTIMATE:
                new_type = ComplexityType.ESTIMATE.value
            elif input_type == BASE_TILDEO:
                new_type = ComplexityType.TILDEO.value
            else:
                raise ValueError(
                    "the complexity type should be either the string ESTIMATE or TILDEO")

        elif input_type not in [ComplexityType.ESTIMATE.value, ComplexityType.TILDEO.value]:
            raise ValueError("invalid value for complexity_type")

        else:
            new_type = input_type

        if self._complexity_type != new_type:
            self.reset()
            self._complexity_type = new_type

    # FIX: What memory_access?
    def memory_access_cost(self, mem: float):
        """Returns the memory access cost (in logarithmic scale) of the algorithm per basic operation.
    
        Args:
            mem (float): Memory consumption of an algorithm.
    
        Returns:
            float: Memory access cost in logarithmic scale.
    
        Note:
            memory_access: Specifies the memory access cost model 
            (default: 0, choices:
            0 - constant,
            1 - logarithmic,
            2 - square-root,
            3 - cube-root or deploy custom function which takes as input the
            logarithm of the total memory usage)
        """
        if self._memory_access == 0:
            return 0
        elif self._memory_access == 1:
            return log2(mem)
        elif self._memory_access == 2:
            return mem / 2
        elif self._memory_access == 3:
            return mem / 3
        elif callable(self._memory_access):
            return self._memory_access(mem)
        return 0

    def _get_verbose_information(self):
        """Returns dictionary with any additional information relevant to this algorithm."""
        return dict()

    def reset(self):
        """Resets internal state of the algorithm."""
        self._complexity_type = ComplexityType.ESTIMATE.value
        self._optimal_parameters = {}
        self._time_complexity = None
        self._memory_complexity = None
        self._verbose_information = None

    def set_parameter_ranges(self, parameter: str, min_value: float, max_value: float):
        """Set range of specific parameter.
    
        If optimal parameter is already set, it must fall in that range.
    
        Args:
            parameter (str): Name of parameter to set
            min_value (float): Lowerbound for parameter (inclusive)
            max_value (float): Upperbound for parameter (inclusive)
        """
        if parameter not in self.parameter_names():
            raise IndexError(
                parameter + " is no valid parameter for " + str(self))
        if min_value > max_value:
            raise ValueError("minValue must be smaller or equal to maxValue")
        if parameter in self._optimal_parameters:
            if not (min_value <= self._optimal_parameters[parameter] <= max_value):
                raise ValueError("current optimal parameter does not fall in this range,"
                                 " reset optimal parameters or choose a different range")

        self._parameter_ranges[parameter]["min"] = min_value
        self._parameter_ranges[parameter]["max"] = max_value

    def _do_valid_parameters_in_current_ranges_exist(self):
        if any(i not in self._optimal_parameters.keys() for i in self.parameter_names()):
            return False
        return True

    def _compute_time_complexity(self, parameters: dict):
        """Compute and return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        raise NotImplementedError

    def _compute_memory_complexity(self, parameters: dict):
        """Compute and return the memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        raise NotImplementedError

    def _compute_tilde_o_time_complexity(self, parameters):
        """Compute and return the tilde-O time complexity of the algorithm.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        raise NotImplementedError

    def _compute_tilde_o_memory_complexity(self, parameters):
        """Compute and return the tilde-O memory complexity of the algorithm.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        raise NotImplementedError

    def _find_optimal_tilde_o_parameters(self):
        raise NotImplementedError

    def _get_optimal_parameter_methods_(self):
        """Return a list of methods decorated with @optimal_parameter ordered by linenumber of appearance."""

        def sort_operator(v):
            return v[1]

        import inspect

        def is_optimal_parameter_method(object):
            return inspect.ismethod(object) and hasattr(object, "__wrapped__")

        members = []
        for _, f in inspect.getmembers(self, predicate=is_optimal_parameter_method):
            _, start_line = inspect.getsourcelines(f)
            members.append([f, start_line])
        members.sort(key=sort_operator)

        return [f[0] for f in members]

    def _is_early_abort_possible(self, time_lower_bound: float):
        """Checks whether the current time lower bound is below the early exit limit."""
        if time_lower_bound > self._current_minimum_for_early_abort:
            return True
        return False

    def _find_optimal_parameters(self):
        """Enumerates all valid parameter configurations within the _parameter_ranges.
    
        Saves the best result (according to time complexity) in `_optimal_parameters`.
        """
        time = inf
        for params in self._valid_choices():
            tmp_time = self._compute_time_complexity(params)
            tmp_memory = self._compute_memory_complexity(params)
            if self.bit_complexities:
                tmp_memory = self.problem.to_bitcomplexity_memory(tmp_memory)

            tmp_time += self.memory_access_cost(tmp_memory)

            if tmp_time < time and tmp_memory <= self.problem.memory_bound:
                time, _ = tmp_time, tmp_memory
                self._current_minimum_for_early_abort = tmp_time
                for i in params:
                    self._optimal_parameters[i] = params[i]

            if self._time_complexity_is_convex and tmp_time > time:
                break
        self._current_minimum_for_early_abort = inf

    def _get_optimal_parameter(self, key: str):
        """Returns the optimal value for the parameter `key`.
    
        Either calculates the asymptotic optimization or for real instances. This
        function is meant for fetching optimization parameters which need to be
        optimized together.
        """
        if key not in self._optimal_parameters:
            if self.complexity_type == ComplexityType.ESTIMATE.value:
                self._call_all_preceeding_optimal_parameter_functions(key)
                self._find_optimal_parameters()
            elif self.complexity_type == ComplexityType.TILDEO.value:
                self._find_optimal_tilde_o_parameters()
            else:
                assert False

        return self._optimal_parameters.get(key)

    def get_optimal_parameters_dict(self):
        """Returns the optimal parameters dictionary."""
        return self._optimal_parameters

    def _fix_ranges_for_already_set_parameters(self):
        """Returns a new parameter rangers dictionary, which fixes already optimal parameters."""
        parameters = self._optimal_parameters
        ranges = self._parameter_ranges
        new_ranges = {i: ranges[i].copy() if i not in parameters else {"min": parameters[i], "max": parameters[i]}
                      for i in ranges}
        return new_ranges

    def _are_parameters_invalid(self, parameters: dict):
        """Specifies constraints on the parameters."""
        return False

    def _valid_choices(self):
        """Generator yielding new sets of valid parameters.
    
        Based on the `_parameter_ranges` and already set parameters in `_optimal_parameters`.
        """
        new_ranges = self._fix_ranges_for_already_set_parameters()
        indices = {i: new_ranges[i]["min"] for i in new_ranges}
        keys = [i for i in indices]
        stop = False
        while not stop:
            if not self._are_parameters_invalid(indices):
                yield indices
            indices[next(iter(indices))] += 1
            for i in range(len(keys)):
                if indices[keys[i]] > new_ranges[keys[i]]["max"]:
                    indices[keys[i]] = new_ranges[keys[i]]["min"]
                    if i != len(keys) - 1:
                        indices[keys[i + 1]] += 1
                    else:
                        stop = True
                else:
                    break

    def __set_dict(self, **kwargs):
        """Returns a dictionary of parameters whose values are all either optimized or they are all specified in kwargs."""
        params = dict()
        if kwargs != {}:
            missing_parameters = [
                x for x in self.parameter_names() if x not in list(kwargs.keys())]
            if missing_parameters:
                raise ValueError(
                    f"values for the parameters in the list {missing_parameters} must be provided")
            else:
                for i in self.parameter_names():
                    params[i] = kwargs.get(i)
        else:
            params = self.optimal_parameters()
        return params

    def set_parameters(self, parameters: dict):
        """Set optimal parameters to predifined values.
    
        Args:
            parameters (dict): Dictionary including parameters to set (for a subset of optimal_parameters functions)
        """
        save_complexity_type = self.complexity_type
        self.reset()
        self.complexity_type = save_complexity_type

        s = self._optimal_parameters_methods
        for i in parameters.keys():
            if str(i) not in [j.__name__ for j in s]:
                raise ValueError(
                    i + " is not a valid parameter for " + str(self))
            self._parameter_ranges[i]["max"] = max(
                parameters[i], self._parameter_ranges[i]["max"])
            self._parameter_ranges[i]["min"] = min(
                parameters[i], self._parameter_ranges[i]["min"])

            self._optimal_parameters[i] = parameters[i]

        self._memory_complexity = None
        self._time_complexity = None

    def _compute_estimate_time_complexity(self, params):
        """Computes time complexity in estimate mode and converts to bit complexity.
    
        Computes time complexity (in estimate mode) for given parameter set and converts to bit complexity
        and adds memory access costs if set.
        """
        temp_time_complexity = self._compute_time_complexity(params)
        if self.bit_complexities:
            temp_basic_operation_cost = self.problem.to_bitcomplexity_time(
                temp_time_complexity)

            if self._memory_access != 0:
                temp_memory_access_cost = temp_time_complexity
                temp_memory_access_cost += self.memory_access_cost(
                    self.memory_complexity())
                temp_time_complexity = log2(int(2 ** temp_basic_operation_cost)
                                            + int(2 ** temp_memory_access_cost))
            else:
                temp_time_complexity = temp_basic_operation_cost

        return temp_time_complexity

    def time_complexity(self, **kwargs):
        """Return the time complexity of the algorithm.
    
        Args:
            **kwargs: Arbitrary keyword arguments.
                optimal_parameters: If for each optimal parameter of the algorithm
                    a value is provided, the computation is done based on those
                    parameters.
        """
        if kwargs == {}:
            if self._time_complexity is not None:
                return self._time_complexity
            else:
                params = self.optimal_parameters()
                if not self._do_valid_parameters_in_current_ranges_exist():
                    self._time_complexity = inf
                    self._memory_complexity = inf
                    return inf
        else:
            params = self.__set_dict(**kwargs)

        if self._complexity_type == ComplexityType.ESTIMATE.value:
            temp_time_complexity = self._compute_estimate_time_complexity(params)
        else:
            temp_time_complexity = self._compute_tilde_o_time_complexity(params)

        if kwargs == {}:
            self._time_complexity = temp_time_complexity
        return temp_time_complexity

    def memory_complexity(self, **kwargs):
        """Return the memory complexity of the algorithm.
    
        Args:
            **kwargs: Arbitrary keyword arguments.
                optimal_parameters: If for each optimal parameter of the algorithm
                    a value is provided, the computation is done based on those
                    parameters.
        """
        if kwargs == {}:
            if self._memory_complexity is not None:
                return self._memory_complexity
            else:
                params = self.optimal_parameters()
                if not self._do_valid_parameters_in_current_ranges_exist():
                    self._time_complexity = inf
                    self._memory_complexity = inf
                    return inf

        else:
            params = self.__set_dict(**kwargs)

        if self._complexity_type == ComplexityType.ESTIMATE.value:
            temp_memory_complexity = self._compute_memory_complexity(params)
            if self.bit_complexities:
                temp_memory_complexity = self.problem.to_bitcomplexity_memory(
                    temp_memory_complexity)
        else:
            temp_memory_complexity = self._compute_tilde_o_memory_complexity(
                params)
        if kwargs == {}:
            self._memory_complexity = temp_memory_complexity
        return temp_memory_complexity

    def optimal_parameters(self):
        """Return a dictionary of optimal parameters.

        Tests:
            >>> from cryptographic_estimators import BaseAlgorithm, BaseProblem
            >>> BaseAlgorithm(BaseProblem()).optimal_parameters()
            {}
        """
        if self.has_optimal_parameter():
            for f in self._optimal_parameters_methods:
                _ = f()
        return self._optimal_parameters

    def _call_all_preceeding_optimal_parameter_functions(self, key: str):
        """Call the decorator function for each parameter, if they are optimal."""

        if self.has_optimal_parameter():
            for f in self._optimal_parameters_methods:
                if f.__name__ == key:
                    break
                _ = f()

    def has_optimal_parameter(self):
        """Return `True` if the algorithm has optimal parameter.

        Tests:
            >>> from cryptographic_estimators import BaseAlgorithm, BaseProblem
            >>> BaseAlgorithm(BaseProblem()).has_optimal_parameter()
            False
        """
        return len(self._optimal_parameters_methods) > 0

    def parameter_names(self):
        """Return the list with the names of the algorithm's parameters.

        Tests:
            >>> from cryptographic_estimators import BaseAlgorithm, BaseProblem
            >>> BaseAlgorithm(BaseProblem()).parameter_names()
            []
        """
        parameter_method_names = []
        if self.has_optimal_parameter():
            parameter_method_names = [
                i.__name__ for i in self._optimal_parameters_methods]
        return parameter_method_names
    def __repr__(self):
        return f"{self._name} estimator for the " + str(self.problem)

def optimal_parameter(func):
    """Decorator to indicate optimization parameter in BaseAlgorithm.

    Args:
        func: A method of a BaseAlgoritm subclass.
    """

    @functools.wraps(func)
    def optimal_parameter(*args, **kwargs):
        name = func.__name__
        self = args[0]
        if name not in self._optimal_parameters:
            temp = func(*args, **kwargs)
            if temp is not None:
                self._optimal_parameters[name] = temp
        return self._optimal_parameters.get(name)

    return optimal_parameter
