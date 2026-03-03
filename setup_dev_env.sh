#! /usr/bin/env bash

#this has to be run in container
# setups the venv and installs dependencies for tests

REPO_ROOT=$(git rev-parse --show-toplevel)

#prepare environment for installation
python3 -m venv $REPO_ROOT/.venv_container
source $REPO_ROOT/.venv_container/bin/activate
pip install --upgrade pip
pip install -r $REPO_ROOT/requirements.txt
#start installation
pip install repo_config/ansible/tmp_install/*
