#!/bin/sh

VERSION=3.0.0-incubation-M1

# prepare fresh directories
rm -rf BUILD RPMS SRPMS TEMP
mkdir -p BUILD RPMS SRPMS SOURCES TEMP

GOLO_URL=https://www.eclipse.org/downloads/download.php?file=/golo/golo-${VERSION}-distribution.zip&r=1

if [ ! -f SOURCES/golo-${VERSION}.tar.gz ]; then
  echo "downloading golo-${VERSION}.tar.gz from $GOLO_URL"
  curl -s -L $GOLO_URL -o SOURCES/golo-${VERSION}-distribution.tar.gz
fi

# Build using rpmbuild (use double-quote for define to have shell resolv vars !)
rpmbuild -bb --define="_topdir $PWD" --define="_tmppath $PWD/TEMP" --define="VERSION $VERSION" SPECS/golo-lang.spec
