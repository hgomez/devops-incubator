BUILD_DIR=/tmp/BUILD
DOWNLOAD_CACHE_DIR=/tmp/devops-incubator-cache
DOWNLOAD_APP_DIR=SOURCES/downloaded

APTDEP_DIR=/vagrant/aptdepo

check_build_dependency(){  
  if which debuild >/dev/null; then
    echo "Debuild found, continue build"
  else
    echo "Debuild not found"
    exit -1;
  fi
}

prepare_build(){
  echo "Prepare build"
  if [ ! -d $DOWNLOAD_APP_DIR ]; then
    echo "Creating sources directory"
    mkdir -p $DOWNLOAD_APP_DIR
  fi

  rm -rf $BUILD_DIR TMP
  mkdir -p $BUILD_DIR TMP

  #prepare directory
  echo $BUILD_DIR/$APP_DIR
  mkdir -p $BUILD_DIR/$APP_DIR

  # copy debian files to build
  cp -R debian $BUILD_DIR/
  }

fetch_remote_file()
{
  URL=$1
  DEST=$2
  BDEST=`basename $DEST`


  if [ ! -f $DEST ]; then

    mkdir -p $DOWNLOAD_CACHE_DIR
    DD_FILE=$DOWNLOAD_CACHE_DIR/$BDEST

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