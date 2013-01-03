#The MIT License
#
#Copyright (c) 2012, Daniel Petisme
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# This script aims to ease the publication of the freshly built devops rpms to the
# content manager https://bintray.com/ It's a lazy script so you won't found any
# CLI controls...


#Constants
API=https://api.bintray.com
NOT_FOUND=404
SUCCESS=200
CREATED=201
PACKAGE_DESCRIPTOR=package.json

# Arguments
# $1 SUBJECT aka. your BinTray username
# $2 API_KEY act as a password for REST authentication
# $3 REPO the targeted repo
# $4 the rpm to deploy on BinTray 

function main() {
  SUBJECT=$1
  API_KEY=$2
  REPO=$3
  RPM=$4
  
  PCK_NAME=$(rpm -qp ${RPM} --qf "%{NAME}")
  PCK_VERSION=$(rpm -qp ${RPM} --qf "%{VERSION}")
  PCK_RELEASE=$(rpm -qp ${RPM} --qf "%{RELEASE}")
  
  init_curl
  if [ not $(check_package_exists) ]; then
    create_package
  else
    deploy_rpm
  fi
}

function init_curl() {
  CURL="curl -u${SUBJECT}:${API_KEY} -H Content-Type:application/json -H Accept:application/json"
}

function check_package_exists() {
  package_exists=`[  $(${CURL} --write-out %{http_code} --silent --output /dev/null -X GET  ${API}/packages/${SUBJECT}/${REPO}/${PCK_NAME})  -eq ${SUCCESS} ]`   
  return ${package_exists} 
}

function create_package() {
  #search for a descriptor in the current folder or generate one on the fly
  if [ -f "${PACKAGE_DESCRIPTOR}" ]; then
    data="@${PACKAGE_DESCRIPTOR}"
  else
    data="{
    \"name\": \"${PCK_NAME}\",
    \"desc\": \"auto\",
    \"desc_url\": \"auto\",
    \"labels\": [\"rpm\", \"devops\"]
    }"
  fi
  
  ${CURL} -X POST  -d  "${data}" ${API}/packages/${SUBJECT}/${REPO}/
}

function upload_content() {
  return $(${CURL} --write-out %{http_code} --silent --output /dev/null -T ${RPM} -H X-Bintray-Package:${REPO} -H X-Bintray-Version:${PCK_VERSION}-${PCK_RELEASE} ${API}/content/${SUBJECT}/${REPO}/${PCK_NAME})
}
function deploy_rpm() {
  
  content_upload=$(upload_content)
  if [ ${content_upload} -eq ${CREATED} ]; then
    ${CURL} -X POST ${API}/content/${SUBJECT}/${REPO}/${PCK_NAME}/${PCK_VERSION}-${PCK_RELEASE}/publish -d "{ \"discard\": \"false\" }"  
  else
    echo "Impossible to upload content - HTTP: ${content_upload}"
  fi  
}

main "$@"
