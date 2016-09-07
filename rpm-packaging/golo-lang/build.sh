#!/bin/sh

VERSION=3.2.0-M4

# prepare fresh directories
rm -rf BUILD RPMS SRPMS TEMP
mkdir -p BUILD RPMS SRPMS SOURCES TEMP

GOLO_URL=https://www.eclipse.org/downloads/download.php?file=/golo/golo-${VERSION}.zip&r=1

if [ ! -f SOURCES/golo-${VERSION}-distribution.zip ]; then
  echo "downloading golo-${VERSION}-distribution.zip from $GOLO_URL"
  curl -s -L $GOLO_URL -o SOURCES/golo-${VERSION}.zip
fi

# Build using rpmbuild (use double-quote for define to have shell resolv vars !)
rpmbuild -bb --define="_topdir $PWD" --define="_tmppath $PWD/TEMP" --define="VERSION $VERSION" SPECS/golo-lang.spec
