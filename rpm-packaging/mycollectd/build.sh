#!/bin/sh

if [ -z "$COLLECTD_VERSION" ]; then
  COLLECTD_VERSION=5.2.1
fi

if [ $# -gt 1 ]; then
 COLLECTD_VERSION=$1
 shift
fi

COLLECTD_URL=http://collectd.org/files/collectd-${COLLECTD_VERSION}.tar.bz2

download_file_if_needed()
{
	URL=$1
	DEST=$2

	if [ ! -f $DEST ]; then

		echo "downloading from $URL to $DEST..."
		curl -L $URL -o $DEST

		case $DEST in
			*.tar.gz)
	        	tar tzf $DEST >>/dev/null 2>&1
	        	;;
	    	*.zip)
	        	unzip -t $DEST >>/dev/null 2>&1
	        	;;
	    	*.jar)
	        	unzip -t $DEST >>/dev/null 2>&1
	        	;;
	    	*.war)
	        	unzip -t $DEST >>/dev/null 2>&1
	        	;;
		esac

		if [ $? != 0 ]; then
			rm -f $DEST
			echo "invalid content for `basename $DEST` downloaded from $URL, discarding content and aborting build."
			exit -1
		fi

	fi
}

download_file_if_needed $COLLECTD_URL SOURCES/collectd-${COLLECTD_VERSION}.tar.bz2

echo "Version to package is $COLLECTD_VERSION"

# prepare fresh directories
rm -rf BUILD RPMS SRPMS TEMP
mkdir -p BUILD RPMS SRPMS TEMP

# Build using rpmbuild (use double-quote for define to have shell resolv vars !)
rpmbuild -bb --define="_topdir $PWD" --define="_tmppath $PWD/TEMP" --define="COLLECTD_REL $COLLECTD_VERSION"  SPECS/mycollectd.spec

