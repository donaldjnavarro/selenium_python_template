# Python Selenium Template

## Setup

* chromedriver is in PATH

### .env - Secrets and non-version controlled data

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

We have standardized the launching of our tests in a poetry script that handles running our tests.

This is implemented via **Poetry Scripts** in */scripts/run_tests.py* and *pyproject.toml*'s `[tool.poetry.scripts]`

```bash
poetry run test
```

This runs pytest, which will run ALL tests in the */test/* folder

> Note: Technically this command will run all files you named with the *test_\*.py* namescheme, but placing these files  outside of the designated folder will throw Pytest warnings.

The best approach is to use the above command, but `pytest` alone will generally work as well. However running test files directly with `python tests/test_example_api.py` will not work, as Pytest fixtures have been incorporated.

#### Running Specific Tests

##### Running tests by filename

If you only want to run a specific test, you can do so by naming the test file at the end of the command:

```bash
poetry run test tests/test_example_api.py
```

> **NOTE:** This works because our run script passes your arguments in to the pytest command it uses internally.

##### Running tests by marker

By adding a pytest marker line above a test's def, you can mark as part of a set of tests that we can run with a single command.

```python
@pytest.mark.marker_flag_example
```

By adding the following argument when we send the test command, only tests with `marker_flag_example` would be run:

```bash
-m "marker_flag example
```

#### Browser specific handling

By default, Pytest will use its fixtures to all tests and then continue to the next web browser and run all the tests again.

## Overview

### Package Management

Poetry with *pyproject.toml* handle the package dependencies.

```bash
poetry install
```

#### Adding packages (Basic Poetry usage)

To add a new package tothe project:

1. Add it to *pyproject.toml* dependencies array
2. Run `poetry lock`
3. Run `poetry install`
4. Commit and submit the contribution without sneaking in other changes to the lock file

### Automation Framework

**Web browser automation:** Selenium

**API automation:** Python's request package

### Testing Framework

**Test execution:** Pytest

**Assertions:** Pytest

For more details, see the Usage section above.

### Linting

We are currently using the **Ruff** library for linting

Our Poetry scripts have standardized ruff usage for our project's needs:

To check for linting issues:

```bash
poetry run lint
```

To have ruff fix the issues it finds, use the command:

```bash
poetry run lint_fix
```

To have ruff fix issues of a specific rule (In this example, Ruff rule I001), use the command:

```bash
poetry run lint_fix_rule I001
```

### CICD Checks

Github Actions are configured to require certain checks pass before a Pull Request is considered valid.

Details are configured in *.github\workflows\selenium.yml*

#### Skipping tests that use secrets

To provide a more secure CICD implementation, we have handling that will skip any test that uses secrets.

We accomplish this by placing a marker on any test that includes credentials or sensitive secrets that we do not want to expose.

```python
@pytest.mark.secrets
```

Placing this line above any test def will cause it to be skipped if the *.env* file has `SKIP_SECRETS=true`.

In *conftest.py* hooks, we skip tests based on this marker and the .env configuration.

#### Skipping browsers that cannot run headless

Currently Selenium's Gecko handling cannot pass the headless flag into Firefox because its compatibility is behind. So we are currently using environmental variables in *.github\workflows\selenium.yml* to make CI skip Firefox coverage.

This is an undesirable approach, but for the purposes of the CI checks the remaining 2 browsers should be sufficient. The full coverage testing should be done by a human tester on a local machine with headed browsers.

### Test Output

#### Reducing Terminal Output

The *run_test* script includes handling for limiting and focusing the test output that is sent to the terminal, which otherwise can be excessively verbose.

To activate this quieter terminal output approach, update the *.env* file `QUIET=true`

If, instead, you prefer to use your own approach of pytest flags, you can always pass pytest arguments to the test running command.

### Max Wait Times

An important aspect to UI testing is that the UI responds to our actions in a timely manner.

While our tests need to wait a reasonable amount of time for web UI to update, we also cannot wait indefinitely without losing failures related to performance.

Our approach to this, includes a set of methods in *utils/timing.py*, the centerpiece of which waits for an assertion that tests provide, so that we can define the specific thing that indicates we are dont waiting - We dont try to move on too early, but also don't wait for longer than we needed to.

To prevent these waits from waiting indefinitely when the expected conditions are never met, or waiting too long and concealing performance issues that we want to be informed about, we define a max threshold.

In the *.env* file, use `MAX_WAIT=` to define the maximum amount of seconds any wait will use. This can be adjusted based on business requirements, or set by a tester for a window determined to be reasonable (Common on environments where performance is not being tested)

### Parallel Automation

In an effort to speed up test runs, we have enabled pytest to run tests in parallel.

This is turned on in the .env file with `PARALLEL=true`.

> **NOTE:** Not all projects are suitable for parallel testing.
> An example where this needs to be avoided would be testing a website
> that uses a login and permanently modifies existing data. Since we
> need our tests to have confidence in the starting state of the product
> being tested, having multiple tests interacting with the system
> may lead to unstable test results.

> **NOTE:** Due to some technology limitations, logs won't display when the parallel flag
> is on. Later we will either solve this, or as a compromise add logging to a local file.
