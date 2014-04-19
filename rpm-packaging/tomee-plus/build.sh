#!/bin/sh

TOMEE_VERSION=1.6.0.1
TOMCAT_VERSION=7.0.53

if [ $# -gt 1 ]; then
  TOMEE_VERSION=$1
  shift
fi

TOMEE_FILE=apache-tomee-$TOMEE_VERSION-plus.tar.gz
TOMEE_URL=http://archive.apache.org/dist/tomee/tomee-$TOMEE_VERSION/$TOMEE_FILE
CATALINA_JMX_REMOTE_URL=http://archive.apache.org/dist/tomcat/tomcat-7/v${TOMCAT_VERSION}/bin/extras/catalina-jmx-remote.jar

if [ ! -f SOURCES/$TOMEE_FILE ]; then
  echo "downloading $TOMEE_FILE from $TOMEE_URL"
  curl -s -L $TOMEE_URL -o SOURCES/$TOMEE_FILE
fi

if [ ! -f SOURCES/catalina-jmx-remote.jar ]; then
  echo "downloading catalina-jmx-remote.jar from $CATALINA_JMX_REMOTE_URL"
  curl -s -L $CATALINA_JMX_REMOTE_URL -o SOURCES/catalina-jmx-remote.jar
fi

echo "RPM Packaging TomEE Plus for $TOMEE_VERSION"

# prepare fresh directories
rm -rf BUILD RPMS SRPMS TEMP
mkdir -p BUILD RPMS SRPMS TEMP

# Build using rpmbuild (use double-quote for define to have shell resolv vars !)
rpmbuild -bb --define="_topdir $PWD" --define="_tmppath $PWD/TEMP" --define="TOMEE_REL $TOMEE_VERSION" SPECS/tomee-plus.spec

