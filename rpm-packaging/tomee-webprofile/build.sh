#!/bin/sh

TOMEE_VERSION=1.5.2

if [ $# -gt 1 ]; then
  TOMEE_VERSION=$1
  shift
fi

TOMEE_FILE=apache-tomee-$TOMEE_VERSION-webprofile.tar.gz
TOMEE_URL=http://apache.osuosl.org/tomee/tomee-$TOMEE_VERSION/$TOMEE_FILE

if [ ! -f SOURCES/$TOMEE_FILE ]; then
  echo "downloading $TOMEE_FILE from $TOMEE_URL"
  curl -s -L $TOMEE_URL -o SOURCES/$TOMEE_FILE
fi

echo "RPM Packaging TomEE WebProfile for $TOMEE_VERSION"

# prepare fresh directories
rm -rf BUILD RPMS SRPMS TEMP
mkdir -p BUILD RPMS SRPMS TEMP

# Build using rpmbuild (use double-quote for define to have shell resolv vars !)
rpmbuild -bb --define="_topdir $PWD" --define="_tmppath $PWD/TEMP" --define="TOMEE_REL $TOMEE_VERSION" SPECS/tomee-webprofile.spec

