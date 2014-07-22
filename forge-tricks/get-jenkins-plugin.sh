#!/bin/bash
#

readonly PROGNAME=$(basename $0)
readonly PROGDIR=$(readlink -m $(dirname $0))
readonly ARGS="$@"

get_plugins() {
$CURL_CMD "$JENKINS_URL/pluginManager/api/xml?depth=1" | xmlstarlet sel -t -m "//plugin" -s A:T:- shortName -v "concat(shortName, ':', version)" -n
}

#
# Usage
#
usage() {
  cat <<- EOF
  usage: $PROGNAME options
  
  Get list of Jenkins Plugins with version

  OPTIONS:
     -u --url  Jenkins base URL
 
  Examples:

     Run:
     $PROGNAME --url http://myjenkins.mycorp.org
EOF

  exit 1
}

#
# Parse command line
#
cmdline() {
  # got this idea from here:
  # http://kirk.webfinish.com/2009/10/bash-shell-script-to-use-getopts-with-gnu-style-long-positional-parameters/
  local arg=
  for arg
  do
    local delim=""
    case "$arg" in
      #translate --gnu-long-options to -g (short options)
      --url)     args="${args}-u ";;
      --help)    args="${args}-h ";;
      --verbose)   args="${args}-v ";;
      --debug)     args="${args}-x ";;
      #pass through anything else
      *) [[ "${arg:0:1}" == "-" ]] || delim="\""
        args="${args}${delim}${arg}${delim} ";;
    esac
  done

  #Reset the positional parameters to the short options
  eval set -- $args

  while getopts "hvxu:" OPTION
  do
     case $OPTION in
     v)
       readonly VERBOSE=1
       ;;
     x)
       readonly DEBUG='-x'
       set -x
       ;;
     h)
       usage
       exit 0
       ;;
     u)
       readonly JENKINS_URL=$OPTARG
       ;;
    esac
  done

  if [ -z "$JENKINS_URL" ]; then
    echo "You must provide Jenkins URL"
    usage
  fi

  if [ "$VERBOSE" = "1" ]; then
    CURL_CMD="curl -L"
  else
    CURL_CMD="curl -L --silent"
  fi 

  if [ "$DEBUG" = "-x" ]; then
    CURL_CMD="$CURL_CMD -v"
  fi 
}


main() {

  cmdline $ARGS
  get_plugins
}

main
