# Tests

## Testing suite architecture overview

This section provides an overview of the testing framework for our Python
library, which employs two main testing approaches:

- **Known Answer Tests (KATs):** These tests verify the accuracy of the
  estimates made by the CryptographicEstimators library. Here one compares the
  estimates by CryptographicEstimators with the one of existing external
  estimators which are widely accepted as correct by the cryptographic
  community.

- **Doctests:** These tests live within the code's docstrings, serving a dual
  purpose. They illustrate how to use functions and classes through practical
  examples, while simultaneously ensuring the code behaves as documented.

Both KATs and Doctests are powered by the `pytest` framework. Doctests,
specifically, leverage Python's built-in `doctest` module.

## KAT tests

### Understanding the process

A Known Answer Test (KAT) in cryptography involves comparing the output of an
algorithm implementation against a set of publicly available parameters and
expected values. These expected values serve as reference points for
correctness. This KAT testing framework uses this approach to ensure that any
modifications to the library do not disrupt existing functionality.

Importantly, while pre-calculated parameters and values are common, some
researchers provide source code (estimators) for their estimates, serving as
**KAT generators**. These generators allow for dynamic KAT value generation.

Unlike isolated doctests, KATs take a more comprehensive approach by comparing
outputs across entire estimators, often involving complex and computationally
intensive operations. To optimize this process, we serialize expected outputs
for specific predefined inputs. These serialized results streamline subsequent
test runs, enabling efficient comparisons and saving valuable development time.

Here's a breakdown of how our KAT testing process works:

```mermaid
flowchart LR;
  katgen("`KAT Generators`")
  inputs("`Inputs`")
  preeo("`Precompute expected outputs`");
  ser("`Serialize and store inputs/expected outputs`")
  estimator("`Library estimation`")
  oc("`TEST:
    Outputs comparison`")

  katgen --> preeo;
  inputs --> preeo;
  preeo --> ser;
  ser -- inputs --> estimator;
  estimator -- actual output --> oc;
  ser -- expected output --> oc;
```

1. **KAT Generator Functions:** We utilize KAT generator functions located in
   the `tests/external_estimators` directory. These functions have hardcoded
   inputs as they are not intended for regular modification. Both input
   parameters and their corresponding outputs (referred to as `expected_outputs`
   as they act as reference values) are serialized into the `tests/kat.yaml`
   file for later use during estimator testing.

2. **Internal Estimation Functions:** With a collection of inputs and their
   expected outputs, we define how these inputs should be processed within our
   library in order to match the configuration of the external estimator. This
   is achieved through internal estimation functions found in the
   `tests/internal_estimators` directory. Each function corresponds to a KAT
   generator in `tests/external_estimators`.

3. **Test Execution and Comparison:** In the final step, we execute all our
   internal estimation functions using the serialized inputs from
   `test/kat.yaml`. The calculated outputs are then compared against the
   expected outputs from the KAT generators to verify the accuracy of the
   CryptographicEstimators library.

This separation of concerns makes it easier to maintain and extend the test
suite as we introduce new estimators or modify existing ones.

### Writing KAT tests: A step-by-step guide

This guide walks you through incorporating a new KAT test for a library
estimator, offering insights relevant for both understanding and updating
existing tests.

#### 1. Define your KAT generator function

This step involves defining or declaring the KAT generator functions which
produces the expected outputs from hardcoded inputs. These functions are
wrappers of external estimators of the complexity of particular algorithms.
Hence, these functions require careful crafting.

- Begin by creating a new file named `ext_<estimator_name>` within the
  `tests/external_estimators/` directory. This file can be written in either
  Sage or Python, as our framework supports both formats.

- Inside this file, define your KAT generator function using the naming
  convention `ext_<algorithm_name>`. These functions contain the logic to
  calculate expected outputs for their predefined inputs.

For example, consider the `ext_lee_brickell` function:

```python
#Defined at ext_sdfq.py
def ext_lee_brickell():
    """Generate expected complexities for Lee-Brickell SDFq problems.

    This function calculates the expected complexities for a predefined set of
    Lee-Brickell SDFq problem parameters.

    Returns:
        list of tuple: Each tuple contains:
            - tuple: Input parameters (n, k, w, q)
            - float: Corresponding expected complexity
    """

    inputs = [(256, 128, 64, 251), (961, 771, 48, 31)]

    def gen_single_kat(input: tuple):
        n, k, w, q = input
        expected_complexity = ... # output of the external estimating the complexity
        # of the lee-brickell algorithm on inputs (n, k, w, q)
        return input, expected_complexity

    inputs_with_expected_outputs = list(map(gen_single_kat, inputs))
    return inputs_with_expected_outputs
```

- **Important:** Each KAT generator function **must** return a list of tuples,
  with every tuple representing a single KAT (input parameters & expected
  output).

#### 2. Generate reference KAT values

> :warning: **Warning:** This step might take a while as it builds and runs a
> Docker container with SageMath.

- From the library root, run the following Docker command to generate the
  reference KAT values. These are generated based on your KAT generator
  functions and their hardcoded inputs.

  ```bash
  make docker-generate-kat
  ```

- This process creates or updates the `tests/kat.yaml` file, which will now
  include your defined KAT generator functions with their outputs, organized
  within a dictionary. Note that the `ext_` prefix used in the code is removed
  for easier readability in the YAML file.

#### 3. Implement the Internal Estimation Function

In this step, instead of directly writing test functions, we'll define our
library's internal estimators – functions that mirror the KAT generators but
implement our algorithms. These internal estimators are what we rigorously test
against the KAT values.

- Create a new file in the `tests/internal_estimators` directory with a name
  that matches your KAT generator file from step 1, but without the `ext_`
  prefix. For instance, if you created `tests/external_estimators/ext_sdfq.py`,
  your new file would be `tests/internal_estimators/sdfq.py`.

- Within this new file, define a corresponding internal estimation function for
  each KAT generator function from step 1. Use the same function name but remove
  the `ext_` prefix. For example, `ext_lee_brickell` would have a corresponding
  `lee_brickell` function.

- These internal estimation functions **must** adhere to the following
  structure:

  1. **Parameters:**

     - `input`: A tuple containing the input parameters received from the
       serialized KAT data.
     - `epsilon`: A hardcoded value representing the acceptable error tolerance
       during comparison. This helps account for potential small discrepancies
       arising from different calculation methods or precision levels.

  2. **Returns:**

     - `actual_complexity`: The estimated complexity value as calculated by your
       internal estimator or algorithm.
     - `epsilon`: Returns the same `epsilon` value passed as input. This
       practice maintains consistency and makes it clear that error tolerance is
       being considered.

For example, the `lee_brickell` function would look like this:

```python
def lee_brickell(input, epsilon = 0.01):
    """Estimate produced by the CryptographicEstimators library for the Lee-Brickell SDFq problem.

    This function calculates the complexity estimate for a single case of the Lee-Brickell SDFq problem.

    Args:
        input (Tuple[int, int, int, int]): A tuple containing (n, k, w, q) parameters for the SDFq problem.
        epsilon (float): The maximum error tolerance for this estimation.

    Returns:
        Tuple[float, float]: A tuple containing:
            - float: The actual complexity calculated by the LeeBrickell algorithm.
            - float: The epsilon value used for error tolerance.
    """
    n, k, w, q = input  # Unpack input tuple

    actual_complexity =  ...# Calculate the actual complexity using your library's implementation

    return actual_complexity, epsilon  # Return the calculated complexity and the epsilon
```

#### 4. Run Your Tests

With your KAT generator functions, internal estimator implementations, and
generated reference values in place, you're ready to run your tests! Use the
following command from your library's root directory:

```bash
make docker-pytest
```

Or by manually executing
`pytest tests/validations/test_<your_new_estimator>.py`. The output will
indicate whether your internal estimators align with the expected KAT values
within the defined error tolerance.

## Writing Doctests

Throughout the CryptographicEstimators library we use the
[python doctests](https://docs.python.org/3/library/doctest.html#module-doctest)
module. These tests are automatically run by our
[CI](https://github.com/Crypto-TII/CryptographicEstimators/actions) to check for
any errors.

It is mandatory to test all algorithms at least once in the corresponding
`Estimator` class docstring.

### Syntax

Doctests can be included in any docstring by creating the section `Tests:` at
the end, and writing the testing code blocks for the current method. Ex:

```python
    def _ncols_in_preprocessing_step(self, k: int, D: int, d: int):
        """Return the number of columns involved in the preprocessing step.

        Args:
            k (int): The number of variables in the resulting system.
            D (int): The degree of the initial Macaulay matrix.
            d (int): The degree of the resulting Macaulay matrix.

        Tests:
             >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.crossbred import Crossbred
             >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
             >>> E = Crossbred(MQProblem(n=10, m=12, q=5))
             >>> E._ncols_in_preprocessing_step(4, 6, 3)
             1412

             >>> E = Crossbred(MQProblem(n=5, m=5, q=13))
             >>> E._ncols_in_preprocessing_step(3, 4, 2)
             45
        """
```

Here we are writing _two_ tests on the same _doctest_, each one with a different
set of input values. The expected return of each test corresponds to the line
without the `>>>` prefix.

Notice that once you have imported something, it isn't required to import again
for subsequent calls **on the same doctest**.

### Skipping long doctests

While we **strongly** discourage the introduction of doctests with very long
computation times, as those tests drastically slow our _CI_ as well as
development work cycles; we have developed one feature to mitigating its impacts
from a development perspective.

In any doctest, and in any position, you will be able to use a special block:

```python
>>> if skip_long_doctests:
...     pytest.skip()
```

This allow developers to skip any test declared _after_ the code block by using
a custom Pytest flag.

As illustration, let's take this base doctest

```python
        """
        ...

        Tests:
            >>> E = MQEstimator(n=15, m=15, q=2, w=2)
            >>> E.table(precision=3, truncate=1)
            <... Some result ...>

            >>> if skip_long_doctests:
            ...     pytest.skip()
            >>> from cryptographic_estimators.MQEstimator import MQEstimator
            >>> E = MQEstimator(q=2, m=42, n=41, memory_bound=45, w=2)
            >>> E.table()
            <... Some other result ...>
        """
```

Now we can run our doctest evaluation in two different ways:

1. Running all the tests: `pytest --doctest-modules cryptographic_estimators/`

2. Executing only the fast tests:
   `pytest --skip-long-doctests  --doctest-modules cryptographic_estimators/`

Where the first command will run all the tests inside the given doctest, but the
second one will skip the
`>>> E = MQEstimator(q=2, m=42, n=41, memory_bound=45, w=2)` case.

**Note:** This commands are simpler illustrative versions of the ones included
in our Makefile. Please use `make doctests` and `make doctests-fast` instead for
better performance.

**Make sure** there is at least one docstring example or fast doctest. This
ensures the `make testfast` command has a good coverage while still executing in
reasonable time which can be very helpful while integrating code into the
library.

## Testing the Frontend

After you have finished implementing your estimator, you may want to export it
to the [webfrontend](https://github.com/Crypto-TII/cryptographic_estimators_ui).

The webfrontend is configured via a json file `input_dictionary.json` which is
already contained in this project root directory. This file already contains all
estimators implemented in the CryptographicEstimators framework. To add your new
estimator first run:

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
      "problem_parameters": [
        // This is a list of dictionaries. Where each dictionary relates to an specific field on the UI
        {
          "id": "Parameter1", // Mandatory
          "type": "number", // Mandatory
          "display_label": "Parameter 1", // Mandatory
          // All the rest are optional
          "direction": "", // 'row' (default) or 'column'
          "placeholder": "",
          "default_value": "",
          "tooltip": "This is the first problem parameter"
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
    }
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
          "tooltip": "This is the first problem parameter"
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
          "options": ["Constant", "Logaritmic", "Square root", "Cube root"]
        }
      ],
      "optional_parameters": [] // Different for each estimator, same structure as problem_paramenters
    }
  ]
}
```

Notice that you do not have to specify any algorithm in this configuration file,
as this is all done automatically.
