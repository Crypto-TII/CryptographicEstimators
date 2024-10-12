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


from math import isinf, inf
from typing import Union, Callable
from .helper import ComplexityType
from .base_constants import BASE_TILDEO_ESTIMATE, BASE_ADDITIONALO, BASE_BIT_COMPLEXITIES, BASE_ESTIMATEO, BASE_EXCLUDED_ALGORITHMS, BASE_MEMORY, BASE_PARAMETERS, BASE_QUANTUMO, BASE_TIME, BASE_ESTIMATOR_TYPE
from .base_algorithm import BaseAlgorithm
from .estimation_renderer import EstimationRenderer


class BaseEstimator(object):
    excluded_algorithms_by_default = []
    def __init__(self, alg, prob, **kwargs):
        """Construct an instance of BaseEstimator.

        Args:
            alg: Specialized algorithm class (subclass of BaseAlgorithm).
            prob: Object of any subclass of BaseProblem.
            **kwargs: Additional keyword arguments.
                excluded_algorithms (list or tuple): A list/tuple of excluded algorithms. Default: None.
                memory_access (int): Specifies the memory access cost model. Default: 0.
                    Choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root
                    or deploy custom function which takes as input the logarithm of the total memory usage.
                complexity_type (int): Complexity type to consider. Default: 0.
                    0: estimate, 1: tilde O complexity.
                bit_complexities (int): State complexity as bit rather than field operations. Default: 1.
                    Only relevant for complexity_type 0.
                include_tildeo (int): Specifies if tildeO estimation should be included in the outputs. Default: 0.
                    0: no tildeO estimation.
                include_quantum (int): Specifies if quantum estimation should be included in the outputs. Default: 0.
                    0: no quantum estimation.
        """

        excluded_algorithms = kwargs.get(BASE_EXCLUDED_ALGORITHMS, tuple())
        if excluded_algorithms:
            if any(not issubclass(Algorithm, alg) for Algorithm in excluded_algorithms):
                raise TypeError(
                    f"all excluded algorithms must be a subclass of {alg.__name__}")
            del kwargs[BASE_EXCLUDED_ALGORITHMS]

        self._algorithms = []
        self.estimates = {}

        self.problem = prob
        self._bit_complexities = kwargs.get(BASE_BIT_COMPLEXITIES, 1)
        self.bit_complexities = self._bit_complexities
        self.include_tildeo = kwargs.get("include_tildeo", False)
        self.include_quantum = kwargs.get("include_quantum", False)
        self._estimator_type = BASE_ESTIMATOR_TYPE

        included_algorithms = (Algorithm for Algorithm in alg.__subclasses__(
        ) if Algorithm not in excluded_algorithms)

        for Algorithm in included_algorithms:
            try:
                algorithm = Algorithm(prob, **kwargs)
            except (ValueError, TypeError):
                continue

            self._algorithms.append(algorithm)

            setattr(self, algorithm.__module__.split('.')[-1], algorithm)

    @property
    def memory_access(self):
        """Returns a list of memory_access attributes of included algorithms."""
        return [i.memory_access for i in self._algorithms]

    @memory_access.setter
    def memory_access(self, new_memory_access: Union[int, Callable[[float], float]]):
        """Sets the memory_access attribute of all included algorithms.
    
        Args:
            new_memory_access (Union[int, Callable[[float], float]]): New memory access value. Either
                (0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom
                function which takes as input the logarithm of the total memory usage)
        """
        for i in self._algorithms:
            i.memory_access = new_memory_access

    @property
    def complexity_type(self):
        """Returns a list of complexity_type attributes of included algorithms."""
        return [i.complexity_type for i in self._algorithms]

    @complexity_type.setter
    def complexity_type(self, new_complexity_type: ComplexityType):
        """Sets the complexity_type attribute of all included algorithms.
    
        Args:
            new_complexity_type (ComplexityType): New complexity_type value. Either (0: estimate, 1: tilde O complexity)
        """
        for i in self._algorithms:
            i.complexity_type = new_complexity_type

    @property
    def bit_complexities(self):
        """Returns a list of bit_complexities attributes of included algorithms."""
        return [i.bit_complexities for i in self._algorithms]

    @bit_complexities.setter
    def bit_complexities(self, new_bit_complexities: int):
        """Sets the bit_complexities attribute of all included algorithms.
    
        Args:
            new_bit_complexities (int): New bit_complexities value.
        """
        if self._bit_complexities != new_bit_complexities:
            self._bit_complexities = new_bit_complexities
            self.reset()
            for i in self._algorithms:
                i.bit_complexities = new_bit_complexities

    @property
    def estimator_type(self):
        """Returns the type of the estimator.
    
        Either problem or scheme
        """
        return self._estimator_type

    def algorithms(self):
        """Return a list of considered algorithms."""
        return self._algorithms

    def algorithm_names(self):
        """Return a list of the name of considered algorithms."""
        return [algorithm.__class__.__name__ for algorithm in self.algorithms()]

    def nalgorithms(self):
        """Return the number of considered algorithms."""
        return len(self.algorithms())

    def _add_tilde_o_complexity(self, algorithm: BaseAlgorithm):
        """Runs the tilde O complexity analysis for the given algorithm.
    
        Args:
            algorithm (BaseAlgorithm): Algorithm to run.
        """
        est = self.estimates
        name = algorithm.__class__.__name__
        algorithm.complexity_type = ComplexityType.TILDEO.value
        est[name][BASE_TILDEO_ESTIMATE] = {}

        try:
            est[name][BASE_TILDEO_ESTIMATE][BASE_TIME] = algorithm.time_complexity()
        except NotImplementedError:
            est[name][BASE_TILDEO_ESTIMATE][BASE_TIME] = "--"
        try:
            est[name][BASE_TILDEO_ESTIMATE][BASE_MEMORY] = algorithm.memory_complexity()
        except NotImplementedError:
            est[name][BASE_TILDEO_ESTIMATE][BASE_MEMORY] = "--"
        try:
            est[name][BASE_TILDEO_ESTIMATE][BASE_PARAMETERS] = algorithm.get_optimal_parameters_dict()
        except NotImplementedError:
            est[name][BASE_TILDEO_ESTIMATE][BASE_PARAMETERS] = "--"

    def _add_quantum_complexity(self, algorithm: BaseAlgorithm):
        """Runs the quantum time analysis for the given algorithm.
    
        Args:
            algorithm (BaseAlgorithm): Algorithm to run.
        """
        est = self.estimates
        name = algorithm.__class__.__name__
        try:
            est[name][BASE_QUANTUMO] = {}
            est[name][BASE_QUANTUMO][BASE_TIME] = algorithm.quantum_time_complexity()
        except NotImplementedError:
            est[name][BASE_QUANTUMO][BASE_TIME] = "--"

    def _add_estimate(self, algorithm: BaseAlgorithm):
        """Runs the bit security analysis for the given algorithm.
    
        Args:
            algorithm (BaseAlgorithm): Algorithm to run.
        """
        est = self.estimates
        name = algorithm.__class__.__name__
        algorithm.complexity_type = ComplexityType.ESTIMATE.value
        est[name][BASE_ESTIMATEO] = {}
        
        time = algorithm.time_complexity()
        est[name][BASE_ESTIMATEO][BASE_TIME] = time if (time is not None and not isinf(
            time)) else '--'

        memory = algorithm.memory_complexity()
        est[name][BASE_ESTIMATEO][BASE_MEMORY] = memory if (memory is not None and not isinf(
            memory)) else '--'

        est[name][BASE_ESTIMATEO][BASE_PARAMETERS] = algorithm.get_optimal_parameters_dict()

        est[name][BASE_ADDITIONALO] = algorithm._get_verbose_information() if (time is not None and not isinf(time)) else {}

    def estimate(self, **kwargs):
        """Returns dictionary describing the complexity of each algorithm and its optimal parameters."""
        logger = kwargs.get("logger", None)

        if not self.estimates:
            self.estimates = dict()
        for index, algorithm in enumerate(self.algorithms()):
            name = algorithm.__class__.__name__
            if name not in self.estimates:
                self.estimates[name] = {}

            # used only in the GUI
            if logger:
                logger(
                    f"[{str(index + 1)}/{str(self.nalgorithms())}] - Processing algorithm: '{name}'")

            if self.include_tildeo and BASE_TILDEO_ESTIMATE not in self.estimates[name]:
                self._add_tilde_o_complexity(algorithm)

            if self.include_quantum and BASE_QUANTUMO not in self.estimates[name]:
                self._add_quantum_complexity(algorithm)

            if BASE_ESTIMATEO not in self.estimates[name]:
                self._add_estimate(algorithm)

            if self.estimator_type != BASE_ESTIMATOR_TYPE:
                if "attack_type" not in self.estimates[name]:
                    self.estimates[name][" "] ={}
                    self.estimates[name][" "]["attack_type"] = algorithm.attack_type
        return self.estimates

    def table(self, show_quantum_complexity=False, show_tilde_o_time=False, show_all_parameters=False, precision=1, truncate=False):
        """Print table describing the complexity of each algorithm and its optimal parameters.
    
        Args:
            show_quantum_complexity (bool): Show quantum time complexity. Defaults to False.
            show_tilde_o_time (bool): Show Ō time complexity. Defaults to False.
            show_all_parameters (bool): Show all optimization parameters. Defaults to False.
            precision (int): Number of decimal digits output. Defaults to 1.
            truncate (bool): Truncate rather than round the output. Defaults to False.
        """
        self.include_tildeo = show_tilde_o_time
        self.include_quantum = show_quantum_complexity
        if all(self.complexity_type):
            self.include_tildeo = show_tilde_o_time = True

        estimate = self.estimate()

        if estimate == {}:
            raise ValueError(
                "No algorithm associated with this estimator or applicable to this problem instance.")

        else:
            renderer = EstimationRenderer(
                show_quantum_complexity, show_tilde_o_time, show_all_parameters, precision, truncate
            )

            return renderer.as_table(estimate)

    def fastest_algorithm(self, use_tilde_o_time=False):
        """Return the algorithm with the smallest time complexity.
    
        Args:
            use_tilde_o_time (bool): Use Ō time complexity, i.e., ignore polynomial factors. Default is False.
        """
        if use_tilde_o_time:
            self.complexity_type = ComplexityType.TILDEO.value

        def key(algorithm):
            try:
                return algorithm.time_complexity()
            except NotImplementedError:
                return inf

        return min(self.algorithms(), key=key)

    def reset(self):
        """Resets the internal states of the estimator and all included algorithms."""
        self.estimates = {}
        for i in self.algorithms():
            i.reset()
