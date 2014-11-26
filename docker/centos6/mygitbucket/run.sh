#!/bin/bash
#

trap trapper HUP INT QUIT KILL TERM

trapper() {
  echo "signal catched"
  /etc/init.d/mygitbucket stop >>/dev/null 2>&1
}

echo "Starting Gitbucket"
# start service in background here
/etc/init.d/mygitbucket start >>/dev/null 2>&1

# ouput Tomcat logs
tail -f /var/log/mygitbucket/catalina.out

echo "Stopping Gitbucket"
/etc/init.d/mygitbucket stop >>/dev/null 2>&1
echo "Gitbucket stopped"
