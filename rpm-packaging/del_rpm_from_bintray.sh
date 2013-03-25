#!/bin/bash
#
# del_rpm_from_bintray.sh - henri.gomez@gmail.com
# 
# This script delete a package from Bintray repo
#

function usage() {
  echo "$0 username api_key repo_name rpm_name"
  exit 0
}

if [ $# -lt 4 ]; then
 usage
fi

BINTRAY_USER=$1
BINTRAY_APIKEY=$2
BINTRAY_REPO=$3

shift;
shift;
shift;

CURL_CMD="curl --write-out %{http_code} --silent --output /dev/null -u$BINTRAY_USER:$BINTRAY_APIKEY"

BINTRAY_ACCOUNT=$BINTRAY_USER

for RPM_NAME in $@; do

  echo "Deleting package $RPM_NAME from Bintray repository $BINTRAY_REPO ..."
  HTTP_CODE=`$CURL_CMD -H "Content-Type: application/json" -X DELETE https://api.bintray.com/packages/$BINTRAY_ACCOUNT/$BINTRAY_REPO/$RPM_NAME`

  if [ "$HTTP_CODE" != "200" ]; then
   echo "can't delete package -> $HTTP_CODE"
  else
   echo "Package deleted"
  fi

done


