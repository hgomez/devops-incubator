#!/bin/sh

if [ $# -ge 1 ]; then
 JMXTRANS_VERSION=$1
 shift
fi

if [ -z "$JMXTRANS_VERSION" ]; then

  JMXTRANS_VERSION=`date +%Y%m%d`
  rm -f SOURCES/jmxtrans-*.tar.gz
  git clone https://github.com/jmxtrans/jmxtrans.git
  mv jmxtrans jmxtrans-$JMXTRANS_VERSION
  tar cvzf SOURCES/jmxtrans-$JMXTRANS_VERSION.tar.gz jmxtrans-$JMXTRANS_VERSION

else
  #
  # https://github.com/jmxtrans/jmxtrans/archive/v242.tar.gz
  #
  JMXTRANS_URL=https://github.com/jmxtrans/jmxtrans/archive/v${JMXTRANS_VERSION}.tar.gz
  download_file_if_needed $JMXTRANS_URL SOURCES/jmxtrans-v${JMXTRANS_VERSION}.tar.gz
fi

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

fetch_remote_file $JMXTRANS_URL SOURCES/jmxtrans-${JMXTRANS_VERSION}.tar.gz

echo "Version to package is $JMXTRANS_VERSION"

# prepare fresh directories
rm -rf BUILD RPMS SRPMS TEMP
mkdir -p BUILD RPMS SRPMS TEMP

# Build using rpmbuild (use double-quote for define to have shell resolv vars !)
rpmbuild -bb --define="_topdir $PWD" --define="_tmppath $PWD/TEMP" --define="JMXTRANS_REL $JMXTRANS_VERSION" SPECS/myjmxtrans.spec

