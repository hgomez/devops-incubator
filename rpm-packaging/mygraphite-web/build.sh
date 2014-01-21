#!/bin/sh

if [ -z "$GRAPHITE_VERSION" ]; then
  GRAPHITE_VERSION=0.9.11
fi

if [ -z "$GRAPHITE_HIGH_VERSION" ]; then
  GRAPHITE_HIGH_VERSION=0.9
fi

if [ $# -gt 1 ]; then
 GRAPHITE_VERSION=$1
 shift
fi

if [ $# -gt 1 ]; then
 GRAPHITE_HIGH_VERSION=$1
 shift
fi


GRAPHITE_URL=http://launchpad.net/graphite/$GRAPHITE_HIGH_VERSION/$GRAPHITE_VERSION/+download/graphite-web-$GRAPHITE_VERSION.tar.gz

#
# Fetch Function
#
fetch_remote_file()
{
	URL=$1
	DEST=$2
	BDEST=`basename $DEST`

	if [ ! -f $DEST ]; then

    if [ -z "$WORKSPACE" ]; then
       WORKSPACE="."
    fi

		DROP_DIR=$WORKSPACE/DROP_DIR
		mkdir -p $DROP_DIR
		DD_FILE=$DROP_DIR/$BDEST

		if [ -f $DD_FILE ]; then
			cp $DD_FILE $DEST
		else
			echo "downloading from $URL to $DEST..."
			curl -L $URL -o $DD_FILE

			case $DD_FILE in
				*.tar.gz)
		        	tar tzf $DD_FILE >>/dev/null 2>&1
		        	;;
		    	*.zip)
		        	unzip -t $DD_FILE >>/dev/null 2>&1
		        	;;
		    	*.jar)
		        	unzip -t $DD_FILE >>/dev/null 2>&1
		        	;;
		    	*.war)
		        	unzip -t $DD_FILE >>/dev/null 2>&1
		        	;;
			esac

			if [ $? != 0 ]; then
				rm -f $DD_FILE
				echo "invalid content $BDEST downloaded from $URL, discarding content and aborting build."
				exit -1
			else
				cp $DD_FILE $DEST
			fi
		fi

	fi
}


fetch_remote_file $GRAPHITE_URL SOURCES/graphite-web-${GRAPHITE_VERSION}.tar.gz

echo "Version to package is $GRAPHITE_VERSION"

# prepare fresh directories
rm -rf BUILD RPMS SRPMS TEMP
mkdir -p BUILD RPMS SRPMS TEMP

# Build using rpmbuild (use double-quote for define to have shell resolv vars !)
rpmbuild -bb --define="_topdir $PWD" --define="_tmppath $PWD/TEMP" --define="GRAPHITE_REL $GRAPHITE_VERSION"  SPECS/mygraphite-web.spec
