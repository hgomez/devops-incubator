#!/bin/sh

VERSION=0-preview1

# prepare fresh directories
rm -rf BUILD RPMS SRPMS TEMP
mkdir -p BUILD RPMS SRPMS SOURCES TEMP

CRASH_URL=http://sourceforge.net/projects/golo-lang/files/${VERSION}/golo-${VERSION}-distribution.tar.gz/download 

if [ ! -f SOURCES/crash-${VERSION}.tar.gz ]; then
  echo "downloading crash-${VERSION}.tar.gz from $CRASH_URL"
  curl -s -L $CRASH_URL -o SOURCES/golo-${VERSION}-distribution.tar.gz
fi

# Build using rpmbuild (use double-quote for define to have shell resolv vars !)
rpmbuild -bb --define="_topdir $PWD" --define="_tmppath $PWD/TEMP" --define="VERSION $VERSION" SPECS/golo-lang.spec

