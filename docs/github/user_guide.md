# User Guide of the CryptographicEstimators Library

This document serves as a guide to use the _CryptographicEstimators_ library.
This is an open source project to estimate the hardness of computational
problems relevant in cryptography. The source code is available
[here](https://github.com/Crypto-TII/cryptographic_estimators).

## 1. Prerequisites and installation of the library

You can find a list of prerequisites and step-by-step instructions to install
the _CyptographicEstimators_ library
[here](https://github.com/Crypto-TII/cryptographic_estimators).

## 2. Using the Estimators

### 2.1. Importing estimators

The estimator class of the _Dummy problem_ is imported from the by executing:
`from cryptographic_estimators.ExampleEstimator import ExampleEstimator`

For example, to import the estimator class of the _Binary Syndrome Decoding
(SD)_ problem we execute

```python
from cryptographic_estimators.SDEstimator import SDEstimator
```

to import the estimator class of the _Multivariate Quadratic (MQ)_ problem we
execute

```python
from cryptographic_estimators.MQEstimator import MQEstimator
```

Further estimators available in the library to date are the `PKEstimator` for
the _permuted kernel problem_, the `PEEstimator` for the _permutation
equivalence problem_, the `LEEstimator` for the _linear equivalence problem_ and
the `SDFqEstimator` for the _syndrome decoding problem over Fq_

### 2.2. Creating estimator objects

An estimator of the hardness of the _Example_ problem with $p_1=10$ and $p_2=7$
is created by running: `ExampleEstimator(p1=10, p2=7)`.

The following code creates an estimator of the SD problem with code length $n =
100$, code dimension $k = 50$ and weight $w = 10$

```python
from cryptographic_estimators.SDEstimator import SDEstimator
SDE = SDEstimator(n=20, k=10, w=10)
```

The following code creates an estimator of the MQ problem $n = 15$ variables and
$m = 17$ equations over a field with $q = 2$ elements.

```python
from cryptographic_estimators.MQEstimator import MQEstimator
MQE = MQEstimator(n=15, m=17, q=2)
```

An overview of the complexity of all algorithms solving the problem can be
obtained via the `table` function.

```python
MQE.table()
```

```
+------------------+---------------+
|                  |    estimate   |
+------------------+------+--------+
| algorithm        | time | memory |
+------------------+------+--------+
| Bjorklund        | 39.8 |   15.3 |
| BooleanSolveFXL  | 20.3 |   11.9 |
| Crossbred        | 21.4 |    7.1 |
| DinurFirst       | 32.1 |   19.5 |
| DinurSecond      | 20.3 |   15.8 |
| ExhaustiveSearch | 18.0 |   11.9 |
| F5               | 36.6 |   23.2 |
| HybridF5         | 18.1 |   11.9 |
| Lokshtanov       | 62.9 |   16.1 |
+------------------+------+--------+
```

The table function offers various customizations. We detail the most important
ones at the end of this user guide. For a full list of features please see the
full [documentation](https://crypto-tii.github.io/CryptographicEstimators/).

#### Associated algorithms

When an estimator object is created, it generates a set of associated algorithm
objects. Each of these algorithms implements an estimator of the complexity of
the algorithm having the same name.<br />

We use the method `algorithms_names()` to get the **names** of the algorithms
solving the input instance for which there is an implemented estimator in the
_CyptographicEstimators_ library.

From the output of the following code, we know that the `Crossbred` algorithm
can be used to solve an instances of the MQ problem with parameters $n = 15$
variables and $m = 17$ equations over a field with $q = 2$ elements. And there
is a module estimating the complexity of `Crossbred`.

```python
from cryptographic_estimators.MQEstimator import MQEstimator
MQE = MQEstimator(n=15, m=17, q=2)
MQE.algorithm_names()
```

```
['Bjorklund',
 'BooleanSolveFXL',
 'Crossbred',
 'DinurFirst',
 'DinurSecond',
 'ExhaustiveSearch',
 'F5',
 'HybridF5',
 'Lokshtanov']
```

Only algorithms applicable for the specified parameters are listed. If we change
_q_ to 3 we see a different output. For example `DinurFirst` is missing in the
following example, as this algorithm only works over binary fields.

```python
from cryptographic_estimators.MQEstimator import MQEstimator
MQE = MQEstimator(n=15, m=17, q=3)
MQE.algorithm_names()
```

```
['BooleanSolveFXL',
 'Crossbred',
 'ExhaustiveSearch',
 'F5',
 'HybridF5',
 'Lokshtanov']
```

We can use the method `algorithms()` to get the full list of algorithm objects
associated with the estimator.

```python
from cryptographic_estimators.MQEstimator import MQEstimator
MQE = MQEstimator(n=15, m=17, q=2)
MQE.algorithms()
```

```
[Björklund et al. estimator for the MQ problem with 15 variables and 17 polynomials,
 BooleanSolveFXL estimator for the MQ problem with 15 variables and 17 polynomials,
 Crossbred estimator for the MQ problem with 15 variables and 17 polynomials,
 Dinur1 estimator for the MQ problem with 15 variables and 17 polynomials,
 Dinur2 estimator for the MQ problem with 15 variables and 17 polynomials,
 ExhaustiveSearch estimator for the MQ problem with 15 variables and 17 polynomials,
 F5 estimator for the MQ problem with 15 variables and 17 polynomials,
 HybridF5 estimator for the MQ problem with 15 variables and 17 polynomials,
 Lokshtanov et al. estimator for the MQ problem with 15 variables and 17 polynomials]
```

We can also excluded certain (otherwise applicable) algorithms from the
estimator. This prevents the corresponding algorithm object to be created during
the Estimator's initialization. We use the argument `excluded_algorithms`, to
list the algorithms we do not want to be included.

In the next example we exclude the algorithms `BooleanSolveFXL`, `F5`,
and`Crossbred`.

```python
from cryptographic_estimators.MQEstimator import MQEstimator
from cryptographic_estimators.MQEstimator.MQAlgorithms import BooleanSolveFXL, F5, Crossbred
MQE = MQEstimator(n=15, m=17, q=3, excluded_algorithms = [BooleanSolveFXL, F5, Crossbred])
MQE.algorithm_names()
```

```
['ExhaustiveSearch', 'HybridF5', 'Lokshtanov']
```

#### Accessing associated algorithms

Algoirthm objects can be individually accessed via `Estimator.<Algorithm Name>`.
For instance, to get an estimator of the complexity of the `Crossbred` algorithm
on an MQ problem $n = 15$ variables and $m = 17$ equations over a field with $q
= 2$ elements we run:

```python
from cryptographic_estimators.MQEstimator import MQEstimator
MQE = MQEstimator(n=15, m=17, q=3)
MQE.crossbred
```

```
Crossbred estimator for the MQ problem with 15 variables and 17 polynomials
```

## 3. Complexities of individual algorithms

Here we show how to obtain complexity estimates of individual algorithms.

_Understanding the complexity estimates_: By default

1. The **time complexity** is given as the logarithm in base 2 of the total
   number of bit operations the underlying algorithm executes for solving the
   problem.
2. The **memory complexity** is given as the logarithm in base 2 of the total
   number of bits the underlying algorithm needs to store at .

### 3.1. Estimates for specific parameters

The next line creates an estimator of Stern's algorithm for an instance of the
SD problem with code length $n = 100$, code dimension $k = 50$ and weight $w =
10$

```python
from cryptographic_estimators.SDEstimator import SDEstimator
SDE = SDEstimator(n=100, k=50, w=10)
Stern = SDE.stern
```

The method `parameter_names()` returns the list of parameters of the associated
algorithm. <br /> <br /> To obtain a list of parameter-names of the Stern
algorithm we run

```python
Stern.parameter_names()
```

```
['r', 'l', 'p']
```

We can compute the time and memory complexities of an algorithm with its
parameters taking specific values. <br /> <br /> The next two lines compute the
time and memory complexities of the Stern algorithm with $r =2$, $p = 3$ and
$l=4$

```python
Stern.time_complexity(r=2, p=3, l=4)
```

```
28.839332187288115
```

```python
Stern.memory_complexity(r=2, p=3, l=4)
```

```
18.828111685180072
```

#### Complexity type

The attribute `complexity_type` sets the mode to which complexities computed by
the estimator refer.

Currently, the _CryptographicEstimators_ library supports two types of
complexity: `Estimate` and `TildeO`.

The `Estimate` mode uses the most precise formula (according to the
state-of-the-art) of the cost of an algorithm to solve the input problem. In
this mode, all constant and polynomial factors of the cost are taken into
account.

The `TildeO` mode uses an asymptotic approximation of the costs. This mode might
disregard polylogarithmic factors.

`complexity_type = 0` sets the `Estimate` mode, while `complexity_type=1` the
`TildeO` one. By default every estimator is in the `Estimate` mode.

```python
from cryptographic_estimators.SDEstimator import SDEstimator
SDE = SDEstimator(n=100, k=50, w=10)
Stern = SDE.stern
Stern.complexity_type
```

```
0
```

Now we switch to the `TildeO` mode and compute time and memory complexity in
this mode.

```python
Stern.complexity_type = 1
```

```python
Stern.time_complexity(r=2, p=3, l=4)
```

```
inf
```

```python
Stern.memory_complexity(r=2, p=3, l=4)
```

```
inf
```

> **Hint:** It is possible to update the complexity type of all algorithms
> associated with the estimator via

```python
SDE.complexity_type = 1
SDE.prange.complexity_type
```

```
1
```

#### Bit complexities

The attribute `bit_complexities` defines whether the complexities are given in
bits or in elementary operations/elements. By default, `bit_complexities = 1`.

If `bit_complexities = 1`, then the time complexity counts for the number of
binary operations, while the memory complexity counts the number of bits of
memory, both in a logarithmic scale.

If `bit_complexities = 0`, then time complexity counts the number of elementary
operations computed, while the memory complexity counts the number of elementary
elements stored, both in a logarithmic scale.

This attribute has an effect when the estimator is in the `Estimate` mode.
Otherwise, it has no effect.

```python
from cryptographic_estimators.SDEstimator import SDEstimator
SDE = SDEstimator(n=100, k=50, w=10)
Stern = SDE.stern
Stern.bit_complexities
```

```
1
```

```python
Stern.bit_complexities = 0
```

```python
Stern.time_complexity(r=2, p=3, l=4)
```

```
22.19547599751339
```

```python
Stern.memory_complexity(r=2, p=3, l=4)
```

```
12.184255495405349
```

```python
Stern.bit_complexities
```

```
0
```

> **Hint:** Similarly the property can be set for all algorithms associated with
> the estimator via

```python
SDE.bit_complexities=0
SDE.prange.bit_complexities
```

```
0
```

#### Memory access cost

The `memory_access` cost indicates how the memory affects the running time of
the algorithm.

If $T$ is the complexity of an algorithm in terms of the number of bits or basic
operations (depending on the `bit_complexities` attribute), then the total cost
including the memory access is defined by $T_M = T \\cdot f(M)$, where $M$ is
the memory usage of the algorithm in bits or unit elements (again depending on
the `bit_complexities` attribute). <br />

`memory_access` can be set to `0, 1, 2` or `3`. By default `memory_access = 0`,
and

1. `memory_access = 0`, indicates that the $f(M) = 1$.
2. `memory_access = 1`, indicates that the $f(M) = \\log_2{M}$.
3. `memory_access = 2`, indicates that the $f(M) = \\sqrt{M}$.
4. `memory_access = 3`, indicates that the $f(M) = \\sqrt\[3\]{M}$.

The `memory_access` cost only has an effect when the algorithm is in the
`Estimate` mode.

```python
from cryptographic_estimators.SDEstimator import SDEstimator
SDE = SDEstimator(n=100, k=50, w=10)
Stern = SDE.stern
Stern.memory_access
```

```
0
```

```python
Stern.memory_access = 2
```

```python
Stern.time_complexity(r=2, p=3, l=4)
```

```
29.89385629700021
```

### 3.1. Time and memory complexities

The method `time_complexity` when used without any arguments, provides the
minimum time complexity of a specific algorithm considering all possible values
for its optimization parameters.

The method `memory_complexity` when used without any arguments, provides the
memory complexity associated with the configuration leading to minimal time
complexity.

To compute the time complexity of the Stern algorithm to solve an SD problem
with parameters $n=100, k=50, w=10$ we run

```python
from cryptographic_estimators.SDEstimator import SDEstimator
SDE = SDEstimator(n=100, k=50, w=10)
Stern = SDE.stern
Stern.time_complexity()
```

```
22.30294492063104
```

The memory complexity is obtained by

```python
Stern.memory_complexity()
```

```
16.023234556845985
```

To estimate the time and memory, the Stern estimator exhaustively searches for
the parameters of the Stern algorithm that minimize the time complexity, and
stores them.

The method `optimal_parameters()` returns the dictionary of parameters
minimizing the time complexity. If the dictionary is not yet computed, the
estimator will calculate it, store it and return it. <br />

The parameters minimizing the time complexity of the Stern algorithm on an SD
problem with parameters $n=100, k=50, w=10$ are

```python
Stern.optimal_parameters()
```

```
{'r': 4, 'p': 2, 'l': 9}
```

In contrast the function `get_optimal_parameters_dict()` returns the optimal
parameters dictionary in its current state. Even if the optimal parameters have
not been computed yet. For instance, for a fresh instance of the class, the
dictionary of optimal parameters is empty.

```python
from cryptographic_estimators.SDEstimator import SDEstimator
SDE = SDEstimator(n=100, k=50, w=10)
Stern = SDE.stern
Stern.get_optimal_parameters_dict()
```

```
{}
```

The attribute `parameter_ranges` returns the ranges in which each optimal
parameter is searched. In the particular case that we are considering, we have

```python
Stern.parameter_ranges
```

```
{'r': {'min': 0, 'max': 50},
 'l': {'min': 0, 'max': 50},
 'p': {'min': 0, 'max': 5}}
```

The previous line indicates that the optimal value of $r$ is searched in the
interval $\[0,50\]$, $l$ in $\[0,50\]$ and $p$ in $\[0,5\]$.

### Reset

The `reset` function restarts the internal state of an algorithm.

```python
from cryptographic_estimators.SDEstimator import SDEstimator
SDE = SDEstimator(n=100, k=50, w=10)
Stern = SDE.stern
Stern.time_complexity()
```

```
22.30294492063104
```

```python
Stern.get_optimal_parameters_dict()
```

```
{'r': 4, 'p': 2, 'l': 9}
```

```python
Stern.reset()
Stern.get_optimal_parameters_dict()
```

```
{}
```

> **Hint:** The same method is applicable to the estimator object. It resets the
> estimator as well as all associated algorithm objects

```python
SDE = SDEstimator(n=100, k=50, w=10)
Stern = SDE.stern
Stern.time_complexity()
```
```
22.30294492063104
```

```
SDE.reset()
Stern.get_optimal_parameters_dict()
```

```
{}
```

> **Note:** When changing the complexity type of an Estimator or Algorithm
> object, its reset function will be automatically called.

### 3.3. Customizing complexity optimization

Here we show how to customize the optimization of the time complexity.

#### Set optimal parameters

We can fix one or several parameters of an algorithm to a specific value while
optimizing the time complexity. This is done by using the method
`set_parameters`

In the following example we set $l = 3$ and $p=1$ in Stern's algorithm estimator

```python
from cryptographic_estimators.SDEstimator import SDEstimator
SDE = SDEstimator(n=100, k=50, w=10)
Stern = SDE.stern
Stern.set_parameters({'p':1, 'l':3})
```

Now we can find the parameter sets minimizing the time complexity under the
restriction $l = 3$ and $p=1$.

```python
Stern.time_complexity()
```

```
23.35379970503515
```

Optimal parameters under the restriction $l = 3$ and $p=1$ are

```python
Stern.optimal_parameters()
```

```
{'p': 1, 'l': 3, 'r': 4}
```

#### Configure parameter ranges

We can modify the range where a particular parameter is optimized by using the
method `set_parameter_ranges()`.

In the next example we set the interval $\[1, 3\]$ to be the optimization range
of the parameter $p$ in Stern's algorithm estimator. This forces the optimal
value of $p$ to be between 1 and 3.

```python
from cryptographic_estimators.SDEstimator import SDEstimator
SDE = SDEstimator(n=100, k=50, w=10)
Stern = SDE.stern
Stern.set_parameter_ranges(parameter='p', min_value=1, max_value=3)
Stern.parameter_ranges
```

```
{'r': {'min': 0, 'max': 50},
 'l': {'min': 0, 'max': 50},
 'p': {'min': 1, 'max': 3}}
```

```python
Stern.optimal_parameters()
```

```
{'r': 4, 'p': 2, 'l': 9}
```

#### memory bound

We use the `problem.memory_bound` attribute to optimize the time complexity
under the constraint that the corresponding memory complexity does not exceed
the memory bound. By default `problem.memory_bound` is set to infinity.

```python
from cryptographic_estimators.SDEstimator import SDEstimator
SDE = SDEstimator(n=100, k=50, w=10)
Stern = SDE.stern
Stern.problem.memory_bound
```

```
inf
```

Now we set the memory bound to $2^{15}$

```python
Stern.problem.memory_bound = 15
```

```python
Stern.memory_complexity() < 15
```

```
True
```

Additionally, you can directly limit the memory for all algorithms of an
estimator.

```python
from cryptographic_estimators.SDEstimator import SDEstimator
SDE = SDEstimator(n=100, k=50, w=10, memory_bound=15)
```

## 4. Complexities of several algorithms

We can customize and manage the complexities of several algorithms attached to
an estimator object from the estimator itself.

### 4.1. Computing and visualizing estimates

The estimation process starts by calling the `estimate()` method. It returns a
dictionary with the algorithm names, time and memory complexities, and the
corresponding dictionary of optimal parameters.

```python
from cryptographic_estimators.MQEstimator import MQEstimator
MQE = MQEstimator(n=15, m=17, q=3)
MQE.estimate()
```

```
{'BooleanSolveFXL': {'estimate': {'time': 29.858222427888588,
 'memory': 12.901244032467376, 
 'parameters': {'k': 14, 'variant': 'las_vegas'}}, 
 'additional_information': {}}, 
 'Crossbred': {'estimate': {'time': 27.676784055214462, 
 'memory': 17.045780987724598, 'parameters': {'D': 3, 'd': 1, 'k': 6}}, 
 'additional_information': {}}, 
 'ExhaustiveSearch': {'estimate': {'time': 25.40490707466741, 
 'memory': 12.901244032467376, 
 'parameters': {}}, 'additional_information': {}}, 
 'F5': {'estimate': {'time': 48.247169726507984, 
 'memory': 31.484561900604888, 
 'parameters': {}}, 'additional_information': {}}, 
 'HybridF5': {'estimate': {'time': 27.605835266254303,
  'memory': 12.901244032467376, 
  'parameters': {'k': 14}}, 'additional_information': {}}, 
  'Lokshtanov': {'estimate': {'time': 95.52681642861242, 
  'memory': 25.266724329355785, 
  'parameters': {'delta': 0.06666666666666667}}, 'additional_information': {}}}
```

Recall that we can avoid algorithms to be included in the esimator by using the
argument `excluded_algorithms`.

In the next example we exclude the algorithms ExhaustiveSearch, F5, HybridF5,
Lokshtanov.

```python
from cryptographic_estimators.MQEstimator import MQEstimator
from cryptographic_estimators.MQEstimator.MQAlgorithms import ExhaustiveSearch, F5, HybridF5, Lokshtanov
MQE = MQEstimator(n=15, m=17, q=3, excluded_algorithms = [ExhaustiveSearch, F5, HybridF5, Lokshtanov])
MQE.estimate()
```

```
{'BooleanSolveFXL': {'estimate': {'time': 29.858222427888588, 
'memory': 12.901244032467376, 
'parameters': {'k': 14, 'variant': 'las_vegas'}}, 'additional_information': {}}, 
'Crossbred': {'estimate': {'time': 27.676784055214462, 
'memory': 17.045780987724598, 
'parameters': {'D': 3, 'd': 1, 'k': 6}}, 'additional_information': {}}}
```

In order to better visualize the provided estimates, one can use directly the
method `table()`. This method will internally call the estimate method, if
estimates have not been computed before, to get the algorithm estimates in the
`Estimate` mode, save them and then print them in a table to ease visualization
and comparison.

```python
from cryptographic_estimators.MQEstimator import MQEstimator
from cryptographic_estimators.MQEstimator.MQAlgorithms import BooleanSolveFXL, F5, Crossbred
MQE = MQEstimator(n=15, m=17, q=3)
MQE.table()
```

```
+------------------+---------------+
|                  |    estimate   |
+------------------+------+--------+
| algorithm        | time | memory |
+------------------+------+--------+
| BooleanSolveFXL  | 29.9 |   12.9 |
| Crossbred        | 27.7 |   17.0 |
| ExhaustiveSearch | 25.4 |   12.9 |
| F5               | 48.2 |   31.5 |
| HybridF5         | 27.6 |   12.9 |
| Lokshtanov       | 95.5 |   25.3 |
+------------------+------+--------+
```

Or again with some algorithm being excluded from consideration

```python
from cryptographic_estimators.MQEstimator.MQAlgorithms import ExhaustiveSearch, F5, HybridF5, Lokshtanov
MQE = MQEstimator(n=15, m=17, q=3, excluded_algorithms = [ExhaustiveSearch, F5, HybridF5, Lokshtanov])
MQE.table()
```

```
+-----------------+---------------+
|                 |    estimate   |
+-----------------+------+--------+
| algorithm       | time | memory |
+-----------------+------+--------+
| BooleanSolveFXL | 29.9 |   12.9 |
| Crossbred       | 27.7 |   17.0 |
+-----------------+------+--------+
```

From the previous output we observe that solving an MQ problem with parameters
$n=15, m=17,$ and $q=3$, the algorithms ExhaustiveSearch, HybridF5 and
Lokshtanov have optimal time complexity of $2^{25.4}$, $2^{30.1}$, and
$2^{99.6}$ field multiplications, respectively.

An additinal example

```python
from cryptographic_estimators.SDEstimator import SDEstimator
SDE = SDEstimator(n=100, k=50, w=10)
SDE.table()
```

```
+---------------+---------------+
|               |    estimate   |
+---------------+------+--------+
| algorithm     | time | memory |
+---------------+------+--------+
| BallCollision | 23.3 |   16.0 |
| BJMMdw        | 23.4 |   14.7 |
| BJMMpdw       | 23.3 |   14.3 |
| BJMM          | 22.8 |   15.0 |
| BJMM_plus     | 22.8 |   15.0 |
| BothMay       | 22.4 |   14.7 |
| Dumer         | 22.7 |   16.4 |
| MayOzerov     | 22.3 |   14.8 |
| Prange        | 28.3 |   12.7 |
| Stern         | 22.3 |   16.0 |
+---------------+------+--------+
```

### 4.2. Customizing estimation and visualization

#### Visualization

One can input several arguments to the table method:

1. `show_all_parameters` allows us to visulize the parameters optimizing the
   time complexity for the given input. An empty dictionary {} indicates the
   corresponding algorithm does not have parameters. (default: false)

2. `precision` to set the number of decimal digits output (default: 1)

3. `truncate` to truncate the output estimates rather than round them (default:
   false)

In what follows we observe that, while solving an SD problem with parameters
`n=100, k=50, w=10`, the Stern algorithm has an optimal time complexity of
$2^{22.3}$ when $r=4$ , $p=2$ and $l = 9$.

```python
from cryptographic_estimators.SDEstimator import SDEstimator
SDE = SDEstimator(n=100, k=50, w=10)
SDE.table(show_all_parameters=True, precision=3, truncate=True)
```

```
+---------------+-------------------------------------------------------------------------+
|               |                                 estimate                                |
+---------------+--------+--------+-------------------------------------------------------+
| algorithm     |   time | memory |                       parameters                      |
+---------------+--------+--------+-------------------------------------------------------+
| BallCollision | 23.290 | 16.023 |           {'r': 4, 'p': 2, 'pl': 0, 'l': 7}           |
| BJMMdw        | 23.416 | 14.731 | {'r': 4, 'p': 2, 'p1': 1, 'w1': 0, 'w11': 0, 'w2': 0} |
| BJMMpdw       | 23.250 | 14.302 |           {'r': 4, 'p': 2, 'p1': 1, 'w2': 0}          |
| BJMM          | 22.778 | 15.027 |     {'r': 4, 'depth': 2, 'p': 2, 'p1': 1, 'l': 8}     |
| BJMM_plus     | 22.778 | 15.027 |       {'r': 4, 'p': 2, 'p1': 1, 'l': 8, 'l1': 2}      |
| BothMay       | 22.421 | 14.731 |  {'r': 4, 'p': 2, 'w1': 0, 'w2': 0, 'p1': 1, 'l': 2}  |
| Dumer         | 22.700 | 16.421 |                {'r': 4, 'l': 8, 'p': 2}               |
| MayOzerov     | 22.251 | 14.808 |     {'r': 4, 'depth': 2, 'p': 2, 'p1': 1, 'l': 2}     |
| Prange        | 28.291 | 12.688 |                        {'r': 4}                       |
| Stern         | 22.302 | 16.023 |                {'r': 4, 'p': 2, 'l': 9}               |
+---------------+--------+--------+-------------------------------------------------------+
```

4. `show_tilde_o_time` allows to show the time and memory estimates in the
   TildeO mode.

```python
SDE.table(show_tilde_o_time=True)
```

```
+---------------+------------------+---------------+
|               | tilde_o_estimate |    estimate   |
+---------------+-------+----------+------+--------+
| algorithm     |  time |   memory | time | memory |
+---------------+-------+----------+------+--------+
| BallCollision |  10.4 |      3.3 | 23.3 |   16.0 |
| BJMMdw        |    -- |       -- | 23.4 |   14.7 |
| BJMMpdw       |    -- |       -- | 23.3 |   14.3 |
| BJMM          |   9.0 |      6.9 | 22.8 |   15.0 |
| BJMMplus      |    -- |       -- | 22.8 |   15.0 |
| BothMay       |   8.8 |      6.4 | 22.4 |   14.7 |
| Dumer         |  10.4 |      3.3 | 22.7 |   16.4 |
| MayOzerov     |   8.5 |      7.2 | 22.3 |   14.8 |
| Prange        |  10.8 |        0 | 28.3 |   12.7 |
| Stern         |  10.4 |      2.9 | 22.3 |   16.0 |
+---------------+-------+----------+------+--------+
```

The `--` in the printed table means _Not Implemented Yet_.

#### Estimation

From an estimator object, one can set a configuration that applies to all the
algorithms attached to it. One can set: `complexity_time`, `bit_complexities` or
`memory_access` and any other parameter for the specific estimator. All these
general configurations are given as input to the estimator class.

All the algorithms attached to the following estimator object are in the
`Estimate` mode, they provide bit complexities, and they have a square root
memory access cost of square root, see Section 3.

```python
from cryptographic_estimators.MQEstimator import MQEstimator
MQE = MQEstimator(n=15, m=17, q=3, complexity_type=0, bit_complexities=True, memory_access=3)
Algo = MQE.algorithms()[1]
print(Algo.complexity_type, Algo.bit_complexities, Algo.memory_access)
```

```
0 True 3
```

To see the `bit_complexities` value of all the algorithms to estimator MQE we
run `MQE.bit_complexities`. Similarly, `for complexity_type` and
`memory_access`.

```python
MQE.bit_complexities
```

```
[True, True, True, True, True, True]
```

One can also apply and modify the configuration of one or several algorithms.

In the following example, we set $d=1$ and $D=3$ the optimal parameters of the
`Crossbred` algorithm; we left untouched the other algorithms.

```python
from cryptographic_estimators.MQEstimator import MQEstimator
MQE = MQEstimator(n=20, m=20, q=3)
MQE.crossbred.set_parameters({'d':1, 'D':3})
MQE.table(show_all_parameters=True)
```

```
+------------------+----------------------------------------------------+
|                  |                      estimate                      |
+------------------+-------+--------+-----------------------------------+
| algorithm        |  time | memory |             parameters            |
+------------------+-------+--------+-----------------------------------+
| BooleanSolveFXL  |  37.8 |   14.0 | {'k': 19, 'variant': 'las_vegas'} |
| Crossbred        |  35.7 |   18.0 |      {'d': 1, 'D': 3, 'k': 6}     |
| ExhaustiveSearch |  33.5 |   14.0 |                 {}                |
| F5               |  60.0 |   39.7 |                 {}                |
| HybridF5         |  35.8 |   14.0 |             {'k': 19}             |
| Lokshtanov       | 106.6 |   33.2 |          {'delta': 0.05}          |
+------------------+-------+--------+-----------------------------------+
```

### 4.1. Fastest algorithm

The method `fastest_algorithm()` returns an estimator of the algorithm with the
minimum time complexity for the specific import problem

```python
from cryptographic_estimators.MQEstimator import MQEstimator
MQE = MQEstimator(n=20, m=20, q=3)
F = MQE.fastest_algorithm()
F
```

```
ExhaustiveSearch estimator for the MQ problem with 20 variables and 20 polynomials
```

```python
F.time_complexity()
```

```
33.475373791757825
```
