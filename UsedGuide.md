# User Guide of the CryptographicEstimators Library 

This document serves as a guide to use the _CyptographicEstimators_ library. This is an open source project to estimate the hardness of computational problems relevant in cryptography. The source code is available [here](https://github.com/Crypto-TII/cryptographic_estimators).

## 1. Pre-requisites and installation of the library

A list of pre-requisites and step-by-step instructions to install the _CyptographicEstimators_ library are [here](https://github.com/Crypto-TII/cryptographic_estimators).

## 2. Estimator classes

### 2.1. Importing estimators 

The estimator class of the _Example problem_ is imported from the by executing: <br />
<br />
`from cryptographic_estimators.ExampleEstimator import ExampleEstimator`

For instance, to import the estimator class of the _Binary Syndrome Decoding (SD)_ problem we execute 


```python
from cryptographic_estimators.SDEstimator import SDEstimator
```

to import the estimator class of the _Mutivariate Quadratic (MQ)_ problem we execute


```python
from cryptographic_estimators.MQEstimator import MQEstimator
```

### 2.2. Creating estimator objects

An estimator of the hardness of the _Example_ problem with $p_1=10$ and $p_2=7$ is created by running: `ExampleEstimator(p1=10, p2=7)`.

The following code creates an estimator of the SD problem with code length $n = 100$, code dimension $k = 50$ and weigth $w = 10$ 


```python
from cryptographic_estimators.SDEstimator import SDEstimator
SDE = SDEstimator(n=20, k=10, w=10)
```

The following code creates an estimator of the MQ problem $n = 15$ variables and $m = 17$ equations over a field with $q = 2$ elements.


```python
from cryptographic_estimators.MQEstimator import MQEstimator
MQE = MQEstimator(n=15, m=17, q=2)
```

#### Associate algorithms 

When an estimator object is created it uploads a set algorithm methods associated to the input instance. Each of these methods implements an estimator of the complexity of the algorithm having the same same.<br />

We use the method `algorithms_names()` to get the **names** of the algorithms solving the input instance for which there is an implemented estimator in the _CyptographicEstimators_ library. 

From the output of the following code, we know that the `Crossbred` algorithm can be used to solve an intances of the MQ problem with paramters $n = 15$ variables and $m = 17$ equations over a field with $q = 2$ elements. And there is module to estimate the complexity `Crossbred`. 


```python
from cryptographic_estimators.MQEstimator import MQEstimator
MQE = MQEstimator(n=15, m=17, q=2)
MQE.algorithm_names()
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



In the output of the following, it is not `DinurFirst` because this algorithm does not work over fields with more than 2 elements.


```python
from cryptographic_estimators.MQEstimator import MQEstimator
MQE = MQEstimator(n=15, m=17, q=3)
MQE.algorithm_names()
```




    ['BooleanSolveFXL',
     'Crossbred',
     'ExhaustiveSearch',
     'F5',
     'HybridF5',
     'Lokshtanov']



We use the method `algorithms()` to get the full list of estimators for algorithms solving the input instance. 


```python
from cryptographic_estimators.MQEstimator import MQEstimator
MQE = MQEstimator(n=15, m=17, q=2)
MQE.algorithms()
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



We can avoid algorithms to be uploaded during the creation of the estimator object. We use the argument `excluded_algorithms`, which is empty by default, to list the algorithms we do not want to be uploded. 

In the next example we exclude the algorithms `BooleanSolveFXL`, `F5`, `Crossbred`.


```python
from cryptographic_estimators.MQEstimator import MQEstimator
from cryptographic_estimators.MQEstimator.MQAlgorithms import BooleanSolveFXL, F5, Crossbred
MQE = MQEstimator(n=15, m=17, q=3, excluded_algorithms = [BooleanSolveFXL, F5, Crossbred])
MQE.algorithm_names()
```




    ['ExhaustiveSearch', 'HybridF5', 'Lokshtanov']



#### Accessing associated algorithms

We can individualy access the uplodaded estimators of algorithms from the estimator object.

For instance, to get an estimator of the complexity of the `Crossbred` algorithm on an MQ problem $n = 15$ variables and $m = 17$ equations over a field with $q = 2$ elements we run: 


```python
from cryptographic_estimators.MQEstimator import MQEstimator
MQE = MQEstimator(n=15, m=17, q=3)
MQE.crossbred
```




    Crossbred estimator for the MQ problem with 15 variables and 17 polynomials



## 3.  Complexities of individual algorithms

Here we show how to obtain complexity estimates of individual algorithms.

_Understanding the complexity estimates_: By default

   1. The **time complexity** is given as the logarithm in base 2 of the bit complexity of the underlying algorithm. 
   2. The **memory complexity** is given as the logarithm in base 2 of the bit memory complexity of the underlying algorithm. 

### 3.1. Estimates for specific parameters

The next line creates an estimaotor of Stern's algorithm for an instance of the SD porblem with code length $n = 100$, code dimension $k = 50$ and weigth $w = 10$ 


```python
from cryptographic_estimators.SDEstimator import SDEstimator
SDE = SDEstimator(n=100, k=50, w=10)
Stern = SDE.stern
```

The method `parameter_names()` return the list of parameters of the associated algorithm. <br />
<br />
The list of paramters of the Stern algorithm we run


```python
Stern.parameter_names()
```




    ['r', 'l', 'p']



We can compute time and memory complexities of an algorithm with its parameters take specific values. <br />
<br />
The next two lines compute the time and memory complexities of the Stern algorithm with $r =2$, $p = 3$ and $l=4$


```python
Stern.time_complexity(r=2, p=3, l=4)
```




    28.839332187288115




```python
Stern.memory_complexity(r=2, p=3, l=4)
```




    18.828111685180072



#### Complexity type

The attribute `complexity_type` establishes the mode on which of complexities used by the underlying estimator are compute.

Currently the _CryptographicEstimators_ library supports up two types of complexity: 
`Estimate` and `TildeO`.

The `Estimate` mode uses the most precise formula (according the state-of-the-art) of the cost of an algorithm 
to solve the input problem. In this mode, all constant and polynomial
factors of the cost are taken into account.

The `TildeO` mode uses asymptotic approximation of the costs. This mode might disregard polylogarithmic factors.

`complexity_type = 0` sets the `Estimate` mode, while `complexity_type=1` the `TildeO` one. By default every estimator is in the `Estimate` mode.


```python
from cryptographic_estimators.SDEstimator import SDEstimator
SDE = SDEstimator(n=100, k=50, w=10)
Stern = SDE.stern
Stern.complexity_type
```




    0



Now we switch to the `TildeO` mode and compute time and memory complexity in this mode.


```python
Stern.complexity_type = 1
```


```python
Stern.time_complexity(r=2, p=3, l=4)
```




    inf




```python
Stern.memory_complexity(r=2, p=3, l=4)
```




    inf



#### Bit complexities

The attribute `bit_complexities` defines whether the complexities are given in bits or in elementary operetions/elements. By default, `bit_complexities = 1`.

If `bit_complexities = 1`, then the time complexity counts for the number of binary operations, while the memory complexity counts the number of bits of memory, both in a logarithmic scale.

If `bit_complexities = 0`, then time complexity counts the number of elementay operations computed, while the memory complexity counts the number of elementary elements stored, both in a logarithmic scale.

This attribute has effect when the estimator is in the `Estimate` mode. Otherwise, it has no effect.


```python
from cryptographic_estimators.SDEstimator import SDEstimator
SDE = SDEstimator(n=100, k=50, w=10)
Stern = SDE.stern
Stern.bit_complexities
```




    1




```python
Stern.bit_complexities = 0
```


```python
Stern.time_complexity(r=2, p=3, l=4)
```




    22.19547599751339




```python
Stern.memory_complexity(r=2, p=3, l=4)
```




    12.184255495405349




```python
Stern.bit_complexities
```




    1



#### Memory access cost

The `memory_access` cost indicates how the memory affects the running time of the algoritm.

If $T$ is the complexity of an algorithm in terms of number of operatin operations, then the additional cost from the memory access is defined by $T_M = T \cdot f(M)$, where $M$ is the memory usage of the algorithm.  <br />

`memory_access` can be set to `0, 1, 2` or `3`. By default `memory_access = 0`, and

1. `memory_access = 0`, indicates that the $f(M) = 1$.
2. `memory_access = 1`, indicates that the $f(M) = \log_2{M}$.
3. `memory_access = 2`, indicates that the $f(M) = \sqrt{M}$.
4. `memory_access = 3`, indicates that the $f(M) = \sqrt[3]{M}$.


The `memory_access` cost only have effect when the algorithm is in the `Estimate` mode. 


```python
from cryptographic_estimators.SDEstimator import SDEstimator
SDE = SDEstimator(n=100, k=50, w=10)
Stern = SDE.stern
Stern.memory_access
```




    0




```python
Stern.memory_access = 2
```


```python
Stern.time_complexity(r=2, p=3, l=4)
```




    36.85094946571111



### 3.1. Time and memory complexities

The methods `time_complexity` and `memory_complexity` are used without any arguments they provide, respectively, the minimum the time and memory complexities of an especific algorithm amogst all possible values of its possible parameter sets. 

To compute the time complexity of the Stern algorithm to solve an SD problem with parameters $n=100, k=50, w=10$ we run


```python
from cryptographic_estimators.SDEstimator import SDEstimator
SDE = SDEstimator(n=100, k=50, w=10)
Stern = SDE.stern
Stern.time_complexity()
```




    22.30294492063104



The memory complexity is obtained by 


```python
Stern.memory_complexity()
```




    16.023234556845985



To estimate the time or memory the Stern estimator exhaustively find the parameters of the Stern algorithm that minimize the time complexity, and it store them.

The method `optimal_parameters()` returns the dictionary of parameters minimizing the time complexity. In the case, the dictionary is not yet computed, the estimator will first compute it and then return it. <br />
<br />

The parameters minimizing the time complexity of the Stern algorithm on an SD problem with paramters $n=100, k=50, w=10$ are


```python
Stern.optimal_parameters()
```




    {'r': 4, 'p': 2, 'l': 9}



`get_optimal_parameters_dict()` return the optimal parameters dictionary in its current state. Even if the optimal paramters have not been computed. For instance, for a fresh instance of the class the dictionary of optimal paramters is empty.


```python
from cryptographic_estimators.SDEstimator import SDEstimator
SDE = SDEstimator(n=100, k=50, w=10)
Stern = SDE.stern
Stern.get_optimal_parameters_dict()
```




    {}



The attribute `parameter_ranges` returns the ranges when each optimal parameter is searched. In the particular case that we are considering we have


```python
Stern.parameter_ranges
```




    {'r': {'min': 0, 'max': 50},
     'l': {'min': 0, 'max': 50},
     'p': {'min': 0, 'max': 5}}



The previous line indicates that the optimal value of $r$ is searched in the interval $[0,50]$, $l$ in $[0,50]$ and $p$ in $[0,5]$.

### Reset

It restarts the internal state of an algorithm.


```python
from cryptographic_estimators.SDEstimator import SDEstimator
SDE = SDEstimator(n=100, k=50, w=10)
Stern = SDE.stern
Stern.time_complexity()
```




    22.30294492063104




```python
Stern.get_optimal_parameters_dict()
```




    {'r': 4, 'p': 2, 'l': 9}




```python
Stern.reset()
Stern.get_optimal_parameters_dict()
```




    {}



### 3.3. Customizing complexity optimization

Here we show how to configure the optimization of the time complexity

#### Set optimal parameter

We can fix one or several parameter(s) of an algorithm to an specific value while optimizing the time complexity. This is done by using the method `set_parameters`

In the following, example we set $l = 3$ and $p=1$ in Stern's algorithm estimator


```python
from cryptographic_estimators.SDEstimator import SDEstimator
SDE = SDEstimator(n=100, k=50, w=10)
Stern = SDE.stern
Stern.set_parameters({'p':1, 'l':3})
```

Now we can find the parameter sets minimizing the time complexity under the restiction $l = 3$ and $p=1$.


```python
Stern.time_complexity()
```




    23.35379970503515



Optimal paramters under the restriction $l = 3$ and $p=1$ are


```python
Stern.optimal_parameters()
```




    {'p': 1, 'l': 3, 'r': 4}



#### Configure parameter ranges

We can modify the range where a particular parameter is optimized by using the method `set_parameter_ranges()`.

In the next example we set the interval $[1, 3]$ to be the optimization range of the paramter $p$ in Stern's algorithm estimator. This forces the optimal value of $p$ to be between 1 and 3.


```python
from cryptographic_estimators.SDEstimator import SDEstimator
SDE = SDEstimator(n=100, k=50, w=10)
Stern = SDE.stern
Stern.set_parameter_ranges(parameter='p', min_value=1, max_value=3)
Stern.parameter_ranges
```




    {'r': {'min': 0, 'max': 50},
     'l': {'min': 0, 'max': 50},
     'p': {'min': 1, 'max': 3}}




```python
Stern.optimal_parameters()
```




    {'r': 4, 'p': 1, 'l': 3}



#### memory bound

We use the `problem.memory_bound` attribute to optimize the time complexity under the constrain that the corresponding memory complexity does not exceed the memory bound. By default `problem.memory_bound` is set to infinty.


```python
from cryptographic_estimators.SDEstimator import SDEstimator
SDE = SDEstimator(n=100, k=50, w=10)
Stern = SDE.stern
Stern.problem.memory_bound 
```




    inf



Now we set the memory bound to $2^{30}$


```python
Stern.problem.memory_bound = 30
```


```python
Stern.memory_complexity() < 30
```




    True



## 4. Complexities of several algorithms

We can customize and manege the complexities of several algorithms attached to an estimator object from the estimator itself.

### 4.1. Computing and visualizing estimates

The estimation process starts by calling the `estimate()` method. It returns a dictionary with the algorithm names, time and memory complexities, and the corresponding dictionary of optimal paraterters.


```python
from cryptographic_estimators.MQEstimator import MQEstimator
MQE = MQEstimator(n=15, m=17, q=3)
MQE.estimate()
```




    {'BooleanSolveFXL': {'estimate': {'time': 29.85822242788859,
       'memory': 12.901244032467376,
       'parameters': {'k': 14, 'variant': 'las_vegas'}},
      'additional_information': {}},
     'Crossbred': {'estimate': {'time': 24.117772038209786,
       'memory': 17.7247403222648,
       'parameters': {'D': 4, 'd': 1, 'k': 7}},
      'additional_information': {}},
     'ExhaustiveSearch': {'estimate': {'time': 25.40490707466741,
       'memory': 12.901244032467376,
       'parameters': {}},
      'additional_information': {}},
     'F5': {'estimate': {'time': 36.87177581110349,
       'memory': 31.484561900604888,
       'parameters': {}},
      'additional_information': {}},
     'HybridF5': {'estimate': {'time': 30.0506201089272,
       'memory': 12.901244032467376,
       'parameters': {'k': 10}},
      'additional_information': {}},
     'Lokshtanov': {'estimate': {'time': 99.55650866097999,
       'memory': 25.266724329355785,
       'parameters': {'delta': 1/15}},
      'additional_information': {}}}



We can avoid algorithms to be uploaded during the creation of the estimator object. We use the argument `excluded_algorithms`, which is empty by default, to list the algorithms we do not want to be uploded. 

In the next example we exclude the algorithms ExhaustiveSearch, F5, HybridF5, Lokshtanov.


```python
from cryptographic_estimators.MQEstimator import MQEstimator
from cryptographic_estimators.MQEstimator.MQAlgorithms import ExhaustiveSearch, F5, HybridF5, Lokshtanov
MQE = MQEstimator(n=15, m=17, q=3, excluded_algorithms = [ExhaustiveSearch, F5, HybridF5, Lokshtanov])
MQE.estimate()
```




    {'BooleanSolveFXL': {'estimate': {'time': 29.85822242788859,
       'memory': 12.901244032467376,
       'parameters': {'k': 14, 'variant': 'las_vegas'}},
      'additional_information': {}},
     'Crossbred': {'estimate': {'time': 24.117772038209786,
       'memory': 17.7247403222648,
       'parameters': {'D': 4, 'd': 1, 'k': 7}},
      'additional_information': {}}}



to vizualize better the provided estimates, one can use directly the method `table()`. This method will internally call the estimate method to get the algorithm estimates in the `Estimate` mode, and then print them in a table to ease visualization and comparison.


```python
from cryptographic_estimators.MQEstimator import MQEstimator
from cryptographic_estimators.MQEstimator.MQAlgorithms import BooleanSolveFXL, F5, Crossbred
MQE = MQEstimator(n=15, m=17, q=3)
MQE.table()
```

    +------------------+---------------+
    |                  |    estimate   |
    +------------------+------+--------+
    | algorithm        | time | memory |
    +------------------+------+--------+
    | BooleanSolveFXL  | 29.9 |   12.9 |
    | Crossbred        | 24.1 |   17.7 |
    | ExhaustiveSearch | 25.4 |   12.9 |
    | F5               | 36.9 |   31.5 |
    | HybridF5         | 30.1 |   12.9 |
    | Lokshtanov       | 99.6 |   25.3 |
    +------------------+------+--------+



```python
from cryptographic_estimators.MQEstimator.MQAlgorithms import ExhaustiveSearch, F5, HybridF5, Lokshtanov
MQE = MQEstimator(n=15, m=17, q=3, excluded_algorithms = [ExhaustiveSearch, F5, HybridF5, Lokshtanov])
MQE.table()
```

    +-----------------+---------------+
    |                 |    estimate   |
    +-----------------+------+--------+
    | algorithm       | time | memory |
    +-----------------+------+--------+
    | BooleanSolveFXL | 29.9 |   12.9 |
    | Crossbred       | 24.1 |   17.7 |
    +-----------------+------+--------+


From the previous output we observe that solving an MQ problem with parameters $n=15, m=17,$ and $q=3$, the algorithms ExhaustiveSearch, HybridF5 and Lokshtanov have optimal time complexity of $2^{25.4}$, $2^{30.1}$, and $2^{99.6}$ field multiplications, respectively.

An additinal example


```python
from cryptographic_estimators.SDEstimator import SDEstimator
SDE = SDEstimator(n=100, k=50, w=10)
SDE.table()
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


### 4.2. Customizing estimation and vizualization

#### Visualization

One can input several arguments to the table method:

1. `show_all_parameters allow` to vizulize the parameters optimizing the time complexity for the given input. An empty dictionary {} indicates the correspoding algorithm do not have parameters. (default: false)


2. `precision` to set the number of decimal digits output (default: 1)


3. `truncate` to truncate the output estimates rather than round them (default:
     false)

The argument `show_all_parameters` allow to vizulize the parameters optimizing the time complexity for the given input. An empty paramters dictionary `{}` indicates the correspoding algorithm do not have parameters. 

In what follows we observe that, while solving an SD problem with paramters `n=100, k=50, w=10`, the Stern algorithm has a optimal time complexity of $2^{22.3}$ when $r=4$ , $p=2$ and $l = 9$.


```python
from cryptographic_estimators.SDEstimator import SDEstimator
SDE = SDEstimator(n=100, k=50, w=10)
SDE.table(show_all_parameters=True, precision=3, truncate=True)
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


4. `show_tilde_o_time` allows to show the time and memory estimates in the TildeO mode.


```python
SDE.table(show_tilde_o_time=True)
```

    +---------------+------------------+---------------+
    |               | tilde_o_estimate |    estimate   |
    +---------------+-------+----------+------+--------+
    | algorithm     |  time |   memory | time | memory |
    +---------------+-------+----------+------+--------+
    | BallCollision |  10.4 |      3.3 | 23.3 |   16.0 |
    | BJMMdw        |    -- |       -- | 23.4 |   14.7 |
    | BJMMpdw       |    -- |       -- | 23.3 |   14.3 |
    | BJMM          |   9.0 |      6.8 | 22.8 |   15.0 |
    | BJMM_plus     |    -- |       -- | 22.8 |   15.0 |
    | BothMay       |   8.8 |      6.4 | 22.4 |   14.7 |
    | Dumer         |  10.4 |      3.3 | 22.7 |   16.4 |
    | MayOzerov     |   8.5 |      7.5 | 22.3 |   14.8 |
    | Prange        |  10.8 |      0.0 | 28.3 |   12.7 |
    | Stern         |  10.4 |      2.9 | 22.3 |   16.0 |
    +---------------+-------+----------+------+--------+


The `--` in the printed table means TO COMPLETED.

#### Estimation 

From an estimator object, one can set configuration that applies for all the algorithms attached to it. One can set:
`complexity_time`, `bit_complexities`, `memory_access`, and any other parameter for the specific estimator. 
All this general configuration are given as input to the estimator class.

All the algorithms attached to the following estimator object are in the `Estimate` mode, they provide bit complexities and they have an square root memory access cost of square root, see Section 3.


```python
from cryptographic_estimators.MQEstimator import MQEstimator
MQE = MQEstimator(n=15, m=17, q=3, complexity_type=0, bit_complexities=True, memory_access=3)
Algo = MQE.algorithms()[1]
print(Algo.complexity_type, Algo.bit_complexities, Algo.memory_access)
```

    0 True 3


To see the `bit_complexities` value of all the algorithms to estimator MQE we run `MQE.bit_complexities`. Similarly `for complexity_time` and `memory_access`.


```python
MQE.bit_complexities
```




    [True, True, True, True, True, True]



One can also just apply modify the configuration of one or several algorithms. 

In the following example, we set $d=1$ and $D=3$ the optimal parameters of the `Crossbred` algorithm; we left the other untorched the optmizations of the other algorithms


```python
from cryptographic_estimators.MQEstimator import MQEstimator
MQE = MQEstimator(n=20, m=20, q=3)
```


```python

```


```python
MQE.crossbred.set_parameters({'d':1, 'D':3})
```


```python
MQE.table(show_all_parameters=True)
```

    +------------------+----------------------------------------------------+
    |                  |                      estimate                      |
    +------------------+-------+--------+-----------------------------------+
    | algorithm        |  time | memory |             parameters            |
    +------------------+-------+--------+-----------------------------------+
    | BooleanSolveFXL  |  37.8 |   14.0 | {'k': 19, 'variant': 'las_vegas'} |
    | Crossbred        |  33.5 |    9.9 |      {'d': 1, 'D': 3, 'k': 6}     |
    | ExhaustiveSearch |  33.5 |   14.0 |                 {}                |
    | F5               |  45.2 |   39.7 |                 {}                |
    | HybridF5         |  38.2 |   14.0 |             {'k': 15}             |
    | Lokshtanov       | 111.2 |   33.2 |          {'delta': 1/20}          |
    +------------------+-------+--------+-----------------------------------+


### 4.1. Fastest algorithm

The method `fastest_algorithm()` returns an estimator of the algorithm with the minimum time complexity for the specific import problem


```python
from cryptographic_estimators.MQEstimator import MQEstimator
MQE = MQEstimator(n=20, m=20, q=3)
F = MQE.fastest_algorithm()
F
```




    Crossbred estimator for the MQ problem with 20 variables and 20 polynomials




```python
F.time_complexity()
```




    31.051489520604672

