#!/bin/sh

if [ -z "$WHISPER_VERSION" ]; then
  WHISPER_VERSION=0.9.10
fi

if [ -z "$WHISPER_HIGH_VERSION" ]; then
  WHISPER_HIGH_VERSION=0.9
fi

if [ $# -gt 1 ]; then
 WHISPER_VERSION=$1
 shift
fi

if [ $# -gt 1 ]; then
 WHISPER_HIGH_VERSION=$1
 shift
fi


           https://launchpad.net/graphite/0.9/0.9.10/+download/whisper-0.9.10.tar.gz

WHISPER_URL=http://launchpad.net/graphite/$WHISPER_HIGH_VERSION/$WHISPER_VERSION/+download/whisper-$WHISPER_VERSION.tar.gz

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

mkdir -p SOURCES

download_file_if_needed $WHISPER_URL SOURCES/whisper-${WHISPER_VERSION}.tar.gz

echo "Version to package is $WHISPER_VERSION"

# prepare fresh directories
rm -rf BUILD RPMS SRPMS TEMP
mkdir -p BUILD RPMS SRPMS TEMP

# Build using rpmbuild (use double-quote for define to have shell resolv vars !)
rpmbuild -bb --define="_topdir $PWD" --define="_tmppath $PWD/TEMP" --define="WHISPER_REL $WHISPER_VERSION"  SPECS/mywhisper.spec

