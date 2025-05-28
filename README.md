# Python Selenium Template

## Package Management

Poetry with *pyproject.toml* handle the package dependencies.

```bash
poetry install
```

## Prerequisites

* chromedriver is in PATH

## .env - Secrets and non-version controlled data

The .env file is not version controlled so that we can store secrets and anything that you want to be user specific.

To get started, copy the *.env.template* file and remove the *.template* from the filename. This will provide you with a starting point, and a map of the expected variable names.

> NOTE: This means that any additional variables added to the *.env* file should also have their names added to the *.env.template* file

## Usage

### Cleaning up old installations

```bash
poetry env remove python
```

### Installing packages and dependencies

```bash
poetry install
```

### Running Tests

```bash
poetry run pytest
```

This runs pytest, which will run all the tests in the */test/* folder (Or any files you named with the *test_\*.py* namescheme, but these existing outside of the designated folder will throw warnings.)
