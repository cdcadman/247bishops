#!/bin/bash
# Run this to update requirements.txt with the latest matching versions from base_reqs.txt
set -e
rm -rf venv/
mkdir venv
python3.12 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r base_reqs.txt
python -m pip freeze > requirements.txt
deactivate
