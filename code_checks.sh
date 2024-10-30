#!/bin/bash
set -e
python3.12 -m licensecheck --zero
python3.12 -m pip_audit
python3.12 -m bandit -c pyproject.toml -r .
python3.12 -m black . --check
python3.12 -m isort . --check
python3.12 -m pylint .
python3.12 -m pytest --cov=. --cov-report=term-missing
python3.12 -m coverage report --fail-under=100
