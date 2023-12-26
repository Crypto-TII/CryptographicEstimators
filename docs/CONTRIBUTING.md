# General Things:
Use python syntax/features. If sage features are necessary, import them via import statements

## GIT Conventions
### Commits
To contribute to this project please follow this subset of [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/). These are some examples
Type
Must be one of the following:
- docs: Documentation only changes
- feat: A new feature
- fix: A bug fix
- refactor: A code change that neither fixes a bug nor adds a feature

### Branching

Branch names should be snake_case. Which means that all the text must be lowercase and replace spaces with dashes. Also,
we should add as a prefix based on the type of implementation. For example:
```
refactor/modify_base_problem
feature/implement_dummy_estimator
fix/algorithm_parameter
```

### Pull request
1. Only create pull requests to the `develop` branch.
2. Fulfill the template

---
# Adding a new estimator
This tutorial shows how to add your own estimator to the CryptographicEstimators library. For this we implement a simple
`DummyEstimator`.

First make sure that you have a working `python` and `sage` instance on your current machine and have correctly
[setup](https://github.com/Crypto-TII/CryptographicEstimators#installation-) the project. In the following we assume 
that you are in the root directory of the project.

The next step adds all needed files for the `DummyEstimator` to the repository
via the command:
```bash 
>>> make add-estimator
```

The script asks you for some basic properties of the new estimator, e.g. its name:
```
Enter a prefix for your Estimator (For example for SyndromeDecoding you could use SD): Dummy
# Creating folders...
# Creating files...
# Creating init files...
# Done! You can now start by editing the files inside 'CryptographicEstimators/cryptographic_estimators/DUMMYEstimator' and the input_dictionary
cryptographic_estimators
├── DUMMYEstimator
│   └── DUMMYAlgorithms
├── LEEstimator
│   └── LEAlgorithms
├── MQEstimator
│   ├── MQAlgorithms
│   └── series
├── PEEstimator
│   └── PEAlgorithms
├── PKEstimator
│   └── PKAlgorithms
├── SDEstimator
│   ├── SDAlgorithms
│   └── SDWorkfactorModels
└── SDFqEstimator
    └── SDFqAlgorithms
```

In this case we choose the name `Dummy`, note that the script automatically 
replaces everything with capital letters. To see which files and folders were
added run:
```bash
>>> tree cryptographic_estimators/DUMMYEstimator
cryptographic_estimators/DUMMYEstimator
├── dummy_algorithm.py
├── DUMMYAlgorithms
│   ├── dummy_algorithm1.py
│   └── __init__.py
├── dummy_constants.py
├── dummy_estimator.py
├── dummy_problem.py
└── __init__.py
```

As one can see, the script generated the three main classes, each in one file, 
`dummy_problem.py`, `dummy_estimator.py` and `dummy_algorithm.py`. Each estimator
of the CryptographicEstimators project needs those to be functioning. So they 
are mandatory. Aditionally, the script added one `dummy_algorithm1.py` file,
which acts like the first algorithm we want to implement.

Note that the script already added all needed links to other files in their
corresponding `__init__.py` files.

Now we need to make the added classes visible to the whole project by simply adding 
```python
from . import DUMMYEstimator
```
to `cryptographic_estimators/__init__.py`. 

Finally we are ready to run our estimator for the first time, create
a `test.py` file, containing:
```python
from cryptographic_estimators.DUMMYEstimator import *
A = DUMMYEstimator()
A.table()
```
and execute it via `sage test.py`. You should see the following output:
```bash
>>> sage test.py
+-----------------+---------------+
|                 |    estimate   |
+-----------------+------+--------+
| algorithm       | time | memory |
+-----------------+------+--------+
| DUMMYAlgorithm1 |   -- |     -- |
+-----------------+------+--------+
```
If for any reason your output doesn't look like this, make sure that you correctly
installed [sage](https://doc.sagemath.org/html/en/installation/index.html),
[python](https://www.python.org/downloads/) and this library via `make install`.

For now, our new estimator is not estimating much. That's because we did neither
describe the problem at hand nor specify the algorithm `DUMMYAlgorithm1`.

A full estimator implementation includes the following three important classes:
  - DUMMYProblem 
  - DUMMYAlgorithm
  - DUMMYEstimator

The first describes the problem at hand, whereas the second computes the complexity of solving it via certain algorithms.
And `DUMMYEstimator` acts like a manager class, putting all together.

Let's introduce a complexity parameter `n` to our problem. Therefore, change the 
constructor of `DUMMYProblem` to 
```python
def __init__(self, n: int, **kwargs):
    super().__init__(**kwargs)
    self.parameters["n"] = n
```
and `DUMMYEstimator` to 
```python
def __init__(self, n: int, memory_bound=inf, **kwargs):
    super(DUMMYEstimator, self).__init__(
        DUMMYAlgorithm,
        DUMMYProblem(n, memory_bound=memory_bound, **kwargs),
        **kwargs
    )
```
to include the parameter `n`. Of course, you can add as many parameters as needed,
only make sure that the estimator passes them correctly to the problem class.

As you can see, in both cases the `DUMMYProblem` and `DUMMYEstimator` need 
to call the constructor of their super class, this is mandatory to inherit all
needed functions and fields for the estimation process.

For the next step we must make sure that the algorithm `DummyAlgorihm1` is 
actually computing something. For this add the following two functions to 
the file `dummy_algorihm1.py`:

```python
def _compute_time_complexity(self, parameters: dict, verbose_information=None):
    """
    Return time complexity of DUMMYAlgorithm1's  for given set of parameters
    
    INPUT:
    -  ``parameters`` -- dictionary including parameters
    -  ``verbose_information`` -- 
    """
    n = self.problem.parameters["n"]
    return n

def _compute_memory_complexity(self, parameters: dict, verbose_information=None):
    """
    Return memory complexity of DUMMYAlgorithm1's  for given set of parameters

    INPUT:
    -  ``parameters`` -- dictionary including parameters
    -  ``verbose_information`` -- 
    """
    return 0
```

The first function returns the time complexity (`n`), whereas the second function returns the memory complexity (`0`).
Thus, this is the estimation of a brute force algorithm.

You may ask what's the purpose of the function parameter `verbose_information`? More on this in a later
[chapter](#Adding-verbose-information). 

In the following we make the distinction between `problem parameter` and `optimization parameters`. The first one are
provided by the user, are not changed by the optimization process and fully describe the problem at hand. Whereas the 
`optimization parameters` are, as the name suggests, optimized by the CryptographicEstimators library to find an 
optimal one.

An important thing to recognize here is, that the two functions only compute the complexity of the algorithm for a
given set of optimization parameters. These function do *not* iterate over a set of optimization parameters, nor they try
to improve upon the given parameters in any way. They are only computing the complexity based on the given parameters. 
Note that the current definition of the time complexity does not use any optimization parameters. To see how to make use 
of optimization parameters see [of how to add an optimization parameter](#Adding-an-optimization-parameter)

Now let us call the `DUMMYEstimator` via the `test.py` script with parameter `n=100`, i.e.,

```python
from cryptographic_estimators.DUMMYEstimator import *
A = DUMMYEstimator(n=100)
A.table()
```
will show:
```bash 
+-----------------+----------------+
|                 |    estimate    |
+-----------------+-------+--------+
| algorithm       |  time | memory |
+-----------------+-------+--------+
| DUMMYAlgorithm1 | 100.0 |   0.0  |
+-----------------+-------+--------+
```
Congratulations, this is your first successful complexity estimation in the 
CryptographicEstimators framework.

A few notes on what you see: 

The values the two functions return are in logarithmic scale, meaning the output `n` of the estimation implies that running `DUMMYAlgorithm1`
to solve the `DUMMYPRoblem` would require `2**n` *basic operations*. Where's `basic operation` is the minimal operation to count by the estimator. This *basic operation*
has to be specified for each estimator and every algorithm inside the estimator uses this same unit for measuring time complexity.
The `basic operation` can for example be bit additions, vector additions, field multiplications or matrix multiplications. To be able to 
compare estimations under different basic operations, the CryptographicEstimators framework provides a unified way to
convert those into bit operations, which we detail in the next section.

The same holds for the memory consumption, which is in the amount of `basic elements` the algorithm needs to store. 
Those basic elements may be binary or F_q vectors of certain length or integers of certain bitsize. Again, the 
CryptographicEstimators framework provides a unified way to convert those into bits. More on this topic in the next  chapter. 

The two functions `_compute_time_complexity(...)` and `_compute_memory_complexity(...)` are automatically called by the
framework to compute the time and memory complexity for a given parameter set. The framework will iterate over a certain
amount of different optimization parameter sets until it cannot reduce the (time/memory) complexity further. The minimum
is then shown in such a table. More on this in chapter [of how to add an optimization parameter](#Adding-an-optimization-parameter)


# Translation between different types of measurements
The complexity of an algorithm is sometimes not measured in bit operations, but in vector operations or in matrix
operations. To convert between those measurements automatically, the CryptographicEstimators library offers an
easy-to-use API.

Notably the two functions `to_bitcomplexity_time` and `to_bitcomplexity_memory` which are implemented by the `Problem`
class of your estimation, in our case `DUMMYProblem`. These two functions are automatically called by the `BaseEstimator`
if implemented. They are therefore mandatory to implement. Note that the estimator generation script by default assumes
that the algorithm's `basic operation` is a bitoperation and that the `basic element` is a bit.

Let us assume our `DummyEstimator` estimates the complexity not in bit operations but in binary vector operations of
length `n` and correspondingly the `basic element` of the estimator are binary vectors of length `n`. To
convert to bit complexity we therefore change the two functions of the `DUMMYProblem` class to the following:

```python
def to_bitcomplexity_time(self, basic_operations: float):
    """
    Return the bit-complexity corresponding to a certain amount of basic_operations

    INPUT:

    - ``basic_operations`` -- Number of basic operations (logarithmic)

    """
    n = self.parameters["n"]
    return basic_operations + log2(n)

def to_bitcomplexity_memory(self, elements_to_store: float):
    """
    Return the memory bit-complexity associated to a given number of elements to store

    INPUT:

    - ``elements_to_store`` -- number of memory operations (logarithmic)

    """
    n = self.parameters["n"]
    return elements_to_store + log2(n)
```
See the `+ log2(n)` which converts in the case of `to_bitcomplexity_time(...)` the vector operations into bit operations.
The input parameter `basic_operations` as well as `elements_to_store` are always passed as a logarithm. This is the case for
(almost) all large values in the CryptographicEstimators, see [this chapter](#Always-compute-the-logarithm).

If we run our `test.py` script now, it will yield:
```bash
+-----------------+----------------------------+
|                 |          estimate          |
+-----------------+------+--------+------------+
| algorithm       | time | memory | parameters |
+-----------------+------+--------+------------+
| DUMMYAlgorithm1 | 56.6 |   56.6 | {'h': 50}  |
+-----------------+------+--------+------------+
```

# Adding an optimization parameter
The CryptographicEstimators framework allows to add arbitrary optimizations parameters that can be chosen (but also
restricted) freely. The framework automatically chooses them within the defined ranges and under the given restrictions
such that the runtime of the algorithm is minimized. 

Right now our `DUMMYAlgorithm1` represents a simple bruteforce algorithm, enumerating the whole search space, e.g. `2**n`
elements. We now want to extend this algorithm to perform a Meet-in-the-Middle (MITM) approach. Therefore, we 
introduce an optimization parameter `h`, which represents the number of elements to precompute for the MITM approach. If
`h=10`, we precompute `2**10` elements and save them in a lookup table. The algorithm can later look them up, without
recomputing them, hence the runtime is reduced to `max(2**{n-h}, 2**{h}) = 2**{90}` for our example (`n=100, h=10`).

A well-known example for such a MITM algorithm is the [Baby-Step Giant Step](https://en.wikipedia.org/wiki/Baby-step_giant-step) 
algorithm for solving the [discrete logarithm problem](https://en.wikipedia.org/wiki/Discrete_logarithm).

To implement this, let us add a new algorithm called `DUMMYAlgorithm2`. Therefor copy the `DUMMYALgorithm1` like:
```shell
cp cryptographic_estimators/DummyEstimator/DummyAlgorithms/dummy_algorithm1.py cryptographic_estimators/DummyEstimator/DummyAlgorithms/dummy_algorithm2.py 
```
and rename everything accordingly. To make the new algorithm visible to the framework add
```python
from .dummy_algorithm2 import DUMMYAlgorithm2
```
to `cryptographic_estimators/DUmmyEstimator/DummyAlgorithms/__init__.py`

And finally to add the parameter we need to inform our `DUMMYAlgorithm2` class about it, for this add the following functions
```python
@optimal_parameter
def h(self):
    return self._get_optimal_parameter("h")
```

The function represents a helper function to efficiently access the optimal parameter `h`, without the knowledge
of the internals of the full implementation of the class. The nice thing about the CryptographicEstimator framework is,
it will keep track of the optimal optimization parameters, and you are therefor able to access via:
```python
algo = DUMMYAlgorith2(DUMMYProblem(n=100))
algo.time_complexity()
optimal_h = algo._get_optimal_parameter(“h”)
```

Note the function decorator `optimal_parameter`, this is mandatory as it publishes the optimization parameter known to
the whole framework. It is defined in `base_algorithm.py`, thus you need to add 
```python
from ...base_algorithm import optimal_parameter
```
to have access to it.

If you encounter speed problems e.g. the estimation process takes to long, have a look to the following
[chapter](#Speeding-up-the-estimation-process).

And finally make sure to initialize all needed fields within the constructor:
```python
def __init__(self, problem: DUMMYProblem, **kwargs):
    self._name = "DUMMYAlgorithm2"
    super(DUMMYAlgorithm2, self).__init__(problem, **kwargs)
    n = self.problem.parameters["n"]
    self.set_parameter_ranges("h", 0, n)
```

This is done by adding the function call `self.set_parameter_ranges("h", 0, n)` to the constructor of `DummyAlgorihm2`.
This call sets the logical lower limit `0` (inclusive) and upper limit `n` (inclusive). 

If we now change our computations in the two functions `_compute_time__complexity` and `_compute_memory_complexity` 
in `DUMMYAlgorithm2` to:
```python
def _compute_time_complexity(self, parameters: dict, verbose_information=None):
    """
    Return time complexity of DUMMYAlgorithm2's  for given set of parameters

    INPUT:
    -  ``parameters`` -- dictionary including parameters
    -  ``verbose_information`` -- 
    """
    n = self.problem.parameters["n"]
    par = SimpleNamespace(**parameters)
    runtime = log2(2**par.h + 2**(n-par.h))
    return runtime

def _compute_memory_complexity(self, parameters: dict, verbose_information=None):
    """
    Return memory complexity of DUMMYAlgorithm2's  for given set of parameters
    
    INPUT:
    -  ``parameters`` -- dictionary including parameters
    -  ``verbose_information`` -- 
    """
    par = SimpleNamespace(**parameters)
    mem = par.h
    return mem
```

and running our `test.py` script, yields a successful computation of a MITM-approach:
```bash
+-----------------+----------------+
|                 |    estimate    |
+-----------------+-------+--------+
| algorithm       |  time | memory |
+-----------------+-------+--------+
| DUMMYAlgorithm1 | 100.0 |    0.0 |
| DUMMYAlgorithm2 |  51.0 |   50.0 |
+-----------------+-------+--------+
```

Note that the class `SimpleNamespace(...)` is used to elegantly access the algorithm parameters like `par.h`. But of
course you could also access the parameters via `h = parameters["h"]`. Additionally, see the runtime formula 
`runtime = log2(2**par.h + 2**(n-par.h))`. The CryptographicEstimators framework automatically balances the time and
memory of the algorithm, resulting in the numbers shown in the table.

### Different Types of Optimization Parameters
There are two ways of implementing optimization parameters. If a parameter has to be optimized in conjunction with other 
parameters, meaning it has to be set in dependence of the time complexity, you can use `opt_parameter_name = self._get_optimal_parameter(“<parameter name>”)`,
as in the example above. Note that this is usually the case.

On the other hand there might be parameters that can be optimized independently based on the input (problem) parameters
you can simply return that value. For example, if in our case `h=n/2` is always the best choice we could return `n/2`
instead. Note that in our case indeed `h=n/2` is optimal with respect to the time complexity. However, since the choice
of `h` also influences the memory complexity and the CryptographicEstimators allows to put constraints on the memory
consumption, [here](#Benchmarking-under-memory-constraints) or [in the User Guide](User_Guide.ipynb) , we decide here
to use the more flexible optimization method via the automatic parameter search.

It also should be mentioned that parameters that can be optimized independently have to appear first in the code and those 
that are optimized in conjunction come after.

After a successful optimization process the optimal parameters, which minimize the runtime are saved in
the algorithm class and can be received via:
```python
algo = DUMMYAlgorithm2(DUMMYProblem(n=100))
algo.time_complexity()
print(algo.get_optimal_parameters_dict())
```

# Advanced Topics:
## Benchmarking under memory constrains
Good news: you do not have to do anything. It works right out of the box via the `memory_bound` argument. So changing
the `test.py` file to `A = DUMMYEstimator(n=100, memory_bound=20)` yields:
```bash
+-----------------+----------------------------+
|                 |          estimate          |
+-----------------+------+--------+------------+
| algorithm       | time | memory | parameters |
+-----------------+------+--------+------------+
| DUMMYAlgorithm1 | 80.0 |   20.0 | {'h': 20}  |
+-----------------+------+--------+------------+
```
For more information have a look to the [user guide](User_Guide.ipynb)


## Adding verbose information

The CryptographicEstimators framework allows to retrieve additional information about the algorithms and there optimization.
This includes for example the possibility to display all internal optimization parameters, such as `h` in case of our MITM algorithm. 
To display those you can use the `table` function with the argument `table(show_all_parameters=True)`, which results
in the following table:
```bash
+-----------------+----------------------------+
|                 |          estimate          |
+-----------------+------+--------+------------+
| algorithm       | time | memory | parameters |
+-----------------+------+--------+------------+
| DUMMYAlgorithm1 | 50.0 |   50.0 | {'h': 50}  |
+-----------------+------+--------+------------+
```
We refer to the [user guide](User_Guide.ipynb) for more information.


In case you want to make more information about a specific algorithm accessible you can use the `verbose_information` dictionary in the 
`_compute_time_complexity(..), _compute_memory_complexity(...)` functions. Such information could include information about internal 
states for the algorithm, as for example the sizes of used lists (or hashmaps).

To use it, you can change the `compute_time_complexity` function in `dummy_algorithm2.py` to the following:
```python
def _compute_time_complexity(self, parameters: dict, verbose_information=None):
    """
    Return time complexity of DUMMYAlgorithm2's  for given set of parameters

    INPUT:
    -  ``parameters`` -- dictionary including parameters
    -  ``verbose_information`` -- 
    """
    n = self.problem.parameters["n"]
    par = SimpleNamespace(**parameters)
    memory = par.h
    if verbose_information is not None:
        verbose_information["List Size"] = par.h
    runtime = max(memory, n - par.h)
    return runtime
```
Now you can read the verbose information via `_get_verbose_information()` function like:
```python
from cryptographic_estimators.DUMMYEstimator.DUMMYAlgorithms import DUMMYAlgorithm2
A = DUMMYAlgorithm2(DUMMYProblem(n=100))
print(A._get_verbose_information())
```

Note that you can use whatever you want as the dictionary key to save your additional data.

## Exclude Algorithms
Sometimes it might be useful to exclude certain algorithms from the estimation process, because their optimization takes 
a long time, or they are similar to other, included algorithms.

From the client perspective this can be easily achieved by adding `excluded_algorithms=[DUMMYAlgorithm1]` to the
estimator constructor:
```python
A = DUMMYEstimator(n=100, excluded_algorithms=[DUMMYAlgorithm1])
```
as shown in the [user guide](User_Guide.ipynb)


But sometimes it might be desirable that some algorithms are excluded by default from the estimation process. This can be
achieved by extending the constructor of `DUMMYEstimator` to:
```python
def __init__(self, n: int, memory_bound=inf, **kwargs):
    if not kwargs.get("excluded_algorithms"):
        kwargs["excluded_algorithms"] = []

    kwargs["excluded_algorithms"] += self.excluded_algorithms_by_default
    super(DUMMYEstimator, self).__init__(
        DUMMYAlgorithm,
        DUMMYProblem(n, memory_bound=memory_bound, **kwargs),
        **kwargs
    )
```
and add the algorithms to be ignored as a class variable to the `DUMMYEstimator` like this:
```python
class DUMMYEstimator(BaseEstimator):
    """
    Construct an instance of DUMMYEstimator

    INPUT:

    - ``excluded_algorithm`` -- A list/tuple of excluded algorithms (default: None)

    """
    excluded_algorithms_by_default = [DUMMYAlgorithm1]

    def __init__(self, n: int, memory_bound=inf, **kwargs):
        ...
```

## Unifying _compute_time_complexity and _compute_memory_complexity
Often computing the time complexity of an algorithm already requires computing its memory complexity. Thus,
to prevent code duplication you should introduce a function that returns both and call this function from the respective 
`_compute_time_complexity(...)` and `_compute_memory_complexity(...)` functions as shown in the following example:

```python
def _compute_time_memory_complexity(self, parameters: dict, verbose_information=None):
    """
    Return time and memory complexity of DUMMYAlgorithm1, for given set of parameters
    
    INPUT:
    -  ``parameters`` -- dictionary including parameters
    -  ``verbose_information`` -- 
    """
    # somehow compute TIME and MEMORY.
    return TIME, MEMORY

def _compute_time_complexity(self, parameters: dict, verbose_information=None):
    """
    Return time complexity of DUMMYAlgorithm1, for given set of parameters
    
    INPUT:
    -  ``parameters`` -- dictionary including parameters
    -  ``verbose_information`` -- 
    """
    time, _ = _compute_time_memory_complexity(parameters, verbose_information)
    return time

def _compute_memory_complexity(self, parameters: dict, verbose_information=None):
    """
    Return memory complexity of DUMMYAlgorithm, for given set of parameters

    INPUT:
    -  ``parameters`` -- dictionary including parameters
    -  ``verbose_information`` -- 
    """
    _, memory = _compute_time_memory_complexity(parameters, verbose_information)
    return memory
```

## Speeding up the estimation process
When the algorithms become more and more complex, an estimation process can last seconds and even minutes, which is 
highly undesirable. To speed things up, we list in this chapter a few tricks to improve the estimation speed.

### Limit the number of valid choices for an algorithm
Often it is known that certain parameters are invalid. To make this clear to the estimation process, one can overload
the `_are_paramters_invalid(self, parameters: dict)` function. This function takes a dictionary containing a
optimization parameter set, and returns false in case the parameter set is valid and true otherwise. 
Thus, if we want to enforce our simple MITM algorithm to only select even `h` we can add the following code to the
`DUMMYAlgorithm1` class:
```python
def _are_parameters_invalid(self, parameters: dict):
    if parameters["h"] % 2 != 0:
        return True
    return False
```
The CryptographicEstimators framework will automatically call this function and skip invalid optimization parameter
sets. Notice that this is an easy way to model basic dependencies between different optimization parameters, i.e. reject sets
with two contradicting optimizations parameters.

Sometimes this not enough, thus it can be desirable to fully replace the optimization parameter selection process with a
custom function to further speed things up. This can make sense if for example one parameter should be set in to 
specific values in dependence on another parameter. This can be achieved  by overloading the `_valid_choices(self)` function of
the algorithm class. In this example we want to restrict the MITM algorithm from the previous chapters to only chose
even `h`. 
```python
def _valid_choices(self) -> dict[str, int]:
    new_ranges = self._fix_ranges_for_already_set_parameters()
    for h in range(new_ranges["h"]["min"], new_ranges["h"]["max"], 2):
        yield {"h": h} 
```

For simplicity the function should be implemented as a [generator](https://wiki.python.org/moin/Generators), thus not
all valid parameter sets are saved in memory at the same time. Also, a dictionary including *all* optimization parameters must be
yielded, as otherwise the optimization process fails. Note that this function is implemented in the `BaseAlgorithm`
and there must be explicitly overloaded for each algorithm of your problem (where you want to have a customized parameter optimization).
Remember to always call the function `self._fix_ranges_for_already_set_parameters()` when overloading the `_valid_choices` function, which
ensures that parameters that have been fixed to certain values by the user are not re-optimized. 

### Always compute the logarithm
We strongly suggest to always compute the logarithm of (large) numbers and add/subtract instead of multiply/divide. Additionally,
if possible use the python integer division `a//b` over the float division `a/b` to further speed things up and to avoid float overlows. 
In general, it's a good idea to avoid the computations of big numbers. The same holds for the return values of functions, which 
should be always logarithmically (if not strictly needed otherwise).

# Writing Doctests
Throughout the CryptographicEstimators library we are using [sage doctests](https://doc.sagemath.org/html/en/developer/doctesting.html).
These tests are then automatically run by our [CI](https://github.com/Crypto-TII/CryptographicEstimators/actions) to check
for any errors.

We strongly encourage to write examples for all optimization parameters of an algorithm. In the case our
`DUMMYAlgorithm1` one could extend the optimization parameter `h` like this:
```python
@optimal_parameter
def h(self):
    """
    MITM parameter of our DUMMYAlgorithm 1 
    
    EXAMPLES::

        sage: from cryptographic_estimators.DummyEstimator.DummyAlgorithms import DUMMYAlgorithm1
        sage: from cryptographic_estimators.DummyEstimator import DUMMYProblem
        sage: A = DUMMYAlgorithm1(DUMMYProblem(n=100))
        sage: A.h()
        50
    
    """
    return self._get_optimal_parameter("h")
```
Note the newlines around `EXAMPLES::` and in the end. These are mandatory. Also note the commands the test framework is 
executing, are starting with `sage: ` and the expected result is written below the last command (`50`).

Additionally, it is mandatory to also test all algorithms at least once in the corresponding `Estimator` class. E.g. in
our case we extend the function `table()` of the `DUMMYEstimator` to
```python
def table(self, show_quantum_complexity=0, show_tilde_o_time=0,
          show_all_parameters=0, precision=1, truncate=0):
    """
    Print table describing the complexity of each algorithm and its optimal parameters

    INPUT:

    - ``show_quantum_complexity`` -- show quantum time complexity (default: False)
    - ``show_tilde_o_time`` -- show Ō time complexity (default: False)
    - ``show_all_parameters`` -- show all optimization parameters (default: False)
    - ``precision`` -- number of decimal digits output (default: 1)
    - ``truncate`` -- truncate rather than round the output (default: False)
   
    TESTS:

        sage: from cryptographic_estimators.DummyEstimator import DUMMYEstimator
        sage: A = DUMMYEstimator(n=100)
        sage: A.table()
        +-----------------+----------------------------+
        |                 |          estimate          |
        +-----------------+------+--------+------------+
        | algorithm       | time | memory | parameters |
        +-----------------+------+--------+------------+
        | DUMMYAlgorithm1 | 51.0 |   50.0 | {'h': 50}  |
        +-----------------+------+--------+------------+
        
        sage: from cryptographic_estimators.DummyEstimator import DUMMYEstimator
        sage: A = DUMMYEstimator(n=1000)
        sage: A.table() # long time 
        +-----------------+-----------------------------+
        |                 |           estimate          |
        +-----------------+-------+--------+------------+
        | algorithm       |  time | memory | parameters |
        +-----------------+-------+--------+------------+
        | DUMMYAlgorithm1 | 501.0 |  500.0 | {'h': 500} |
        +-----------------+-------+--------+------------+
        
    """
    ...
```
Again note the new lines around `TESTS:` and the end of the test. Additionally, notice the `# long test` at the end of
the last command. You can add this if the command takes a great amount of time, and you do not want to run the test to
run on every change you make, but rather only on every commit. Tests missing the `# long test` are always executed.
Make sure there is at least one example or test for the table function that executes fast and, hence, is not marked as
long test via `# long time`. This ensures that the `make testfast` command has a good coverage while still executing in
reasonable time which can be very helpful while integrating code into the library.

If you incorporated an existing estimator to the CryptographicEstimators library we strongly encourage to load the old
estimator as a module into `test/module` and write unit tests comparing the estimation results of the newly incorporated
estimator against the online available code. An example for such an integration test can be found under
`tests/test_le_bbps.sage`. Its important that all tests functions start with a `test_`.

To build and run the fast tests, execute:
```sh
make testfast
```
or all tests execute
```sh
make testall
```

or if you have Apple Silicon M1 Chip
```sh
make test-m1
```
#### Pytest
```sh
make docker-pytest
```

## Difference between ```_compute_time_complexity(...)``` and ```time_complexity(...)```
The first one returns the time for a given set of parameters in number of basic operations, while the second initiates a
search for the optimal parameters and converts time to bit operations if specified, includes memory access costs etc.

# Testing the Frontend:
After you finished implementing your estimator, you may want to export it to the 
[webfrontend](https://github.com/Crypto-TII/cryptographic_estimators_ui). See 
[this](https://github.com/Crypto-TII/cryptographic_estimators_ui/blob/main/docs/INPUTDICTIONARYGUIDE.md)
guide for the details of the configuration possibilities.

The webfrontend is configured via a json file `input_dictionary.json` which is 
already contained in this project root directory. This file already contains 
all estimators implemented in the CryptographicEstimators framework. To add your
new estimator first run:
```bash
python3 scripts/append_estimator_to_input_dictionary.py
```

This command appends a bare bone configuration to `input_dictionary.json` which 
looks like this:

```json
{
  "estimators": [
    {
      "estimator_id": "DUMMYEstimator", // Mandatory (Estimator class name)
      "algorithm_id": "DUMMYAlgorithm", // Mandatory (Algorithm class name)
      "display_label": "Dummy Estimator", // Mandatory
      "landing_page_content": "# Fill with markdown or latex content",
      // Problem parameters are mandatory, they are different for each problem
      // (Syndrome Decoding, Multivariate Quadratic, etc...)
      "problem_parameters": [ // This is a list of dictionaries. Where each dictionary relates to an specific field on the UI
        { 
          "id": "Parameter1", // Mandatory
          "type": "number", // Mandatory
          "display_label": "Parameter 1", // Mandatory
          // All the rest are optional
          "direction": "", // 'row' (default) or 'column'
          "placeholder": "",
          "default_value": "",
          "tooltip": "This is the first problem parameter",
        }
      ],
      "estimator_parameters": [
        {
          "id": "included_algorithms",
          "type": "multiple_selector",
          "direction": "column",
          "display_label": "Included algorithms",
          "tooltip": "Algorithms to include for optimization",
          "default_value": [],
          "excluded_algorithms": [],
          "options": [],
          "dependencies": []
        }
      ], // Equal among all the estimators, same structure as problem_paramenters
      "optional_parameters": [] // Different for each estimator, same structure as problem_paramenters
    },
  ]
}
```

After editing it to your needs it can look like this for the `DummyEstimator`:
```json
{
  "estimators": [
    {
      "estimator_id": "DUMMYEstimator",
      "algorithm_id": "DUMMYAlgorithm",
      "display_label": "Dummy Estimator",
      "landing_page_content": "Dummy Estimator\n\n This project provides an estimator for the well known Dummy Problem on which many cyryptocraphic schemes are based upon.",
      "problem_parameters": [
        { 
          "id": "n",
          "type": "number",
          "display_label": "Problem Dimension",
          "placeholder": "Insert parameter",
          "default_value": 100,
          "tooltip": "This is the first problem parameter",
        }
      ],
      "estimator_parameters": [
        {
          "id": "bit_complexities",
          "type": "switch",
          "display_label": "Bit complexities",
          "default_value": true,
          "tooltip": "Show complexities as count of bit operations. If false, show number of elementary operations"
        },
        {
          "id": "memory_access",
          "type": "selector",
          "direction": "column",
          "display_label": "Memory access cost",
          "default_value": 0,
          "tooltip": "Function that takes as input the memory bit complexity and outputs the associate algorithmic cost. Example, logarithmic memory access, input M, output M+log2M.",
          "options": [
            "Constant",
            "Logaritmic",
            "Square root",
            "Cube root"
          ]
        },
      ],
      "optional_parameters": [] // Different for each estimator, same structure as problem_paramenters
    },
  ]
}
```

Notice that you do not have to specify any algorithm in this configuration file. As this is all done automatically.