# Hacker News API automated Tests (pytest) 

## Description

This project is an automated test suite for the [Hacker News API](https://github.com/HackerNews/API). It provides a testing framework to validate API responses, data structures, and edge cases for Hacker News endpoints.

### Features

- **API Client Framework**: Custom `BaseClient` and `HackerNewsClient` classes for making HTTP requests with retry logic, logging, and response handling
- **Test Coverage**: Tests for top stories, individual items, comments, and various edge cases (deleted comments, stories without comments, invalid IDs)
- **Response Validation**: Helper functions that validate API response structure, data types, and required/optional fields according to the Hacker News API specification
- **Error Handling**: Tests handle edge cases like non-existent items, deleted content, and malformed responses
- **Logging & Debugging**: Configurable detailed logging for request/response tracing during test execution
- **Parallel Test Execution**: Support for running tests in parallel using pytest-xdist


### Architecture

- **`core/api/clients/`**: Base API client and Hacker News-specific client implementation
- **`core/api/helpers/`**: Validation and utility functions for API response testing
- **`core/api/api_response.py`**: Wrapper class for API responses with convenient access methods
- **`tests/api/`**: Test suite using pytest with custom markers for test organization


# Environment setup

1. Install python 3.12
    ```shell
    brew install python@3.12
    ```

2. To create virtual environment navigate to project root directory and execute
    ```shell
    make install
    ```

3. Activate the venv and update the interpreter in your IDE to use `venv/bin/python`
    ```shell
    source venv/bin/activate
    ```

## Running tests


Use pytest from project virtunalenv to filter and run tests. Supported
markers could be found in `pytest.ini` or by running `pytest --markers`

Examples
 
``` 
pytest -m 'hacker_news' -n5 # run all test with marker in parallel
pytest -k 'test_top_stories' # run single tests with name  
```

#### Makefile available options:

```
help                      List the available targets
ensure-bash               check that the correct shell is configured for make
install                   create venv, install requirements and pre-commit hooks
venv                      create venv, install requirements
pylint                    run `pylint core tests` on changed files, all messages
pylint-all                run `pylint core tests` on all files, all messages
clean                     remove venv and compiled python files
cleanup                   remove tmp dirs and test artifacts
logs                      tail request / response test logs 
```

### TODO
* add pre-commit hook checks i.e. formatting, linting
* extend edge case coverage  
