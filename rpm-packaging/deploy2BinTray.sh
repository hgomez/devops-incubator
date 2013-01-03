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

# Arguments
# $1 SUBJECT aka. your BinTray username
# $2 API_KEY act as a password for REST authentication
# $3 REPO the targeted repo 

function main() {
  SUBJECT=$1
  API_KEY=$2
  REPO=$3
  
  init_curl
  check_package_exists "crash"
  echo $?  

}

function init_curl() {
  CURL="curl -u${SUBJECT}:${API_KEY} -i -H \"Content-Type: application/json\" -H \"Accept: application/json\" "     
}

function check_package_exists() {
  local package=$1  
  return [ $(curl --write-out %{http_code} --silent --output /dev/null -X GET  ${API}/packages/${SUBJECT}/${REPO}/${package}) -eq ${NOT_FOUND} ] 
}


main "$@"
