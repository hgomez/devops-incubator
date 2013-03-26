#!/bin/sh

MYAPP_VERSION=1.0.4
TOMCAT_VERSION=7.0.37

if [ $# -gt 1 ]; then
  TOMCAT_VERSION=$1
  shift
fi

TOMCAT_URL=http://mir2.ovh.net/ftp.apache.org/dist/tomcat/tomcat-7/v${TOMCAT_VERSION}/bin/apache-tomcat-${TOMCAT_VERSION}.tar.gz
CATALINA_JMX_REMOTE_URL=http://mir2.ovh.net/ftp.apache.org/dist/tomcat/tomcat-7/v${TOMCAT_VERSION}/bin/extras/catalina-jmx-remote.jar
MYAPP_URL=http://repo1.maven.org/maven2/org/jmxtrans/embedded/samples/cocktail-app/${MYAPP_VERSION}/cocktail-app-${MYAPP_VERSION}.war

if [ ! -f SOURCES/apache-tomcat-${TOMCAT_VERSION}.tar.gz ]; then
  echo "downloading apache-tomcat-${TOMCAT_VERSION}.tar.gz from $TOMCAT_URL"
  curl -s -L $TOMCAT_URL -o SOURCES/apache-tomcat-${TOMCAT_VERSION}.tar.gz
fi

if [ ! -f SOURCES/catalina-jmx-remote-${TOMCAT_VERSION}.jar ]; then
  echo "downloading catalina-jmx-remote-${TOMCAT_VERSION}.jar from $CATALINA_JMX_REMOTE_URL"
  curl -s -L $CATALINA_JMX_REMOTE_URL -o SOURCES/catalina-jmx-remote-${TOMCAT_VERSION}.jar
fi

if [ ! -f SOURCES/cocktail-app-${MYAPP_VERSION}.war ]; then
  echo "downloading cocktail-app-${MYAPP_VERSION}.war from $MYAPP_URL"
  curl -s -L $MYAPP_URL -o SOURCES/cocktail-app-${MYAPP_VERSION}.war
fi

echo "Version to package is powered by Apache Tomcat $TOMCAT_VERSION"

# prepare fresh directories
rm -rf BUILD RPMS SRPMS TEMP
mkdir -p BUILD RPMS SRPMS TEMP

# Build using rpmbuild (use double-quote for define to have shell resolv vars !)
rpmbuild -bb --define="_topdir $PWD" --define="_tmppath $PWD/TEMP" --define="TOMCAT_REL $TOMCAT_VERSION" --define="MYAPP_REL $MYAPP_VERSION"  SPECS/myapp.spec

