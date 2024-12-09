# Docstrings and HTML documentation

[Docstrings](https://en.wikipedia.org/wiki/Docstring#Python) are comments at the
start of any class, method or function. By being embedded directly into the
code, they are a practical approach to avoid obsolete documentation.

In the CryptographicEstimators library, docstrings are also used to generate
[HTML documentation](https://crypto-tii.github.io/CryptographicEstimators/).
This requires careful formatting of the docstrings to ensure proper rendering.

Tech stack:

- [Sphinx](https://www.sphinx-doc.org/en/master/index.html) with the
  [Napoleon](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#sections)
  extension enabled.
- We also have a custom extension [kwargs formatter](../kwargs_formatter.py) to
  extend the parsing capabilities of Sphinx.

## Syntax

The docstring syntax used in the library is based on the
[Google Style](https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html),
which allows a concise and clean way to represent all the required information.

A typical docstring should look something as below, but other
[sections](%22https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#docstring-sections%22)
can be included if needed:

```python
class Crossbred(MQAlgorithm):
    def __init__(self, problem: MQProblem, **kwargs):
        """Construct an instance of crossbred estimator.

        The Crossbred is an algorithm to solve the MQ problem [JV18]_. This algorithm consists of two steps:
        the preprocessing step and the linearization step. In the preprocessing step, we find a set S of
        degree-D polynomials in the ideal generated by the initial set of polynomials. Every specialization
        of the first n-k variables of the polynomials in S results in a set S' of degree-d polynomials in k
        variables. Finally, in the linearization step, a solution to S' is found by direct linearization.

        Note:
            Our complexity estimates are a generalization over any field of size q of the complexity formulas
            given in [Dua20]_, which are given either for q=2 or generic fields.

        Args:
            problem (MQProblem): MQProblem object including all necessary parameters.
            **kwargs: Additional keyword arguments.
                h (int): External hybridization parameter. Defaults to 0.
                w (float): Linear algebra constant (2 <= w <= 3). Defaults to 2.81.
                max_D (int): Upper bound to the parameter D. Defaults to 20.
                memory_access (int): Specifies the memory access cost model. Defaults to 0.
                    Choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root.
                    Alternatively, deploy a custom function which takes as input the logarithm
                    of the total memory usage.
                complexity_type (int): Complexity type to consider. Defaults to 0.
                    0: estimate, 1: tilde O complexity.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.crossbred import Crossbred
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = Crossbred(MQProblem(n=10, m=12, q=5))
            >>> E
            Crossbred estimator for the MQ problem with 10 variables and 12 polynomials
        """
```

## Conventions

1. Every method or function in the library should have a docstring. Some
   self-explanatory functions can skip this convention.

2. Every docstring should have a one-liner top description. On some very simple
   methods this one-liner could be enough.

3. If your docstring needs any external reference, please:

- Include your reference in the `references.rst` file at the root of the
  project. You can find examples on how to do it there.

- Include any cite in your docstrings by using the syntax `[XXXX]_` . Ex:
  `[JV18]_` or `[Dua20]_`. This format is parsed by Sphinx to create hyperlinks
  on the HTML documentation.

4. If your method or function supports `**kwargs`, you can document the expected
   named arguments by adding another indentation level, and then following the
   same structure used by normal arguments (look at the example above for
   details).