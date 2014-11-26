#!/bin/bash
#

trap trapper HUP INT QUIT KILL TERM

trapper() {
  echo "signal catched"
  /etc/init.d/mynexus stop >>/dev/null 2>&1
}

echo "Starting Nexus"
# start service in background here
/etc/init.d/mynexus start stop >>/dev/null 2>&1

# ouput Tomcat logs
tail -f /var/log/mynexus/catalina.out

echo "Stopping Nexus"
/etc/init.d/mynexus stop stop >>/dev/null 2>&1
echo "Nexus stopped"
