#!/bin/sh

# prepare fresh directories
rm -rf BUILD RPMS SRPMS TEMP
mkdir -p BUILD RPMS SRPMS TEMP

# Build using rpmbuild (use double-quote for define to have shell resolv vars !)
rpmbuild -ba --define="_topdir $PWD" --define="_tmppath $PWD/TEMP" SPECS/myforge-apache2-front.spec

