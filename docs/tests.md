# Tests

## Testing Suite Architecture and Guide

This documentation provides an overview of the testing architecture for our
Python library, which employs two types of tests: **regression tests** and
**doctests**. Both types are powered by pytest, with doctests **(WIP)** being
specifically based on Python's doctest module.

### Regression Tests

This guide will focus on the architecture and implementation of **regression
tests**, which are designed to streamline the testing process through
precomputations and eliminate the dependency on Sagemath for the end user.

#### Testing Phases and Directory Structure

The regression testing architecture consists of three phases, each corresponding
to a specific directory within the `tests/` directory:

1. **Generating Expected Outputs:**

   - The `references/` directory stores **generator** functions for producing
     the expected outputs of the estimators.
   - Each estimator has a dedicated subdirectory under `references/`, e.g.,
     `<estimator_name>Estimator/`.
   - Inside the estimator's subdirectory:
     - `legacy_implementations/` (optional): Contains previous implementations
       of the estimator.
     - `gen_<estimator_name>.py`: Houses the generator functions.

   Generator functions must adhere to the following conventions: - They start
   with the prefix `gen_`. - They have a single parameter named `inputs`, which
   can be either a single test case (tuple) or a tuple containing information to
   generate multiple test cases. - They return a list of tuples, where each
   tuple is of the form `(input, expected_output)`.

2. **Defining Test Inputs:**

   - The `tests/references/references_inputs.py` file holds the
     `REFERENCES_INPUTS` dictionary.
   - This dictionary mirrors the file structure of the `references/` directory
     and specifies the inputs for the generator functions.
   - To add a new estimator and its inputs, follow this structure within the
     dictionary:

   ```python
   REFERENCES_INPUTS = {
       "<estimator_name>Estimator": {
           "gen_<estimator_name>": {
               "gen_<estimator_name>_<function_name_1>": {
                   "inputs": [(256, 128, 64, 251), (961, 771, 48, 31)]
               },
               # Add more functions as needed...
           },
       },
       # Add more estimators as needed...
   }
   ```

   After defining the inputs, run the following command from the library root to
   generate the reference values:

   ```bash
   make docker-generate-tests-references
   ```

   **Warning:** This command creates a Docker container with SageMath installed,
   which may take some time to run.

   The generated inputs and their corresponding outputs will be serialized in
   `tests/references/reference_values.yaml`.

3. **Implementing Tests:**

   - The `tests/validations/` directory contains the test implementation files.

   - Each estimator has a corresponding file named `test_<estimator_name>.py`.

   - For each generator function (`gen_<estimator_name>_<function_name>`) in
     `references/`, there must be a corresponding test function named
     `test_<estimator_name>_<function_name>` in the validation file.

   - Each test function:

     - Takes a single parameter, `test_data`, automatically provided by _pytest_
       and containing the input/output pairs from the `reference_values.yaml`
       file.
     - The boilerplate code is expected to have the following structure:

     ```python
     def test_<my_estimator>_<my_function>(test_data):
         """
         Test for the ... problem with an error tolerance of epsilon.
         """
         inputs_with_expected_outputs = test_data()
         epsilon = 0.01

         def test_single_case(input_with_exp_output):
             input, expected_complexity = input_with_exp_output
             # ... Calculate actual_complexity
             actual_complexity = ...
             assert abs(actual_complexity - expected_complexity) < epsilon

         map(test_single_case, inputs_with_expected_outputs)
     ```

### Doctests (with pytests)

TODO

## Writing Doctests

Throughout the CryptographicEstimators library we are using
[sage doctests](https://doc.sagemath.org/html/en/developer/doctesting.html).
These tests are then automatically run by our
[CI](https://github.com/Crypto-TII/CryptographicEstimators/actions) to check for
any errors.

We strongly encourage to write examples for all optimization parameters of an
algorithm. In the case our `DUMMYAlgorithm1` one could extend the optimization
parameter `h` like this:

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

Note the newlines around `EXAMPLES::` and in the end. These are mandatory. Also
note the commands the test framework is executing, are starting with `sage: `
and the expected result is written below the last command (`50`).

Additionally, it is mandatory to also test all algorithms at least once in the
corresponding `Estimator` class. E.g. in our case we extend the function
`table()` of the `DUMMYEstimator` to

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

Again note the new lines around `TESTS:` and the end of the test. Additionally,
notice the `# long test` at the end of the last command. You can add this if the
command takes a great amount of time, and you do not want to run the test to run
on every change you make, but rather only on every commit. Tests missing the
`# long test` are always executed. Make sure there is at least one example or
test for the table function that executes fast and, hence, is not marked as long
test via `# long time`. This ensures that the `make testfast` command has a good
coverage while still executing in reasonable time which can be very helpful
while integrating code into the library.

If you incorporated an existing estimator to the CryptographicEstimators library
we strongly encourage to load the old estimator as a module into `test/module`
and write unit tests comparing the estimation results of the newly incorporated
estimator against the online available code. An example for such an integration
test can be found under `tests/test_le_bbps.sage`. Its important that all tests
functions start with a `test_`.

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

### Difference between `_compute_time_complexity(...)` and `time_complexity(...)`

The first one returns the time for a given set of parameters in number of basic
operations, while the second initiates a search for the optimal parameters and
converts time to bit operations if specified, includes memory access costs etc.

## Testing the Frontend

After you finished implementing your estimator, you may want to export it to the
[webfrontend](https://github.com/Crypto-TII/cryptographic_estimators_ui). See
[this](https://github.com/Crypto-TII/cryptographic_estimators_ui/blob/main/docs/INPUTDICTIONARYGUIDE.md)
guide for the details of the configuration possibilities.

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

Notice that you do not have to specify any algorithm in this configuration file.
As this is all done automatically.
