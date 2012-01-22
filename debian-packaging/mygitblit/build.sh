#!/bin/bash

pushd `dirname $0`

APP_VERSION=0.8.2
TOMCAT_VERSION=7.0.25


# Build variables
BUILD_DIR=/tmp/BUILD

APTDEP_DIR=/vagrant/aptdepo


# Application variables

APP_NAME=mygitblit
APP_DIR=/opt/$APP_NAME
APP_EXEC=$APP_DIR/bin/catalina.sh
APP_USER=$APP_NAME

APP_DATADIR=/var/lib/$APP_NAME
APP_LOGDIR=/var/log/$APP_NAME
APP_CONFDIR=$APP_DIR/conf

APP_CONFLOCALDIR=$APP_DIR/conf/Catalina/localhost
APP_WEBAPPDIR=$APP_DIR/webapps
APP_TMPDIR=/tmp/$APP_NAME
APP_WORKDIR=/var/$APP_NAME
#APP_VERSION=1.0.0
APP_RELEASE=1

if [ $# -gt 1 ]; then
  APP_VERSION=$1
  shift
fi

if [ $# -gt 1 ]; then
  TOMCAT_VERSION=$1
  shift
fi

GITBLIT_URL=http://gitblit.googlecode.com/files/gitblit-${APP_VERSION}.war
TOMCAT_URL=http://mir2.ovh.net/ftp.apache.org/dist/tomcat/tomcat-7/v${TOMCAT_VERSION}/bin/apache-tomcat-${TOMCAT_VERSION}.tar.gz
CATALINA_JMX_REMOTE_URL=http://mir2.ovh.net/ftp.apache.org/dist/tomcat/tomcat-7/v${TOMCAT_VERSION}/bin/extras/catalina-jmx-remote.jar

if [ ! -d SOURCES ]; then
  echo "Creating sources directory"
  mkdir SOURCES
fi




if [ ! -f SOURCES/downloaded/apache-tomcat-${TOMCAT_VERSION}.tar.gz ]; then
  echo "downloading apache-tomcat-${TOMCAT_VERSION}.tar.gz from $TOMCAT_URL"
  curl -s -L $TOMCAT_URL -o SOURCES/downloaded/apache-tomcat-${TOMCAT_VERSION}.tar.gz
fi

if [ ! -f SOURCES/downloaded/catalina-jmx-remote-${TOMCAT_VERSION}.jar ]; then
  echo "downloading catalina-jmx-remote-${TOMCAT_VERSION}.jar from $CATALINA_JMX_REMOTE_URL"
  curl -s -L $CATALINA_JMX_REMOTE_URL -o SOURCES/downloaded/catalina-jmx-remote-${TOMCAT_VERSION}.jar
fi


if [ ! -f SOURCES/downloaded/$APP_NAME-${APP_VERSION}.war ]; then
  echo "downloading gitblit-${APP_VERSION}.war from $GITBLIT_URL"
  curl  -s -L $GITBLIT_URL -o SOURCES/downloaded/$APP_NAME-${APP_VERSION}.war
fi

echo "Version to package is $APP_VERSION, powered by Apache Tomcat $TOMCAT_VERSION"

#set -x

# prepare fresh directories
rm -rf $BUILD_DIR TMP
mkdir -p $BUILD_DIR TMP

#prepare directory
mkdir -p $BUILD_DIR/$APP_DIR

# copy debian files to build
cp -R debian $BUILD_DIR/

for DEBIANFILE in `ls SOURCES/app.*`; do
  debiandestfile=$APP_NAME${DEBIANFILE#SOURCES/app}
  cp $DEBIANFILE $BUILD_DIR/debian/$debiandestfile;
  sed -i "s|@@SKEL_APP@@|$APP_NAME|g" $BUILD_DIR/debian/$debiandestfile
  sed -i "s|@@SKEL_USER@@|$APP_USER|g" $BUILD_DIR/debian/$debiandestfile
  sed -i "s|@@SKEL_VERSION@@|version $APP_VERSION release $APP_RELEASE powered by Apache Tomcat $TOMCAT_VERSION|g" $BUILD_DIR/debian/$debiandestfile
  sed -i "s|@@SKEL_EXEC@@|$APP_EXEC|g" $BUILD_DIR/debian/$debiandestfile
  sed -i "s|@@SKEL_LOGDIR@@|$APP_LOGDIR|g" $BUILD_DIR/debian/$debiandestfile
  sed -i "s|@@APP_TMPDIR@@|$APP_TMPDIR|g" $BUILD_DIR/debian/$debiandestfile


done


cp SOURCES/control $BUILD_DIR/debian

sed -i "s|@@SKEL_APP@@|$APP_NAME|g" $BUILD_DIR/debian/control
sed -i "s|@@SKEL_APPVERSION@@|$APP_VERSION|g" $BUILD_DIR/debian/control
sed -i "s|@@SKEL_TOMCATVERSION@@|$TOMCAT_VERSION|g" $BUILD_DIR/debian/control


cp SOURCES/changelog $BUILD_DIR/debian

sed -i "s|@@SKEL_APP@@|$APP_NAME|g" $BUILD_DIR/debian/changelog
sed -i "s|@@SKEL_APPVERSION@@|$APP_VERSION|g" $BUILD_DIR/debian/changelog





#prepare tomcat
tar -zxf SOURCES/downloaded/apache-tomcat-${TOMCAT_VERSION}.tar.gz -C TMP
mv TMP/apache-tomcat-${TOMCAT_VERSION}/* $BUILD_DIR/$APP_DIR
cp SOURCES/downloaded/catalina-jmx-remote-${TOMCAT_VERSION}.jar $BUILD_DIR/$APP_DIR/lib




# Prepare config

mkdir -p $BUILD_DIR/etc/opt/

cp SOURCES/myapp.config $BUILD_DIR/etc/opt/$APP_NAME
sed -i "s|@@SKEL_APP@@|$APP_NAME|g" $BUILD_DIR/etc/opt/$APP_NAME
sed -i "s|@@SKEL_APPDIR@@|$APP_DIR|g" $BUILD_DIR/etc/opt/$APP_NAME
sed -i "s|@@SKEL_DATADIR@@|$APP_DATADIR|g" $BUILD_DIR/etc/opt/$APP_NAME
sed -i "s|@@SKEL_LOGDIR@@|$APP_LOGDIR|g" $BUILD_DIR/etc/opt/$APP_NAME
sed -i "s|@@SKEL_USER@@|$APP_USER|g" $BUILD_DIR/etc/opt/$APP_NAME
sed -i "s|@@SKEL_CONFDIR@@|$APP_CONFDIR|g" $BUILD_DIR/etc/opt/$APP_NAME
RANDOMVAL=`echo $RANDOM | md5sum | sed "s| -||g" | tr -d " "`
sed -i "s|@@SKEL_RO_PWD@@|$RANDOMVAL|g" $BUILD_DIR/etc/opt/$APP_NAME
RANDOMVAL=`echo $RANDOM | md5sum | sed "s| -||g" | tr -d " "`
sed -i "s|@@SKEL_RW_PWD@@|$RANDOMVAL|g" $BUILD_DIR/etc/opt/$APP_NAME


# Prepare limits.d
mkdir -p $BUILD_DIR/etc/security/limits.d/
cp SOURCES/myapp.limits.conf $BUILD_DIR/etc/security/limits.d/$APP_NAME.conf

sed -i "s|@@APP_USER@@|$APP_USER|g" $BUILD_DIR/etc/security/limits.d/$APP_NAME.conf





# remove unneeded file in Debian
rm -f $BUILD_DIR/$APP_DIR/*.sh
rm -f $BUILD_DIR/$APP_DIR/*.bat
rm -f $BUILD_DIR/$APP_DIR/bin/*.bat
rm -rf $BUILD_DIR/$APP_DIR/logs
rm -rf $BUILD_DIR/$APP_DIR/temp
rm -rf $BUILD_DIR/$APP_DIR/work

# Copy setenv.sh
cp  SOURCES/setenv.sh $BUILD_DIR/$APP_DIR/bin/
sed -i "s|@@SKEL_APP@@|$APP_NAME|g" $BUILD_DIR/$APP_DIR/bin/setenv.sh
sed -i "s|@@APP_TMPDIR@@|$APP_TMPDIR|g" $BUILD_DIR/$APP_DIR/bin/setenv.sh


chmod 755 $BUILD_DIR/$APP_DIR/bin/*.sh

# Copy .skel
cp  SOURCES/*.skel $BUILD_DIR/$APP_DIR/conf/


# Copy context.xml
cp  SOURCES/myapp.context.xml $BUILD_DIR/$APP_DIR/conf/context.xml
sed -i "s|@@SKEL_DATADIR@@|$APP_DATADIR|g" $BUILD_DIR/$APP_DIR/conf/context.xml

# Copy users.properties

mkdir -p $BUILD_DIR/$APP_DATADIR/conf
#cp SOURCES/myapp.users.properties $BUILD_DIR/$APP_DATADIR/conf/users.properties
cp SOURCES/myapp.users.conf $BUILD_DIR/$APP_DATADIR/conf/users.conf




#Install war
rm -rf $BUILD_DIR/$APP_DIR/webapps/*
cp  SOURCES/downloaded/$APP_NAME-${APP_VERSION}.war $BUILD_DIR/$APP_DIR/webapps/ROOT.war




# create debian package
pushd $BUILD_DIR
debuild -us -uc -B
#ls
popd

cp $BUILD_DIR/../$APP_NAME*.deb .

# Copy the .deb into the APT local depot if exist
if [ -n "$APTDEP_DIR" ]; then
cp $BUILD_DIR/../$APP_NAME*.deb $APTDEP_DIR/binary
fi

popd
