#! /usr/bin/env bash

REPO_ROOT=$(git rev-parse --show-toplevel)
source $REPO_ROOT/repo_config/.venv_installation/bin/activate

ansible-playbook -c local $REPO_ROOT/repo_config/ansible/download_release.yml --extra-vars "json_file=$REPO_ROOT/repo_config/download_configs/repo_helper.json"
ansible-playbook -c local $REPO_ROOT/repo_config/ansible/download_release.yml --extra-vars "json_file=$REPO_ROOT/repo_config/download_configs/tcl_utils.json"