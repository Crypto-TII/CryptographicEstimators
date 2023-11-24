# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[1.0.2]: https://github.com/Crypto-TII/CryptographicEstimators/compare/v1.0.2..v1.0.1
[1.0.1]: https://github.com/CRYPTO-TII/CryptographicEstimators/compare/v1.0.1..v1.0.0
[1.0.0]: https://github.com/CRYPTO-TII/CryptographicEstimators
