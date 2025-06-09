# Python Selenium Template

## Getting Started

### Secrets and personal configurations

#### Using the .env file

We are using the **.env* file to manage secrets and personal configurations for how you want these tests to behave for an individual execution.

* **Not version controlled:** The .env file is not version controlled so that we can store sensitive secrets such as passwords and API keys. This also prevents personal configurations (Such as whether you want to run in parallel) from being included in commits.

**Getting Started:** To get started, copy the *.env.template* file and remove the *.template* from the filename. This will provide you with a starting point, and a map of the expected variable names.

#### Adding new variables to the .env

Making changes to the .env variables needs to be done in 3 places:

1. **.env** file itself.
2. **.env.template** file so new users have a clear indication of the variable you added.
3. **.github\workflows\selenium.yml** file so that Github Actions generate their virtual .env when running CI tests.

## Using the suite

### Cleaning up old installations

```bash
poetry env remove python
```

### Installing packages and dependencies

```bash
poetry install
```

### Running tests

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
-m "marker_flag example"
```

#### Browser specific handling

By default, Pytest will use its fixtures to all tests and then continue to the next web browser and run all the tests again.

Which browsers are included in this coverage can be customized in the *.env* file

## Overview

### Package Management

**Poetry** with *pyproject.toml* handle the package dependencies.

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

**API automation:** Python's `request` package

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

### CI/CD Checks

**Github Actions** are configured to require certain checks pass before a Pull Request is considered valid.

Details are configured in *.github\workflows\selenium.yml*

#### CI Exclusions: Skipping tests that use secrets

To provide a more secure CICD implementation, we have handling that will skip any test that uses secrets.

We accomplish this by placing a marker on any test that includes credentials or sensitive secrets that we do not want to expose.

```python
@pytest.mark.secrets
```

Placing this line above any test def will cause it to be skipped if the *.env* file has `SKIP_SECRETS=true`.

In *conftest.py* hooks, we skip tests based on this marker and the .env configuration.

#### CI Exclusions: Skipping browsers that cannot run headless

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

### Page Object Models
This repo uses a POM (Page Object Model) approach to structuring the logical details about actions that automation takes.

A few patterns emerge:

* The `models/` folder has all the page model details, and the tests in `tests/` import them as needed
* Each page model consolidates information about a given page: URL, expected page title, etc
  * **Element locators** *(generally XPath)* are all stored at this level. This creates a single location where all the DOM references for a given page can be maintained
  * **Page actions** are standardized as class methods within the page model. This reduces duplication and lets us maintain a single source of truth where we can reliably establish implementation details for page features
  * **BasePage** is a core page model that all page models inherit. This is where we define universal method and fundamental structural design.
    * Examples include the `URL` and `LOCATORS` constants are established as a pattern here, to illustrate that they are expected in all page models
    * Other core functionality exists at this level, such as `get_element()` which defines how we take our locator dictionaries that we are creating within the page models and use them with Selenium actions.

Other items of note:
**APIs as page models** follow the same patterns as the web UI page models, though they have their own `BaseAPI` page model that serves as the API equivalent of `BasePage`.

### Saving DOMs on failures

*utils/dom.py* provides a utility to save the dom HTML of the current page. 

This can be used in testing. Currently it is implemented in page model `is_loaded` checks for the page having loaded.

All doms will be saved in a report subfolder to keep large runs tidy.

### Logging

We have implemented a custom logger.

* Display syntax of logs is improved
* Logs display in color
* Logs are saved to a log file in the report folder
* Logs are included in the HTML test report

> NOTE: Code that runs during initial setup only has our "pre_logger" which will display logs to the console but may lack some enhancement features such as being included in the log file. Once the environmental variables are all loaded, the main logger launches, from which point full logging features become active.

#### Customizing Log Level

The .env file can be used to provide a specific log level for the main logger.

Ex: LOG_LEVEL=WARNING will suppress all logs of lower levels, such as INFO, from the main logger
