<div align="center">
    <img src="https://github.com/user-attachments/assets/bbe49f32-5e62-49a7-bb41-b28f1864833d" alt="estimators-logo" width=100 height=100></img>
</div>

# CryptographicEstimators

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Crypto-TII_CryptographicEstimators&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Crypto-TII_CryptographicEstimators)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=Crypto-TII_CryptographicEstimators&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=Crypto-TII_CryptographicEstimators)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=Crypto-TII_CryptographicEstimators&metric=bugs)](https://sonarcloud.io/summary/new_code?id=Crypto-TII_CryptographicEstimators)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=Crypto-TII_CryptographicEstimators&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=Crypto-TII_CryptographicEstimators)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=Crypto-TII_CryptographicEstimators&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=Crypto-TII_CryptographicEstimators)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Crypto-TII_CryptographicEstimators&metric=coverage)](https://sonarcloud.io/summary/new_code?id=Crypto-TII_CryptographicEstimators)

## Introduction 🎉

This library provides bit complexity estimators for cryptographic problems, as
well as some cryptographic schemes. Currently, the implemented estimators are:

- ### Problem Estimators
  - Multivariate Quadratic
  - Binary Syndrome Decoding
  - Syndrome Decoding over Fq
  - Permuted Kernel
  - Permutation Equivalence
  - Linear Equivalence
  - MinRank
  - Regular Syndrome Decoding
  - Rank Syndrome Decoding

- ### Scheme Estimators
  - [BIKE](https://bikesuite.org)
  - [MAYO](https://pqmayo.org)
  - [UOV](https://www.uovsig.org)

## Getting Started 🚀

This project is designed to be run through a terminal as a Python package. You
can also access the estimators through [this](https://estimators.crypto.tii.ae/)
user friendly and installation-free web application.

### Prerequisites ✔️

You need to have `python3`, `make` and `git` installed on your machine.

**Optional:** If you want to install the package in an isolated
[Python virtual environment](https://docs.python.org/3/library/venv.html), run
the next commands before the installation process:

```shell
python3 -m venv .venv
source .venv/bin/activate
```

### Installation 🛠

- Clone and `cd` into the project directory.

- Run `make install` to install the `cryptographic_estimators` library locally.

  _Note:_ If you encounter some permission error, please try creating a virtual
  environment with the steps mentioned in the
  Prerequisites section in this document, so you don't need
  to use `sudo` to interact with python/pip related commands.

### Running the project ✈️

Open the Python interpreter in a terminal and import the library as shown in the
following example:

```python
>>> from cryptographic_estimators.SDEstimator import SDEstimator
>>> SD = SDEstimator(n=15, k=10, w=5)
>>> SD.table()
```

## Documentation 📝

- A user guide can be found [here](./docs/github/user_guide.md).

- Reference documentation for the library estimators can be found online
  [here](https://crypto-tii.github.io/CryptographicEstimators/), or be generated
  locally with the command `make doc` or `make docker-doc` (see at
  `docs/build/html/index.html` after successful generation).

## Contributing 🤝

Thank you for considering contributing to our project. We thrive on community
involvement and warmly welcome your contributions.

### Where to begin 🌱

1. **Explore Open Issues**: If you're looking for a place to start, check out
   our [open issues](https://github.com/Crypto-TII/CryptographicEstimators/issues). There might be something that catches your
   interest!

2. **Read the Contribution Guide**: Before submitting a pull request, please
   take a moment to review our
   [Contribution Documentation](./docs/github/contributing.md). It contains
   important information about our development guidelines and process.

3. **Ask for Help**: Stuck on something? Don't hesitate to reach out! You can:

- Start a
  [new discussion](https://github.com/Crypto-TII/CryptographicEstimators/discussions)
- Open a
  [new issue](https://github.com/Crypto-TII/CryptographicEstimators/issues)
- [Contact us directly](https://github.com/Crypto-TII/CryptographicEstimators?tab=readme-ov-file#contact-%EF%B8%8F)

Every contribution, big or small, is valued and appreciated. Whether you're
fixing a typo, improving documentation, or adding a new feature, your efforts
help make this library better for everyone. We look forward to collaborating
with you!

## Contact 🖊️

If you need any help about contributing to this project feel free to contact us
at `cryptographic_estimators at tii.ae`
