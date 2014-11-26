#!/bin/bash
#

trap trapper HUP INT QUIT KILL TERM

trapper() {
  echo "signal catched"
  /etc/init.d/mygitblit stop >>/dev/null 2>&1
}

echo "Starting Gitblit"
# start service in background here
/etc/init.d/mygitblit start stop >>/dev/null 2>&1

# ouput Tomcat logs
tail -f /var/log/mygitblit/catalina.out

echo "Stopping Gitblit"
/etc/init.d/mygitblit stop stop >>/dev/null 2>&1
echo "Gitblit stopped"
