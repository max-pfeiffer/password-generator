# password-generator
A FastApi example project providing a password generator.

## Local Development
For local development Python v3.9 is required and needs to be installed.
This documentation assumes your current ```python``` interpreter/command is
Python v3.9.

### Create virtual environment and install dependencies
```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
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
