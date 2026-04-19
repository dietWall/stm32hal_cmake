#! /usr/bin/env bash
#
# gh-dl-release! It works!
# 
# This script downloads an asset from latest or specific Github release of a
# private repo. Feel free to extract more of the variables into command line
# parameters.
#
# PREREQUISITES
#
# curl, wget, jq
#
# USAGE
#
# Set all the variables inside the script, make sure you chmod +x it, then
# to download specific version to my_app.tar.gz:
#
#     gh-dl-release 2.1.1 my_app.tar.gz
#
# to download latest version:
#
#     gh-dl-release latest latest.tar.gz
#
# If your version/tag doesn't match, the script will exit with error.

#TOKEN="<github_access_token>"

DOWNLOAD_DIR=$(pwd)/repo_config/tmp_download    #this is adapted to this repo, change at will if reusing
#REPO="dietwall/openocd-tcl-controller"          #this should be mandatory actually
VERSION="latest"                                # tag name or the word "latest", tag is a git tag created at release
GITHUB="https://api.github.com"

while getopts "t:r:f:v:o:" opt; do
  case $opt in
    t) TOKEN="$OPTARG" ;;
    r) REPO="$OPTARG" ;;
    f) FILE="$OPTARG" ;;
    v) VERSION="$OPTARG" ;;
    o) DOWNLOAD_DIR="$OPTARG" ;;
    *) echo "Usage: $0 -r <organization/repo> [-t token] [-f file] [-v version] [-o outdir]" >&2
       echo "$0 -r dietwall/repo_helper -o \$(pwd)/repo_config/tmp_download"
       echo "-r is mandatory"
       echo "-t is a Github Private Token, if omited, the script will take a TOKEN environment variable"
       echo "-f if provided, the file will be renamed to this arg, otherwise its name will be kept"
       echo "-v latest if ommited, otherwise it should be exactly the git tag, that has been created at release"
       echo "-o if ommited it will be current directory, otherwise the directory will be created"
       exit 1 ;;
  esac
done

echo "Downloading from: $REPO"
echo "Version: $VERSION"

if [ -z $TOKEN ]; then
  echo "environment variable TOKEN not set, cannot proceed"
  exit 1
fi;

function gh_curl() {
  curl -H "Authorization: token $TOKEN" \
       -H "Accept: application/vnd.github.v3.raw" \
       $@
}

release_data=`gh_curl -s $GITHUB/repos/$REPO/releases`
echo $release_data > release.json


if [ "$VERSION" = "latest" ]; then
  # this has been always the first entry in the array, 
  # if a wrong version is downloaded, 
  # check if github changed its response
  asset_id=`echo $release_data | jq ".[0].assets[0].id"`
  file_parser=".[0].assets[0].name "
  
  # check if file was set from outside, if not, get the original filename:
  if [ -z $FILE ]; then
    FILE=$(echo $release_data | jq $file_parser | tr -d '"')
  fi;

else
  #i hade to use jqs --arg to avoid quotes escaping hell here:
  asset_id=$(echo $release_data | jq --arg ver "$VERSION" ' . | map(select(.tag_name==$ver ))[0].assets[0].id ')
  echo "asset id found: $asset_id"
  file_parser=' . | map(select(.tag_name==$ver ))[0].assets[0].name '
  # check if file was set from outside, if not, get the original filename:
  if [ -z $FILE ]; then
    FILE=$(echo $release_data | jq --arg ver "$VERSION" ' . | map(select(.tag_name==$ver ))[0].assets[0].name ' | tr -d '"')
  fi;
fi;

if [ "$asset_id" = "null" ]; then
  echo "ERROR: asset id still not set, cannot download, exiting"
  exit 1
fi;

echo Starting Download:
echo "asset_id = $asset_id"
echo "file=$FILE"

if [ ! -d $DOWNLOAD_DIR ]; then
  mkdir -p $DOWNLOAD_DIR
fi;

download_url="https://$TOKEN:@api.github.com/repos/$REPO/releases/assets/$asset_id"
#actual download
wget -q --auth-no-challenge --header='Accept:application/octet-stream' \
  $download_url \
  -O $DOWNLOAD_DIR/$FILE
