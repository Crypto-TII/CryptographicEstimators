# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.5] - 2024-06-13

### Added

- Release v1.3.1.
- Changes to the deployment pipelines.
- Uov input dictionary.
- Add lading page.
- Add input dictionary of minrank estimator.

### Changed

- Set default of matrix multiplication constant (w) in mq webapplication.
- Uov input dictionary.
- Update readme with new estimators.
- Merge develop.

### Fixed

- Build doc in the docker.

## [1.0.4] - 2024-04-25

### Added

- Release v1.3.0 (#129).

### Changed

- Drop sage in mqalgorithms dinur1.
- Drop sage in mqalgorithms f5.
- Drop_sage_in_mq_algorithms_cgmta.

## [1.0.3] - 2024-04-24

### Added

- Adding brutefore algorithm for minrank estimator.
- Minors algorithm for the mrestimator.
- Add input dictionary for the minrank estimator.
- Add regular sd estimator to gui.
- Add sd attack and tests.
- Added regularisd and ccj algorithm.
- Add time/memory complexity for intersection_attack.
- Add time_complexity for collision_attack.
- Added first version, untested.
- Add kipnis-shamir time/memory complexity.
- Release v1.2.0.
- Implement expected_number_of_solutions.
- Implement hashes_to_basic_operations.
- Allow only for n > m in uovproblem class.
- Add to_bitcomplexity_time/memory functions.
- Direct attack for uov.
- Minrank estimator only with sm algorithm.
- Add support minors algorithm.
- Minrank base algorithm class.
- Mrestimator structure and mrproblem.
- Add documentation.
- Add attack_type and estimator_type for uov.
- Attack_type column in estimation_renderer.
- _table_problem and _table_scheme methods.
- Add attack_type/estimator_type attributes.
- Restrict ell value in bjmm to likely range.

### Changed

- Merge helper functions minors mr algorithm.
- Edit doc of minrank bruforece.
- Messages to the user.
- Input_dictionary_template.
- Fix code smells and tests.
- Adding variant class to support_minors.
- Set default w=2.81.

### Fixed

- Remove duplicated file.
- Doc.
- Implement pr comments.
- Fix default_value to be number in type selector fields.
- Remove regsd gui (#115).
- Remainig algorithms.
- Intersection attack.
- Minor correction in uov_estimator tests.
- Update uov_estimator test and minor corrections in complexities.
- Fixing doctest in kernelsearch.
- Sd stern behaviour for multiple solutions.
- Fixing some tests and comments.
- Fixing conflicts.
- Renaming some function names.
- Time complexity estimation of support-minors.
- Update uov test.
- Disable variable ranges once parameters are preset.
- Method ncols_in_preprocessing_step method in crossbred.
- Fix typo in run-pytest-and-sonarcloud.yml.
- Set update-changelog workflow to run only after merge to main has been completed.
- Specify on branch push for testing the update-changelog workflow.
- Set workflow to run only after merge to main has been completed.
- Specify on branch push for testing the workflow.
- Generate documentation with estimators-lib image.
- Pr comments/issuses.
- Directattack mqestimator constructor and complexity methods.
- Typo in documentation.
- Paths in tests_mq.py.

## [1.0.2] - 2023-11-24

### Changed

- Remove condition for the system to be non-underdefined.
- Self._ncols --> self._ncols_at_degree_dreg.
- Remove test mq.py.
- Speeding up lokshtanov.

### Fixed

- Fixed complexity formula without considering field equations.
- Case n = 1.
- Adapting doc test.
- Unnecesary factor of n in time complexity.

## [1.0.1] - 2023-03-30

### Fixed

- Add the missing estimator imports
- Fix the SDFq name with the right casing

## [1.0.0] - 2023-03-30

### Added

- Implemented Binary Syndrome Decoding Problem
- Implemented Syndrome Decoding Problem over larger fields
- Implemented Mulivariate Quadratic Problem
- Implemented Permuted Kernel Problem
- Implemented Linear Equivalence Problem
- Implemented Permutation Equivalence Problem

[1.0.5]: https://github.com/Crypto-TII/CryptographicEstimators/compare/v1.0.5..v1.0.4
[1.0.4]: https://github.com/Crypto-TII/CryptographicEstimators/compare/v1.0.4..v1.0.3
[1.0.3]: https://github.com/Crypto-TII/CryptographicEstimators/compare/v1.0.3..v1.0.2
[1.0.2]: https://github.com/Crypto-TII/CryptographicEstimators/compare/v1.0.2..v1.0.1
[1.0.1]: https://github.com/CRYPTO-TII/CryptographicEstimators/compare/v1.0.1..v1.0.0
[1.0.0]: https://github.com/CRYPTO-TII/CryptographicEstimators
