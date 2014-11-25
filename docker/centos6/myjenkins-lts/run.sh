#!/bin/sh
#

trap trapper HUP INT QUIT KILL TERM

trapper() {
  echo "signal catched"
  /etc/init.d/myjenkins stop
}

# start service in background here
/etc/init.d/myjenkins start

echo "[hit enter key to exit] or run 'docker stop <container>'"
read

# stop service and clean up here
echo "stopping service"
/etc/init.d/myjenkins stop

echo "exited $0"
