#! /usr/bin/env bash

REPO_ROOT=$(git rev-parse --show-toplevel)

#prepare environment for installation
python3 -m venv $REPO_ROOT/repo_config/.venv_installation
source $REPO_ROOT/repo_config/.venv_installation/bin/activate
pip install --upgrade pip
pip install -r $REPO_ROOT/repo_config/requirements.txt

