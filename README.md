[![codecov](https://codecov.io/gh/max-pfeiffer/password-generator/branch/main/graph/badge.svg?token=WQI2SJJLZN)](https://codecov.io/gh/max-pfeiffer/password-generator)
# password-generator
A FastApi example project providing a password generator.

## Version Control Workflow
For this project I choose to go for [trunk-based development](https://trunkbaseddevelopment.com/)
as a version control management practice. The core "trunk" is here the
projects "main" branch. The advantages outweigh the disadvantages.

Advantages:
* No need to build releases on special branches: saves time and effort for merges in the team
* CI/CD friendly: deployments can be done easily via pipeline i.e. by simply tagging the trunk ("main" branch)
* Enables team to do deliver frequently to production
* Urgent hotfixes can be delivered faster

Disadvantages:
* Deliverables/Features have to be planned more thoroughly as they become deployed immediately via small feature branches

Branch naming conventions:
* main (trunk)
* feature/{description}
* bugfix/{description}
* hotfix/{description}

## Local Development
For local development Python v3.9 is required and needs to be installed.
This documentation assumes your current ```python``` interpreter/command is
Python v3.9.

### Create virtual environment and install dependencies
```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Add .env File
For running the application locally with a custom configuration (also when using
docker-compose) you need to have a ```.env``` file placed in project root.
This file is not checked into the repo.

This .env file contains the environment variables for configuring the default
values for the password generation.

You can use the ```.env-example``` as a template like so:
```shell
cp .env-example .env
```

### Code Formatting
I choose to add black as dependency for doing automatic code formatting.
Manual code formatting is time-consuming. This way the software engineer can
use his time to work on features and improvements.
Black is also used in the CI/CD pipeline to check for correct code formatting.

Run black to format code in project root like this:
```shell
black .
```

### Linting
I choose to add pylint as linter as this is probably the most widely used
linter that is able to find syntax errors. Advantage of that tool is that we
can identify syntax errors and bad coding practices which could slip through
code review. Downside of pylint is that it produces a lot of false positives
which need to be checked on and silenced. But I think the advantages outweigh
the disadvantages here.

Run pylint in project roo like this:
```shell
pylint app tests
```

### Pre-commit Handler
The pre-commit handler is configured to automatically check:
* general commit content i.e. no secrets in commits, large files 
* code formatting compliance (with black)
* syntax errors, good coding practices (with pylint)

Install pre-commit handler:
```shell
pre-commit install
```

Adding pylint to the pre-commit handler can become questionable in larger
projects as it then runs very slow. And this can slow down commits in
development process. But in this small example problem this is not a problem.

### Run Tests
Run all tests from project root:
```shell
pytest
```
Run a specific test from project root:
```shell
pytest tests/application/unit/test_api_endpoint_error_handler.py
```
Create test coverage reports from project root like so:
```shell
pytest --cov=app
```

### Run the Application
```shell
uvicorn --host 127.0.0.1 --port 8000 app.main:app
```
For development purposes you can use the --reload flag for hot reloading after
code changes:
```shell
uvicorn --host 127.0.0.1 --port 8000 --reload app.main:app
```
The applications homepage just redirects tp the API autodocs on
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). The usage of the
password generation endpoint is documented in the autodocs. This is also a
convenient way to try out the functionality of that endpoint.

### Build and run the Docker Container
Build the container from project root:
```shell
docker build --target production-image --tag password-generator:dev .
```
Run the container from project root:
```shell
docker run --rm -it --publish 8000:8000 password-generator:dev
```
