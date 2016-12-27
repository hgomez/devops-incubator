#!/bin/sh
#

#
# read MYPID MYCMD MYSTATE MYPPID MYPGRP MYSESSION MYTTYNR MYTPGID MYREST < /proc/self/stat
#

readonly PROGNAME=$(basename $0)
readonly PROGDIR=$(readlink -m $(dirname $0))
readonly ARGS="$@"

# Trap Signals
trap catchsignal HUP INT QUIT KILL TERM

waitprocess() {

    local SERVICE_PID=/var/run/$SERVICE_NAME.pid

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

catchsignal() {

    if [ ! -z "$SERVICE_NAME" ]; then
      /etc/init.d/$SERVICE_NAME stop
      waitprocess
    fi
}

main() {

    SERVICE_NAME=$1

    /etc/init.d/$SERVICE_NAME start
    waitprocess
}

main $ARGS

