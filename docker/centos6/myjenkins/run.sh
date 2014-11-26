#!/bin/bash
#

trap trapper HUP INT QUIT KILL TERM

trapper() {
  echo "signal catched"
  /etc/init.d/myjenkins stop >>/dev/null 2>&1
}

echo "Starting Jenkins"
# start service in background here
/etc/init.d/myjenkins start >>/dev/null 2>&1

# ouput Tomcat logs
tail -f /var/log/myjenkins/catalina.out

echo "Stopping Jenkins"
/etc/init.d/myjenkins stop >>/dev/null 2>&1
echo "Jenkins stopped"
