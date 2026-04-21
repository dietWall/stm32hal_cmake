#! /usr/bin/env bash

repo_root=$(git rev-parse --show-toplevel)
venv_dir=$repo_root/repo_config/.venv_host/

echo "Initializing Dev Environment"
echo Repository located in $repo_root
echo Creating Python Virtual environment: $venv_dir

python3 -m venv $venv_dir
echo "venv created, activating"
source $venv_dir/bin/activate

#download private repo_stuff only for host environment
if [ -f $repo_root/repo_config/.env ]; then
  echo ".env file found, taking TOKEN from there"
  source $repo_root/repo_config/.env
  export TOKEN=$REPO_HELPER_TOKEN
fi;

#test if token has been set from (ci and local)
if [ -z $TOKEN ]; then
  echo "TOKEN not set, cannot proceed with downloading private repo_helper"
  exit 1
fi;

#download
$repo_root/repo_config/download_release.sh -r dietwall/repo_helper -o $repo_root/repo_config/tmp_download
#install private repo_helper in venv_host
pip3 install $repo_root/repo_config/tmp_download/repo_helper-*.whl
#cleanup:
rm -rf $repo_root/repo_config/tmp_download/*


echo "Dev Environment setup complete"
echo "activate environment with:" 
echo "source $venv_dir/bin/activate"
echo "run repo_ops.py to proceed:"
echo "$repo_root/repo_ops.py --help"

