#
# Read config file
#

if [ -r "/etc/sysconfig/@@MYAPP_APP@@" ]; then
    . /etc/sysconfig/@@MYAPP_APP@@
fi

if [ ! -z "$APP_JAVA_HOME" ]; then
  JAVA_HOME=$APP_JAVA_HOME
fi

CATALINA_OPTS=$APP_JAVA_OPTS

#
# CATALINA tuning
#

JMX_EXT_IP=""

CATALINA_OPTS="$CATALINA_OPTS -Dcom.sun.management.jmxremote=true -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.authenticate=true"
CATALINA_OPTS="$CATALINA_OPTS -Dcom.sun.management.jmxremote.password.file=$CATALINA_HOME/conf/jmxremote.password -Dcom.sun.management.jmxremote.access.file=$CATALINA_HOME/conf/jmxremote.access"

CATALINA_OPTS="$APP_JAVA_OPTS $CATALINA_OPTS"


