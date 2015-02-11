#!/bin/sh

VERSION=1.3.1

# prepare fresh directories
rm -rf BUILD RPMS SRPMS TEMP
mkdir -p BUILD RPMS SRPMS SOURCES TEMP

CRASH_URL=http://central.maven.org/maven2/org/crashub/crash.distrib/${VERSION}/crash.distrib-${VERSION}.tar.gz

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

fetch_remote_file $CRASH_URL SOURCES/crash.distrib-${VERSION}.tar.gz

# Build using rpmbuild (use double-quote for define to have shell resolv vars !)
rpmbuild -bb --define="_topdir $PWD" --define="_tmppath $PWD/TEMP" --define="VERSION $VERSION" SPECS/crash.spec

