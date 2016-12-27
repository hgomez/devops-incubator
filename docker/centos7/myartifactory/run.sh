#!/bin/bash
#

trap trapper HUP INT QUIT KILL TERM

trapper() {
  echo "signal catched"
  /etc/init.d/myartifactory stop >>/dev/null 2>&1
}

echo "Starting Artifactory"
# start service in background here
/etc/init.d/myartifactory start >>/dev/null 2>&1

# ouput Tomcat logs
tail -f /var/log/myartifactory/catalina.out

echo "Stopping Artifactory"
/etc/init.d/myartifactory stop >>/dev/null 2>&1
echo "Artifactory stopped"
