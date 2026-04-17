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
REPO="dietwall/openocd-tcl-controller"
VERSION="latest"                       # tag name or the word "latest"
GITHUB="https://api.github.com"

while getopts "t:r:f:v:" opt; do
  case $opt in
    t) TOKEN="$OPTARG" ;;
    r) REPO="$OPTARG" ;;
    f) FILE="$OPTARG" ;;
    v) VERSION="$OPTARG" ;;
    *) echo "Usage: $0 -r <organization/repo> [-t token] [-f file] [-v version]" >&2
       exit 1 ;;
  esac
done

alias errcho='>&2 echo'

function gh_curl() {
  curl -H "Authorization: token $TOKEN" \
       -H "Accept: application/vnd.github.v3.raw" \
       $@
}

if [ -z "$FILE" ]; then
  release_data=`gh_curl -s $GITHUB/repos/$REPO/releases`
  #echo "release_data: $release_data"
  asset_id=`echo $release_data | jq ".[0].assets[0].id"`
  echo "asset_id: $asset_id"
  FILE=`echo $release_data | jq ".[0].assets[0].name" | tr -d '"'`
  echo $FILE
fi;

if [ "$VERSION" = "latest" ]; then
  # Github should return the latest release first.
  parser=".[0].assets | map(select(.name == \"$FILE\"))[0].id"
else
  parser=". | map(select(.tag_name == \"$VERSION\"))[0].assets | map(select(.name == \"$FILE\"))[0].id"
fi;


if [ "$asset_id" = "null" ]; then
  echo "ERROR: asset id still not set, exiting"
  exit 1
fi;

download_url="https://$TOKEN:@api.github.com/repos/$REPO/releases/assets/$asset_id"
#actual download
wget -q --auth-no-challenge --header='Accept:application/octet-stream' \
  $download_url \
  -O $FILE