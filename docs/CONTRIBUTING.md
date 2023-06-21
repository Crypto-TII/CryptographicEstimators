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


# Hacking existing estimator
TODO

# Adding a new estimator
This tutorial shows how to add your own estimator to the CryptographicEstimators 
library, in which a `DummyEstimator` will be implemented.

First make sure that you have a working `python` and `sage` instance on your
current machine and have correctly [setup](https://github.com/Crypto-TII/CryptographicEstimators#installation-)
the project. In the following we assume that you are in the root directory of 
the project.

The next step adds all needed files for the `DummyEstimator` to the repository
via the command:
```bash 
>>> make add-estimator
```

The script asks you some basic properties of your estimator, eg. its name:
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

Now we need to make the added classes visible to the project by simply adding 
```python
from . import DUMMYEstimator
```
to `cryptographic_estimators/__init__.py`. 

Finally we are ready to run our estimator for the first time, simply create
a `test.py` file, containing:
```python
from cryptographic_estimators.DUMMYEstimator import *
A = DUMMYEstimator()
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
installed [sage](TODO), [python](TODO) and this library via `make install`.

As you can see, our new estimator doesn't estimate much. That's because we didn't
describe the problem at hand nor the algorithms `DUMMYAlgorithm1` at all.

An full estimator implementation includes the following 3 important classes:
  - DUMMYProblem 
  - DUMMYAlgorithm
  - DUMMYEstimator

The first describes the problem at hand, whereas the second computes its complexity.
`DUMMYEstimator` acts like a manager class, putting all together.

Lets introduce a complexity parameter `n`to our problem. Therefore change the 
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

For the next step we must make sure that the algorithm `DummyAlgorihm1` is 
actually computing something. For this add the following function together to 
the file `dummy_algorihm1.py`:
```
def _time_and_memory_complexity(self, parameters: dict, verbose_information=None):
    """
    Return time complexity of DUMMYAlgorithm1's  for given set of parameters

    INPUT:
    -  ``parameters`` -- dictionary including parameters
    -  ``verbose_information`` -- if set to a dictionary `permutations` and `gauß` will be returned.
    """
    n = self.problem.get_parameters()[0]
    return n, n
```

Now calling in the `test.py` script the `DUMMYEstimator` with the parameter `n=100`, e.g.
```
from cryptographic_estimators.DUMMYEstimator import *
A = DUMMYEstimator(n=100)
```
will show:
```bash 
+-----------------+----------------+
|                 |    estimate    |
+-----------------+-------+--------+
| algorithm       |  time | memory |
+-----------------+-------+--------+
| DUMMYAlgorithm1 | 100.0 |  100.0 |
+-----------------+-------+--------+
```
Congratulations, you first successful complexity estimation in the CryptographicEstimators framework.

A few note on what you see. The function `_time_and_memory_complexity(...)` is 
automatically called by the framework to compute the time and memory complexity 
for a given parameter set. The framework will iterate over a certain amount of 
different parameter sets until it cannot reduce the (time/memory) complexity
further. The minimum is then shown in such a table.
Additional note that the number the function `_time_and_memory_complexity(...)`
returns is in logarithmic notation, meaning a successful run of `DUMMYAlgorithm1`
would take `2**n` basic operations. More about the `verbose_information` you 
will find in the chapter [TODO](TODO).


Right now our estimator does only return a static runtime, lets enhance this by
introducing a optimization parameter `h`. 




# Change an existing estimator
TODO lets hack into an existing estimator

# Advanced Topics:

## Add verbose information

## Translation between different types of measurements
TODO describe the usage of the `to_bitcomplexity_time`.. in `DUMMYProblem`

## Exclude Algorithms
TODO
##
# Testing the Frontend:
TODO: Short chapter about how to add the generated `input_dictionary.json`
