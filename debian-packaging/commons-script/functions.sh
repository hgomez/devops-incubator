SOURCES_DIR=SOURCES
BUILD_DIR=/tmp/BUILD
DOWNLOAD_CACHE_DIR=/tmp/devops-incubator-cache
DOWNLOAD_APP_DIR=SOURCES/downloaded

APTDEP_DIR=/vagrant/aptdepo


#
# Check that needed tools are already installed
#
check_build_dependency(){  
  if which debuild >/dev/null; then
    echo "Debuild found, continue build"
  else
    echo "Debuild not found"
    echo "aptitude install devscripts"
    exit -1;
  fi
}


#
# Create build directory
#
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


#
# Fetch and cache remote files
#
fetch_remote_file()
{
  echo "Fetch remote from $1"

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

copy_war(){
  echo "Copy war"
  rm -rf $BUILD_DIR/$APP_DIR/webapps/*
  cp  $SOURCES_DIR/downloaded/$APP_NAME-${APP_VERSION}.war $BUILD_DIR/$APP_DIR/webapps/ROOT.war
}

build_debian(){
  echo "Prepare debian packaging files"
  for DEBIANFILE in `ls $SOURCES_DIR/debian/app.*`; do
  debiandestfile=$APP_NAME${DEBIANFILE#SOURCES/debian/app}
  echo "$DEBIANFILE -> $debiandestfile"
  cp $DEBIANFILE $BUILD_DIR/debian/$debiandestfile;
  sed -i "s|@@APP_NAME@@|$APP_NAME|g" $BUILD_DIR/debian/$debiandestfile
  sed -i "s|@@APP_USER@@|$APP_USER|g" $BUILD_DIR/debian/$debiandestfile
  sed -i "s|@@APP_VERSION@@|version $APP_VERSION release $APP_RELEASE powered by Apache Tomcat $TOMCAT_VERSION|g" $BUILD_DIR/debian/$debiandestfile
  sed -i "s|@@APP_EXEC@@|$APP_EXEC|g" $BUILD_DIR/debian/$debiandestfile
  sed -i "s|@@APP_LOGDIR@@|$APP_LOGDIR|g" $BUILD_DIR/debian/$debiandestfile
  sed -i "s|@@APP_TMPDIR@@|$APP_TMPDIR|g" $BUILD_DIR/debian/$debiandestfile
done


  cp $SOURCES_DIR/control $BUILD_DIR/debian

  sed -i "s|@@APP_NAME@@|$APP_NAME|g" $BUILD_DIR/debian/control
  sed -i "s|@@APP_VERSION@@|$APP_VERSION|g" $BUILD_DIR/debian/control
  sed -i "s|@@APP_TOMCATVERSION@@|$TOMCAT_VERSION|g" $BUILD_DIR/debian/control

  cp $SOURCES_DIR/changelog $BUILD_DIR/debian

  sed -i "s|@@APP_NAME@@|$APP_NAME|g" $BUILD_DIR/debian/changelog
  sed -i "s|@@APP_VERSION@@|$APP_VERSION|g" $BUILD_DIR/debian/changelog
}

build_config(){
  echo "Prepare application configuration file"
  mkdir -p $BUILD_DIR/etc/opt/

  cp $SOURCES_DIR/app.config $BUILD_DIR/etc/opt/$APP_NAME
  sed -i "s|@@APP_NAME@@|$APP_NAME|g" $BUILD_DIR/etc/opt/$APP_NAME
  sed -i "s|@@APP_APPDIR@@|$APP_DIR|g" $BUILD_DIR/etc/opt/$APP_NAME
  sed -i "s|@@APP_DATADIR@@|$APP_DATADIR|g" $BUILD_DIR/etc/opt/$APP_NAME
  sed -i "s|@@APP_LOGDIR@@|$APP_LOGDIR|g" $BUILD_DIR/etc/opt/$APP_NAME
  sed -i "s|@@APP_USER@@|$APP_USER|g" $BUILD_DIR/etc/opt/$APP_NAME
  sed -i "s|@@APP_CONFDIR@@|$APP_CONFDIR|g" $BUILD_DIR/etc/opt/$APP_NAME
  RANDOMVAL=`echo $RANDOM | md5sum | sed "s| -||g" | tr -d " "`
  sed -i "s|@@APP_RO_PWD@@|$RANDOMVAL|g" $BUILD_DIR/etc/opt/$APP_NAME
  RANDOMVAL=`echo $RANDOM | md5sum | sed "s| -||g" | tr -d " "`
  sed -i "s|@@APP_RW_PWD@@|$RANDOMVAL|g" $BUILD_DIR/etc/opt/$APP_NAME
}

build_limitd(){
  echo "Prepare limits.conf"
  mkdir -p $BUILD_DIR/etc/security/limits.d/
  cp $SOURCES_DIR/app.limits.conf $BUILD_DIR/etc/security/limits.d/$APP_NAME.conf

  sed -i "s|@@APP_USER@@|$APP_USER|g" $BUILD_DIR/etc/security/limits.d/$APP_NAME.conf


}

build_tomcat(){
  echo "Prepare tomcat installation"
  tar -zxf $SOURCES_DIR/downloaded/apache-tomcat-${TOMCAT_VERSION}.tar.gz -C TMP
  mv TMP/apache-tomcat-${TOMCAT_VERSION}/* $BUILD_DIR/$APP_DIR
  cp $SOURCES_DIR/downloaded/catalina-jmx-remote-${TOMCAT_VERSION}.jar $BUILD_DIR/$APP_DIR/lib

  # remove unneeded file in Debian
  rm -f $BUILD_DIR/$APP_DIR/*.sh
  rm -f $BUILD_DIR/$APP_DIR/*.bat
  rm -f $BUILD_DIR/$APP_DIR/bin/*.bat
  rm -rf $BUILD_DIR/$APP_DIR/logs
  rm -rf $BUILD_DIR/$APP_DIR/temp
  rm -rf $BUILD_DIR/$APP_DIR/work

  # Copy setenv.sh
  cp  $SOURCES_DIR/setenv.sh $BUILD_DIR/$APP_DIR/bin/
  sed -i "s|@@APP_NAME@@|$APP_NAME|g" $BUILD_DIR/$APP_DIR/bin/setenv.sh
  sed -i "s|@@APP_TMPDIR@@|$APP_TMPDIR|g" $BUILD_DIR/$APP_DIR/bin/setenv.sh


  chmod 755 $BUILD_DIR/$APP_DIR/bin/*.sh

  # Copy .skel
  cp  $SOURCES_DIR/*.skel $BUILD_DIR/$APP_DIR/conf/
}


package_deb(){
  echo "Package .deb"
  pushd $BUILD_DIR
  debuild -us -uc -B
  popd
  cp $BUILD_DIR/../$APP_NAME*.deb .

}