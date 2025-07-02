# Documentation Commands

This page describes the Makefile commands available for generating and managing the project's documentation.

## Overview

The CryptographicEstimators library uses Sphinx to generate HTML documentation from docstrings and RST files. The documentation generation process involves several steps that can be run individually or as a complete pipeline.

## Local Documentation Generation

### Complete Documentation Build

To generate the complete HTML documentation locally:

```bash
make doc
```

This command runs the full documentation pipeline:
1. Cleans previous documentation builds
2. Creates Sphinx configuration
3. Generates RST files from docstrings
4. Builds HTML documentation

### Individual Steps

If you need to run individual steps of the documentation generation process:

#### Clean Documentation Build Files
```bash
make clean-docs
```
Removes all generated documentation files and build artifacts.

#### Create Sphinx Configuration
```bash
make create-sphinx-config
```
Initializes a new Sphinx configuration for the project.

#### Generate RST Files
```bash
make create-rst-files
```
Creates RST (reStructuredText) files from the library's docstrings using the `scripts/create_documentation.py` script.

#### Build HTML Documentation
```bash
make create-html-docs
```
Builds the final HTML documentation from RST files using Sphinx.

## Docker Documentation Generation

For systems where installing Sphinx and documentation dependencies might be challenging, you can generate documentation using Docker:

```bash
make docker-doc
```

This command:
1. Builds a Docker image with all documentation dependencies
2. Mounts the documentation directory as a volume
3. Runs the complete documentation generation process inside the container
4. Cleans up the container after completion

The generated documentation will be available in `docs/build/html/` and can be viewed by opening `docs/build/html/index.html` in a web browser.

## Documentation Structure

The generated documentation includes:
- API reference for all estimators and algorithms
- User guide and examples
- Code documentation extracted from docstrings
- Cross-references between related components

## Notes

- The documentation generation process requires the library to be installed (either in development mode or via pip)
- RST files are automatically generated from docstrings, so keeping docstrings up-to-date ensures accurate documentation
- The Docker variant is particularly useful for CI/CD pipelines or systems with limited package management options 