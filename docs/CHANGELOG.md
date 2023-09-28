# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.1] - 2023-09-05

### Smaller bugfixes

- updated readme with links to user guide and web application
- added sonarcloud checks and fixed corresponding bugs

## [1.1.0] - 2023-08-30

### New Features
- Added new [TMTO for BJMM](https://eprint.iacr.org/2022/1329) in the SDEstimator
- Added [user guide](https://github.com/Crypto-TII/CryptographicEstimators/blob/develop/docs/CONTRIBUTING.md)
- Added [developer guide](https://github.com/Crypto-TII/CryptographicEstimators/blob/develop/User_Guide.ipynb)
- MQAlgorithms follows convention

### Restructuring

- Decoupled printing routine from base estimator class
- Introduced templates for new estimator generation

### Fixes affecting Estimates
- fixed number of solutions for SDFq problem (according to the [official comment to SDitH](https://groups.google.com/a/list.nist.gov/g/pqc-forum/c/d_BcUfFGl5o/m/zy7pGkTAAQAJ) in the NIST PQC forum). This also affects the PKEstimator, LEEstimator and PEEstimator. 
- fixed the computation of memory access costs. The time complexity is now calculated as T = #B_op * T_op + #B_op * f(M), where #B_op is the amount of basic operations, T_op the bit complexity per basic operation and f(M) the memory access cost associated with one basic operation.

### Smaller bugfixes

- updated readme
- fixed failing GUI for PKEstimator
- fixed several float overflows due to implicit conversion
- 
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

[1.0.1]: https://github.com/CRYPTO-TII/CryptographicEstimators/compare/v1.0.1..v1.0.0
[1.0.0]: https://github.com/CRYPTO-TII/CryptographicEstimators
