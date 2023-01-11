from .helper import concat_all_tables, round_or_truncate, ComplexityType
from prettytable import PrettyTable
from math import inf, isinf
from sage.all import *
from .base_constants import *

class BaseEstimator(object):
    """
    Construct an instance of BaseEstimator

    INPUT:

    - ``alg`` -- specialized algorithm class (subclass of BaseAlgorithm)
    - ``prob`` -- object of any subclass of BaseProblem
    - ``excluded_algorithms`` -- a list/tuple of excluded algorithms (default: None)
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
    - ``complexity_type`` -- complexity type to consider (0: estimate, 1: tilde O complexity, default 0)
    - ``bit_complexities`` -- state complexity as bit rather than field operations (default 1, only relevant for complexity_type 0)
    - ``include_tildeo`` -- specifies if tildeO estimation should be included in the outputs (default 0: no tildeO esimation)
    - ``include_quantum`` -- specifies if quantum estimation should be included in the outputs (default 0: no quyantum esimation)

    """
    excluded_algorithms_by_default = []

    def __init__(self, alg, prob, **kwargs):

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
        """
        Returns a list of memory_access attributes of included algorithms

        """
        return [i.memory_access for i in self._algorithms]

    @memory_access.setter
    def memory_access(self, new_memory_access):
        """
        Sets the memory_access attribute of all included algorithms

        """
        for i in self._algorithms:
            i.memory_access = new_memory_access

    @property
    def complexity_type(self):
        """
        Returns a list of complexity_type attributes of included algorithms

        """
        return [i.complexity_type for i in self._algorithms]

    @complexity_type.setter
    def complexity_type(self, new_complexity_type):
        """
        Sets the complexity_type attribute of all included algorithms

        """
        for i in self._algorithms:
            i.complexity_type = new_complexity_type

    @property
    def bit_complexities(self):
        """
        Returns a list of bit_complexities attributes of included algorithms

        """
        return [i.bit_complexities for i in self._algorithms]

    @bit_complexities.setter
    def bit_complexities(self, new_bit_complexities):
        """
        Sets the bit_complexities attribute of all included algorithms

        """
        if self._bit_complexities != new_bit_complexities:
            self._bit_complexities = new_bit_complexities
            self.reset()
            for i in self._algorithms:
                i.bit_complexities = new_bit_complexities

    def algorithms(self):
        """
        Return a list of considered algorithms

        """
        return self._algorithms

    def algorithm_names(self):
        """
        Return a list of the name of considered algorithms

        """
        return [algorithm.__class__.__name__ for algorithm in self.algorithms()]

    def nalgorithms(self):
        """
        Return the number of considered algorithms

        """
        return len(self.algorithms())

    def _add_tilde_o_complexity(self, algorithm):
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

    def _add_quantum_complexity(self, algorithm):
        est = self.estimates
        name = algorithm.__class__.__name__
        try:
            est[name][BASE_QUANTUMO] = {}
            est[name][BASE_QUANTUMO][BASE_TIME] = algorithm.quantum_time_complexity()
        except NotImplementedError:
            est[name][BASE_QUANTUMO][BASE_TIME] = "--"

    def _add_estimate(self, algorithm):
        est = self.estimates
        name = algorithm.__class__.__name__
        algorithm.complexity_type = ComplexityType.ESTIMATE.value
        est[name][BASE_ESTIMATEO] = {}

        est[name][BASE_ESTIMATEO][BASE_TIME] = algorithm.time_complexity() if not isinf(
            algorithm.time_complexity()) else '--'
        est[name][BASE_ESTIMATEO][BASE_MEMORY] = algorithm.memory_complexity() if not isinf(
            algorithm.memory_complexity()) else '--'

        est[name][BASE_ESTIMATEO][BASE_PARAMETERS] = algorithm.get_optimal_parameters_dict()
        est[name][BASE_ADDITIONALO] = algorithm._get_verbose_information()

    def estimate(self, **kwargs):
        """
        Returns dictionary describing the complexity of each algorithm and its optimal parameters

        """
        logger = kwargs.get("logger", None)

        if not self.estimates:
            self.estimates = dict()
        for index, algorithm in enumerate(self.algorithms()):
            name = algorithm.__class__.__name__
            if name not in self.estimates:
                self.estimates[name] = {}

            # used only in the GUI
            if logger:
                logger(f"[{str(index + 1)}/{str(self.nalgorithms())}] - Processing algorithm: '{name}'")

            if self.include_tildeo and BASE_TILDEO_ESTIMATE not in self.estimates[name]:
                self._add_tilde_o_complexity(algorithm)

            if self.include_quantum and BASE_QUANTUMO not in self.estimates[name]:
                self._add_quantum_complexity(algorithm)

            if BASE_ESTIMATEO not in self.estimates[name]:
                self._add_estimate(algorithm)

        return self.estimates

    def _create_initial_table_containing_algorithm_column(self):
        tbl = PrettyTable([BASE_ALGORITHM])
        tbl.padding_width = 1
        tbl.title = ' '
        tbl.align[BASE_ALGORITHM] = "l"

        for i in self.estimates.keys():
            tbl.add_row([i])

        return tbl

    def _create_subtable_containing_all_columns(self, sub_table_name, show_all_parameters):
        key = list(self.estimates.keys())[0]
        table_columns = [i for i in list(self.estimates[key][sub_table_name].keys()) if
                         i != BASE_PARAMETERS or show_all_parameters]
        tbl = PrettyTable(table_columns, min_table_width=len(sub_table_name))
        tbl.padding_width = 1
        tbl.title = sub_table_name
        if BASE_TIME in table_columns:
            tbl.align[BASE_TIME] = "r"
        if BASE_MEMORY in table_columns:
            tbl.align[BASE_MEMORY] = "r"
        return tbl

    def _add_rows(self, tbl, truncate, precision):
        for i in self.estimates.keys():
            row = [self.estimates[i][tbl.title][k] for k in tbl.field_names]
            row = [round_or_truncate(i, truncate, precision)
                   if i in RR else i for i in row]
            tbl.add_row(row)
        return tbl

    def table(self, show_quantum_complexity=0, show_tilde_o_time=0, show_all_parameters=0, precision=1, truncate=0):
        """
        Print table describing the complexity of each algorithm and its optimal parameters

        INPUT:

        - ``show_quantum_complexity`` -- show quantum time complexity (default: false)
        - ``show_tilde_o_time`` -- show Ō time complexity (default: false)
        - ``show_all_parameters`` -- show all optimization parameters (default: false)
        - ``precision`` -- number of decimal digits output (default: 1)
        - ``truncate`` -- truncate rather than round the output (default: false)

        """

        self.include_tildeo = show_tilde_o_time
        self.include_quantum = show_quantum_complexity
        est = self.estimate()

        if est is None:
            print("No algorithms associated with this estimator.")
        key = list(est.keys())[0]
        tables = []
        tbl = self._create_initial_table_containing_algorithm_column()
        tables.append(tbl)

        for j in est[key].keys().__reversed__():
            if j == BASE_QUANTUMO and not show_quantum_complexity:
                continue
            if j == BASE_TILDEO_ESTIMATE and not show_tilde_o_time:
                continue
            if j == BASE_ADDITIONALO:
                continue

            tbl = self._create_subtable_containing_all_columns(
                j, show_all_parameters)
            self._add_rows(tbl, truncate, precision)
            tables.append(tbl)

            if j == BASE_QUANTUMO:
                tbl._min_width = {BASE_TIME: len(BASE_QUANTUMO)}

        tbl_join = concat_all_tables(tables)

        print(tbl_join)

    def fastest_algorithm(self, use_tilde_o_time=False):
        """
         Return the algorithm with the smallest time complexity

         INPUT:

         - ``use_tilde_o_time`` -- use Ō time complexity, i.e., ignore polynomial factors (default: False)
         """
        if use_tilde_o_time:
            self.complexity_type = ComplexityType.TILDEO.value

        def key(algorithm): return algorithm.time_complexity()
        return min(self.algorithms(), key=key)

    def reset(self):
        """
        Resets the internal states of the estimator and all included algorithms

        """

        self.estimates = {}
        for i in self.algorithms():
            i.reset()
