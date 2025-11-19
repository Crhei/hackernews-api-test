# Environment setup

1. Install python 3.12
    ```shell
    brew install python@3.12
    ```

2. Create a virtual environment. Navigate to project root directory and execute
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
pytest -m 'hn_news' -n5 # run all test with marker in parallel
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
