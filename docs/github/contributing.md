# Contributing Guide

## Development Installation

To contribute to the project, you'll need to install the library in development mode. This allows you to make changes to the code and see them immediately without reinstalling.

1. Clone and `cd` into the project directory:
   ```bash
   git clone <repository-url>
   cd CryptographicEstimators
   ```

2. Run `make install` to install the `cryptographic_estimators` library in development mode (using the `-e` flag with pip):
   ```bash
   make install
   ```

   _Note:_ If you encounter permission errors, consider creating a virtual environment first:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   make install
   ```

## Documentation

To streamline your contribution process, you can use the following pages as you
need:

- Code guidelines
  - [Code conventions](./code_conventions.md)
  - [Adding a new estimator](./add_new_estimator.md)
  - [Tests](./tests.md)
- Documentation guidelines
  - [Docstrings and HTML documentation](./docstrings_and_html.md)
