#!/bin/sh
#

#
# read MYPID MYCMD MYSTATE MYPPID MYPGRP MYSESSION MYTTYNR MYTPGID MYREST < /proc/self/stat
#

readonly PROGNAME=$(basename $0)
readonly PROGDIR=$(readlink -m $(dirname $0))
readonly ARGS="$@"

# Trap SIGTERM / SIGINT
trap catchsignal INT
trap catchsignal TERM

function signal() {
    /etc/init.d/$1 stop
    sleep 1
}

main() {

    /etc/init.d/$1 start
    sleep 1

    local SERVICE_PID=/var/run/$1.pid

    while true; do

      if [ -r "$SERVICE_PID" ]; then
        PID=`cat "$SERVICE_PID"`
        ps -p $PID >/dev/null 2>&1
        if [ $? -eq 1 ] ; then
          break;
        fi
      else
          break;
      fi

      sleep 1

    done
}

main $ARGS

