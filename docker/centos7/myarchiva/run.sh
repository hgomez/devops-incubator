#!/bin/bash
#

trap trapper HUP INT QUIT KILL TERM

trapper() {
  echo "signal catched"
  /etc/init.d/myarchiva stop >>/dev/null 2>&1
}

echo "Starting Archiva"
# start service in background here
/etc/init.d/myarchiva start >>/dev/null 2>&1

# ouput Tomcat logs
tail -f /var/log/myarchiva/catalina.out

echo "Stopping Archiva"
/etc/init.d/myarchiva stop >>/dev/null 2>&1
echo "Archiva stopped"
