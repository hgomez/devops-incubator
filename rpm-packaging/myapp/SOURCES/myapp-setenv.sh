#
# Read config file
#

if [ -r "/etc/sysconfig/@@SKEL_APP@@" ]; then
    . /etc/sysconfig/@@SKEL_APP@@
fi

if [ ! -z "$APP_JAVA_HOME" ]; then
  JAVA_HOME=$APP_JAVA_HOME
fi

CATALINA_OPTS=$APP_JAVA_OPTS

#
# Variable resolution
#
ALL_VARS=$(compgen -A variable | grep APP_)

for RES_KEY in $ALL_VARS; do
 eval RES_VAL=\$${RES_KEY}
 XREPLACE="$XREPLACE | sed 's|@${RES_KEY}@|$RES_VAL|g'"
done

for XFILE in $CATALINA_HOME/conf/server.xml.skel $CATALINA_HOME/conf/jmxremote.access.skel $CATALINA_HOME/conf/jmxremote.password.skel; do
    DXFILE=${XFILE%.skel}
    eval "cat ${XFILE} $XREPLACE > ${DXFILE}"
done

#
# CATALINA tuning
#

JMX_EXT_IP=""

CATALINA_OPTS="$CATALINA_OPTS -Dcom.sun.management.jmxremote=true -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.authenticate=false"
CATALINA_OPTS="$CATALINA_OPTS -Dcom.sun.management.jmxremote.password.file=$CATALINA_HOME/conf/jmxremote.password -Dcom.sun.management.jmxremote.access.file=$CATALINA_HOME/conf/jmxremote.access"

CATALINA_OPTS="$APP_JAVA_OPTS $CATALINA_OPTS"


