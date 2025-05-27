# Python Selenium Template

## Pre-requisites

* chromedriver is in PATH
* `pip install selenium`
* `pip install pytest`

## .env - Secrets and non-version controlled data

The .env file is not version controlled so that we can store secrets and anything that you want to be user specific.

To get started, copy the `.env.template` file and remove the `.template` from the filename. This will provide you with a starting point, and a map of the expected variable names.

## Usage

Running `pytest` in the top directory, will run the tests in all files beginning with `test_`
