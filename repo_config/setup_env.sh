#! /usr/bin/env bash

REPO_ROOT=$(git rev-parse --show-toplevel)

#clean
#rm -rf $REPO_ROOT/repo_config/.venv_installation

#prepare environment for installation
python3 -m venv $REPO_ROOT/repo_config/.venv_installation
source $REPO_ROOT/repo_config/.venv_installation/bin/activate
pip install --upgrade pip
pip install -r $REPO_ROOT/repo_config/env_requirements.txt
source $REPO_ROOT/repo_config/.env

#start installation
ansible-playbook -c local $REPO_ROOT/repo_config/ansible/download_release.yml --extra-vars "json_file=$REPO_ROOT/repo_config/download_configs/repo_helper.json"
ansible-playbook -c local $REPO_ROOT/repo_config/ansible/download_release.yml --extra-vars "json_file=$REPO_ROOT/repo_config/download_configs/tcl_utils.json"
ansible-playbook -c local $REPO_ROOT/repo_config/ansible/playbooks/start_container.yml --extra-vars "json_file=$REPO_ROOT/repo_config/download_configs/tcl_utils.json"
#ansible-playbook -c local $REPO_ROOT/repo_config/ansible/install_releases.yml