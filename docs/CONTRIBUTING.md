## Project structure

If you want to add a new estimator please keep in mind the current project structure. You can run `make add-estimator` and it will create the basic code and folder structure for you to edit, you also can review the `DummyEstimator` to see a minimal reproduction of whats its needed to start. 

````python
── cryptographic_estimators
 │   ├── base_algorithm.py
 │   ├── base_problem.py
 │   ├── base_estimator.py
 │   └── OneEstimator.py
 │      ├── OneEstimator.py (Inherits from base_estimator)
 │      ├── OneProblem.py (Inherits from base_problem)
 │      ├── OneAlgorithm.py (Inherits from base_algorithm)
 │      └── Algorithms
 │          ├── List of algorithms (Inherits from NEWalgorithm.py)
 |   └── [...]
 │   └── NEWEstimator
 │      ├── NEWEstimator.py (Inherits from base_estimator)
 │      ├── NEWProblem.py (Inherits from base_problem)
 │      ├── NEWAlgorithm.py (Inherits from base_algorithm)
 │      └── Algorithms
 │          ├── List of algorithms (Inherits from NEWalgorithm.py)
````
---
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
Branch names should be snake_case. Which means that all the text must be lowercase and replace spaces with dashes. Also we should add as a prefix based on the type of implementation. For example:

```
refactor/modify_base_problem
feature/implement_dummy_estimator
fix/algorithm_parameter
```

### Pull request
  1. Only create pull requests to the `develop` branch.
  2. Fulfill the template

---

### Testing
#### Sage tests

To build and run the image based on Dockerfile.test
```sh
make testfast
```
or all tests via
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
### Documenting
Remember to document your code using [sphinx syntax](https://www.sphinx-doc.org/en/master/tutorial/automatic-doc-generation.html).


# Adding a new estimator
This tutorial shows how to add your own estimator to the CryptographicEstimators 
library. For this we implement a simple `DummyEstimator`.

First make sure that you have a working `python` and `sage` instance on your
current machine and have correctly [setup](https://github.com/Crypto-TII/CryptographicEstimators#installation-)
the project. In the following we assume that you are in the root directory of 
the project.

The next step adds all needed files for the `DummyEstimator` to the repository
via the command:
```bash 
>>> make add-estimator
```

The script asks you for some basic properties of the new estimator, eg. its name:
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
are mandatory. Additionally the script added one `dummy_algorithm1.py` file,
which acts like the first algorithm we want to implement.

Note that the script already added all needed links to other files in they
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

As you can see, our new estimator doesn't estimate much. That's because we didn't
describe the problem at hand nor the algorithms `DUMMYAlgorithm1` at all.

An full estimator implementation includes the following 3 important classes:
  - DUMMYProblem 
  - DUMMYAlgorithm
  - DUMMYEstimator

The first describes the problem at hand, whereas the second computes its complexity.
`DUMMYEstimator` acts like a manager class, putting all together.

Lets introduce a complexity parameter `n` to our problem. Therefore change the 
constructor of `DUMMYProblem` to 
```python
def __init__(self, n: int, **kwargs):
    super().__init__(**kwargs)
    self.parameters["problem dimension"] = n
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
to include the parameter `n`. Of cause you can add as much parameters as needed,
only make sure that estimator passes them correctly to the problem class.

As you can see, in both cases the `DUMMYProblem` and `DUMMYEstimator` do need 
to call the constructor of their super class, this is mandatory to inherit all
needed functions and fields for the estimation process.

For the next step we must make sure that the algorithm `DummyAlgorihm1` is 
actually computing something. For this add the following function to 
the file `dummy_algorihm1.py`:
```python
def _time_and_memory_complexity(self, parameters: dict, verbose_information=None):
    """
    Return time complexity of DUMMYAlgorithm1's  for given set of parameters

    INPUT:
    -  ``parameters`` -- dictionary including parameters
    -  ``verbose_information`` -- 
    """
    n = self.problem.get_parameters()[0]
    return n, 0
```

The first return value is the time complexity, whereas the second is the memory
complexity.

Now calling in the `test.py` script the `DUMMYEstimator` with the parameter `n=100`, e.g.
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

The function `_time_and_memory_complexity(...)` is automatically called by the 
framework to compute the time and memory complexity 
for a given parameter set. The framework will iterate over a certain amount of 
different parameter sets until it cannot reduce the (time/memory) complexity
further. The minimum is then shown in such a table.

Additional note that the values the function `_time_and_memory_complexity(...)`
returns are in logarithmic notation, meaning a successful run of `DUMMYAlgorithm1`
would take `2**n` basic operations. More about the `verbose_information` you 
will find in the [chapter](#Adding verbose information).


# Adding a optimization parameter
Right now our estimator does only return a static runtime, lets enhance this by
introducing a optimization parameter `h`, which represents the number of elements
to precompute for a MITM-based algorithm. If `h=10`, we precompute `2**10` elements
on a lookup table, and hence the runtime is reduced to `2**{n-h} = 2**{90}`.

To add the parameter we need to inform our `DUMMYAlgorithm1` class about it, for 
this add the following functions
```python
@optimal_parameter
def h(self):
    return self._get_optimal_parameter("h")

def _valid_choices(self):
    new_ranges = self._fix_ranges_for_already_set_parameters()
    for h in range(new_ranges["h"]["min"], new_ranges["h"]["max"], 2):
        yield {"h": h} 
```
The first function represents a helper function to efficiently access the optimal
parameter `h`, without the knowledge of the internals of the full implementation 
of the class. Note the function decorator `optimal_parameter`, this is mandatory
as it makes the optimization parameter known to the whole framework. 

The second function `_valid_choices()` is automatically called by the `BaseEstimator`,
to generated valid subsets of the parameter range. In our case, such a restriction
of parameters is rather simple, by only allowing even values for `h`. But of cause
you can implement arbitrary restrictions.

And finally make sure to initialize all needed fields within the constructor:
```python
def __init__(self, problem: DUMMYProblem, **kwargs):
    self._name = "DUMMYAlgorithm1"
    super(DUMMYAlgorithm1, self).__init__(problem, **kwargs)
    n = self.problem.get_parameters()[0]
    self.set_parameter_ranges("h", 0, n)
```

This is done by adding the function call `self.set_parameter_ranges("h", 0, n)` 
to the constructor of `DummyAlgorihm1`. This call sets the logical lower limit 
`0` and upper limit `n`. 

If we now change our computation function `_time_and_memory_complexity` to:
```python
def _time_and_memory_complexity(self, parameters: dict, verbose_information=None):
    """
    Return time complexity of DUMMYAlgorithm1's  for given set of parameters

    INPUT:
    -  ``parameters`` -- dictionary including parameters
    -  ``verbose_information`` -- 
    """
    n = self.problem.get_parameters()[0]
    par = SimpleNamespace(**parameters)
    rt = max(par.h, n - par.h)
    mem = par.h 
    return rt, mem
```

and running our `test.py` script, yields a successful computation of a MITM-approach:
```bash
+-----------------+---------------+
|                 |    estimate   |
+-----------------+------+--------+
| algorithm       | time | memory |
+-----------------+------+--------+
| DUMMYAlgorithm1 | 50.0 |   50.0 |
+-----------------+------+--------+
```

Note that the class `SimpleNamespace(...)` is used to elegantly access the 
algorithm parameters like `par.h`. But of cause you could also access the 
parameters via `h = parameters["h"]`.

# Advanced Topics:

## Benchmarking under memory constrains
Good news: you do not have to do anything. It works right out of the box via the 
`memory_bound` argument. So  changing the `test.py` file to `A = DUMMYEstimator(n=100, memory_bound=20)`
yields:
```bash
+-----------------+----------------------------+
|                 |          estimate          |
+-----------------+------+--------+------------+
| algorithm       | time | memory | parameters |
+-----------------+------+--------+------------+
| DUMMYAlgorithm1 | 80.0 |   80.0 | {'h': 20}  |
+-----------------+------+--------+------------+
```

## Add verbose information

The CryptographicEstimators framework has two ways to show verbose information
about the algorithms at hand. The first - and simple way - is by calling the 
`table` function with the argument `table(show_all_parameters=1)`, which results
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
it will show all parameters and their values of each applicable algorithm.

The second way to show more information is by using the `verbose_information` 
dictionary in the `_time_and_memory_complexity(...)` function. This dictionary 
comes in handy if one wants to show verbose information about the algorithm,
which are not parameters. For example list sizes, which are used internally.

To use it, you can add something like:
```python
    verbose_information["Lists Sizes"] = par.h
```
to the `_time_and_memory_complexity(...)` function. Afterwards you can read the 
verbose information via `_get_verbose_information()` function.

Note that you can use whatever you want as the dictionary key to save your
additional data.

## Translation between different types of measurements

The complexity of an algorithm is sometimes not measured in bit operations, but 
in vector operations or even in matrix operations. To convert between those 
measurements automatically, the CryptographicEstimators library offers an easy 
to use API.

Notably the two functions `to_bitcomplexity_time` and `to_bitcomplexity_memory`
which are implemented by the `Problem` class of your estimation, in our case
`DUMMYProblem`. These two functions are automatically called by the `BaseEstimator` 
if implemented.

Assumed our `DummyEstimator` estimates the complexity not in bit operations but 
in vector operations of length `n`. To convert to bit complexity we therefore 
change the two functions to the following:
```python
def to_bitcomplexity_time(self, basic_operations: float):
    """
    Return the bit-complexity corresponding to a certain amount of basic_operations

    INPUT:

    - ``basic_operations`` -- Number of basic operations (logarithmic)

    """
    n = self.parameters["problem dimension"]
    return basic_operations + log2(n)

def to_bitcomplexity_memory(self, elements_to_store: float):
    """
    Return the memory bit-complexity associated to a given number of elements to store

    INPUT:

    - ``elements_to_store`` -- number of memory operations (logarithmic)

    """
    n = self.parameters["problem dimension"]
    return elements_to_store + log2(n)
```

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

## Exclude Algorithms
Sometimes its useful to exclude certain algorithms from the estimation process,
because they may take long, or the algorithm is not that important.

From the client perspective this can be easily archived by adding
`excluded_algorithms=[DUMMYAlgorithm1]` to the estimator constructor:
```python
A = DUMMYEstimator(n=100, excluded_algorithms=[DUMMYAlgorithm1])
```

But it is sometimes desirable that some algorithms are excluded by standard from 
the estimation process. This can be archive by extending the constructor of 
`DummyEstimator` to:
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

and add the algorithms to be ignored like this:
```python
excluded_algorithms_by_default = [DUMMYAlgorithm1]
```

# Testing the Frontend:
After you finished with your estimator, you may want to export it to the 
[webfronted](https://github.com/Crypto-TII/cryptographic_estimators_ui). See 
[this](https://github.com/Crypto-TII/cryptographic_estimators_ui/blob/main/docs/INPUTDICTIONARYGUIDE.md)
guide for the details of the configuration possibilities.

The webfronted is configured via a json file `input_dictionary.json` which is 
already contained in this projects root directory. This file already contains 
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
          "default_value": "Constant",
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

Notice that you do not have to specify any algorithm in this configuration file.
As this is all done automatically.
