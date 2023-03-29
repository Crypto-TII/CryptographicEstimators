## Project structure
This the current project structure. 
```sh
── cryptographic_estimators
│   ├── base_algorithm.py
│   ├── base_estimator.py
│   ├── base_problem.py
│   ├── helper.py
│   ├── MQEstimator
│   │   ├── degree_of_regularity.py
│   │   ├── mq_algorithm.py
│   │   ├── MQAlgorithms
│   │   ├── mq_estimator.py
│   │   ├── mq_helper.py
│   │   ├── mq_problem.py
│   │   ├── series
│   │   └── witness_degree.py
│   └── SDEstimator
│       ├── sd_algorithm.py
│       ├── SDAlgorithms
│       ├── sd_estimator.py
│       ├── sd_helper.py
│       └── sd_problem.py
```
If you want to add a new estimator please run `make add-estimator` and it will create the basic code and folder structure for you to edit, you also can review the `DummyEstimator` to see a minimal reproduction of whats its needed to start. 

````python
── cryptographic_estimators
 │   ├── base_algorithm.py
 │   ├── base_problem.py
 │   ├── base_estimator.py
 │   └── NEWEstimator
 │      ├── NEWestimator.py (Inherits from base_estimator)
 │      ├── NEWproblem.py (Inherits from base_problem)
 │      ├── NEWalgorithm.py (Inherits from base_algorithm)
 │      └── Algorithms
 │          ├── List of algorithms (Inherits from NEWalgorithm.py)
````
---
## GIT Conventions
### Commits
To contribute to this project please follow the [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/).

### Branching
Branch names should be snake_case. Which means that all the text must be lowercase and replace spaces with dashes. Also we should add as a prefix based on the type of implementation. For example:

```
poc/some_testing_branch 
refactor/modify_base_problem
feature/implement_dummy_estimator
fix/algorithm_parameter
```

### Pull request
  1. Only create pull requests to the `develop` branch.

---

### Testing
#### Unit tests
To build and run the image based on Dockerfile.test
```sh
make test
```
or if you have Apple Silicon M1 Chip
```sh
make test-m1
```

### Documenting
Remember to document your code using [sphinx syntax](https://www.sphinx-doc.org/en/master/tutorial/automatic-doc-generation.html).


