# Tests

## Testing Suite Architecture Overview

This section provides an overview of the testing architecture for our Python
library, which employs two types of tests: **regression tests** and
**doctests**. Both types are powered by pytest, with doctests **(WIP)** being
specifically based on the Python's doctest module.

## Regression Tests: Understanding the Process

At its core, our regression testing framework is designed to ensure that any
changes made to the library don't inadvertently break existing functionality.
Unlike doctests, which focus on individual components in isolation, regression
tests take a broader approach by comparing the output of entire estimators
against pre-computed expected results.

This approach brings a significant advantage: **improved testing times.**
Running each regression test, which often involves complex computations, can be
very time-consuming. To optimize this process, we serialize expected outputs on
predefined inputs. These serialized results are then used in subsequent test
runs for efficient comparisons, saving valuable time during development.

Here's a breakdown of how it works:

1. **Generating Expected Outputs:** For each estimator, we have specialized
   generator functions that take defined input values and produce the expected
   outputs. These generator functions are grouped by estimator and found in the
   `tests/references/` directory. The generated outputs are then serialized to
   be later used in the testing process.

2. **Storing Test Inputs:** To maintain consistency, all input values used by
   the generator functions are centrally defined in the `REFERENCES_INPUTS`
   dictionary within `tests/references/references_inputs.py`. This ensures that
   every test execution utilizes the same, controlled input data.

3. **Executing Tests:** The actual test cases reside in the `tests/validations/`
   directory, with each estimator having a dedicated file
   (`test_<estimator_name>.py`). These test functions fetch input/output pairs
   from a YAML file (which was pre-populated using the generator functions and
   input data), execute the estimator's code, and compare the actual results
   against the expected values.

This separation of concerns makes it easier to maintain and extend the test
suite as we introduce new estimators or modify existing ones.

### Writing Tests: A Step-by-Step Guide

This guide will walk you through the process of adding a new regression test to
our Python library. We'll assume you're already familiar with Python, pytest,
and the basic structure of our estimators.

#### 1. Create Your Generator Function

- Create a new Python file (`gen_<your_new_estimator>.py`) within the
  `tests/references/<YourNewEstimator>Estimator/` directory.
- Define your generator function that will produce expected outputs based on the
  provided inputs. Adhere to the naming convention
  (`gen_<your_new_estimator>_<test_function_name>`)

```python
def gen_<your_new_estimator>_<your_test_function_name>(inputs):
    # ... logic to generate expected outputs based on inputs
    return [(input_1, expected_output_1), (input_2, expected_output_2), ...]
```

**Notes:**

- While not mandatory, most generator functions are expected to receive a list
  of tuples as input, with each tuple representing the inputs for one test case.
- It **is mandatory** that each generator function returns a list of tuples.
  Each tuple should correspond to the input and expected output for a single
  test case.

#### 2. Define Your Input Data

- Navigate to the `tests/references/references_inputs.py` file.
- Locate the `REFERENCES_INPUTS` dictionary.
- Add an entry for your new estimator (or locate the existing one) and define
  the specific inputs you'll be testing.

```python
REFERENCES_INPUTS = {
    # ... other estimators ...
    "<YourNewEstimator>Estimator": {
        "gen_<your_new_estimator>": {
            "gen_<your_new_estimator>_<your_test_function_name>": {
                "inputs": [(input_value_1, input_value_2, ...),  (...), ...] # Your input tuples here
            },
            # Add more functions as needed...
          },
    },
    # ... more estimators...
}
```

**Note:**

The structure of this nested dictionary directly maps to the file path of the
generator function, starting from the
`CryptographicEstimators/tests/references/` directory.

For example, the entry above indicates that in the file located at:
`CryptographicEstimators/tests/references/<YourNewEstimator>Estimator/gen_<your_new_estimator>.py`,
there's a function named `gen_<your_new_estimator>_<your_test_function_name>`.
This function will be executed using the provided list of input tuples.

#### 3. Generate Reference Output Values

> :warning: **Warning:** This step might take a while as it builds and runs a
> Docker container with SageMath.

- From the library root, run the Docker command to generate the reference values
  based on your provided inputs and the new generator function:

  ```bash
  make docker-generate-tests-references
  ```

- This updates `tests/references/reference_values.yaml`, which now includes your
  new estimator's expected outputs.

#### 4. Implement the Test Function

- In the `tests/validations/` directory, locate the file for your estimator
  (`test_<your_new_estimator>.py`) or create it if it doesn't exist.

- Add a test function that directly corresponds to your generator function,
  adhering to the naming convention
  (`test_<your_new_estimator>_<test_function_name>`).

- The test function will:

  - Receive test data (input/output pairs) from the `reference_values.yaml`
    file.
  - Execute your estimator's logic using the input values.
  - Compare the actual results against the expected outputs from the reference
    data.

```python
def test_<your_new_estimator>_<your_test_function_name>(test_data):
    """
    (Optional) Docstring to describe the test case
    """
    inputs_with_expected_outputs = test_data()
    epsilon = 0.01 # Or an appropriate tolerance for your estimator

    def test_single_case(input_with_exp_output):
        input, expected_output = input_with_exp_output
        # ... Use the 'input' to calculate your estimator's  actual_output
        actual_output  = ...
        assert abs(actual_output - expected_output) < epsilon

    map(test_single_case, inputs_with_expected_outputs)
```

#### 5. That's all

After following these steps, your new test case will be integrated into our
testing framework. You can run the tests using our test-related `make` commands,
or manually execute `test_<your_new_estimator>.py` using pytest.

## Doctests (with pytests)

TODO

## Writing Doctests (with sage doctests)

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
