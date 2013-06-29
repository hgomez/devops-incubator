#!/bin/sh

TOMEE_VERSION=1.0.52

if [ $# -gt 1 ]; then
  TOMEE_VERSION=$1
  shift
fi

TOMEE_URL=http://www.apache.org/dyn/closer.cgi/tomee/tomee-$TOMEE_VERSION/apache-tomee-$TOMEE_VERSION-webprofile.tar.gz

if [ ! -f SOURCES/apache-tomee-$TOMEE_VERSION-webprofile.tar.gz ]; then
  echo "downloading apache-tomee-$TOMEE_VERSION-webprofile.tar.gz from $TOMEE_URL"
  curl -s -L $TOMEE_URL -o SOURCES/apache-tomee-$TOMEE_VERSION-webprofile.tar.gz
fi

echo "RPM Packaging TomEE WebProfile for $TOMEE_VERSION"

# prepare fresh directories
rm -rf BUILD RPMS SRPMS TEMP
mkdir -p BUILD RPMS SRPMS TEMP

# Build using rpmbuild (use double-quote for define to have shell resolv vars !)
rpmbuild -bb --define="_topdir $PWD" --define="_tmppath $PWD/TEMP" --define="TOMEE_REL $TOMCAT_VERSION" SPECS/tomee-webprofile.spec

