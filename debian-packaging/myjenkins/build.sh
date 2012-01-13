#!/bin/bash


JENKINS_VERSION=1.447
TOMCAT_VERSION=7.0.23

APP_NAME=myjenkins
APP_DIR=/opt/$APP_NAME
APP_EXEC=$APP_DIR/bin/catalina.sh
APP_USER=myjenkins

APP_DATADIR=/var/lib/$APP_NAME
APP_LOGDIR=/var/log/$APP_NAME
APP_CONFDIR=$APP_DIR/conf
APP_CONFLOCALDIR=$APP_DIR/conf/Catalina/localhost
APP_WEBAPPDIR=$APP_DIR/webapps
APP_TMPDIR=/tmp/$APP_NAME
APP_WORKDIR=/var/$APP_NAME

if [ $# -gt 1 ]; then
  JENKINS_VERSION=$1
  shift
fi

if [ $# -gt 1 ]; then
  TOMCAT_VERSION=$1
  shift
fi

JENKINS_URL=http://mirrors.jenkins-ci.org/war/${JENKINS_VERSION}/jenkins.war
TOMCAT_URL=http://mir2.ovh.net/ftp.apache.org/dist/tomcat/tomcat-7/v${TOMCAT_VERSION}/bin/apache-tomcat-${TOMCAT_VERSION}.tar.gz
CATALINA_JMX_REMOTE_URL=http://mir2.ovh.net/ftp.apache.org/dist/tomcat/tomcat-7/v${TOMCAT_VERSION}/bin/extras/catalina-jmx-remote.jar

if [ ! -d SOURCES ]; then
  echo "Creating sources directory"
  mkdir SOURCES
fi

if [ ! -f SOURCES/jenkins-${JENKINS_VERSION}.war ]; then
  echo "downloading jenkins-${JENKINS_VERSION}.war from $JENKINS_URL"
  curl -s -L $JENKINS_URL -o SOURCES/jenkins-${JENKINS_VERSION}.war
fi

if [ ! -f SOURCES/apache-tomcat-${TOMCAT_VERSION}.tar.gz ]; then
  echo "downloading apache-tomcat-${TOMCAT_VERSION}.tar.gz from $TOMCAT_URL"
  curl -s -L $TOMCAT_URL -o SOURCES/apache-tomcat-${TOMCAT_VERSION}.tar.gz
fi

if [ ! -f SOURCES/catalina-jmx-remote-${TOMCAT_VERSION}.jar ]; then
  echo "downloading catalina-jmx-remote-${TOMCAT_VERSION}.jar from $CATALINA_JMX_REMOTE_URL"
  curl -s -L $CATALINA_JMX_REMOTE_URL -o SOURCES/catalina-jmx-remote-${TOMCAT_VERSION}.jar
fi

echo "Version to package is $JENKINS_VERSION, powered by Apache Tomcat $TOMCAT_VERSION"

set -x

# prepare fresh directories
rm -rf BUILD TMP
mkdir -p BUILD TMP

#prepare directory
mkdir -p BUILD$APP_DIR

# copy debian files to build 
cp -R debian BUILD

#prepare tomcat
tar -zxf SOURCES/apache-tomcat-${TOMCAT_VERSION}.tar.gz -C TMP
mv TMP/apache-tomcat-${TOMCAT_VERSION}/* BUILD/$APP_DIR
cp SOURCES/catalina-jmx-remote-${TOMCAT_VERSION}.jar BUILD/$APP_DIR/lib


# Prepare init.d script
cp  SOURCES/myjenkins.initd BUILD/debian/$APP_NAME.init
sed -i "s|@@SKEL_APP@@|$APP_NAME|g" BUILD/debian/$APP_NAME.init
sed -i "s|@@SKEL_USER@@|$APP_USER|g" BUILD/debian/$APP_NAME.init
sed -i "s|@@SKEL_VERSION@@|version %{version} release %{release}|g" BUILD/debian/$APP_NAME.init
sed -i "s|@@SKEL_EXEC@@|$APP_EXEC|g" BUILD/debian/$APP_NAME.init

# Prepare config

mkdir -p BUILD/etc/opt/

cp SOURCES/myjenkins.config BUILD/etc/opt/myjenkins

sed -i "s|@@SKEL_APP@@|$APP_NAME|g" BUILD/etc/opt/myjenkins
sed -i "s|@@SKEL_APPDIR@@|$APP_DIR|g" BUILD/etc/opt/myjenkins
sed -i "s|@@SKEL_DATADIR@@|$APP_DATADIR|g" BUILD/etc/opt/myjenkins
sed -i "s|@@SKEL_LOGDIR@@|$APP_LOGDIR|g" BUILD/etc/opt/myjenkins
sed -i "s|@@SKEL_USER@@|$APP_USER|g" BUILD/etc/opt/myjenkins
sed -i "s|@@SKEL_CONFDIR@@|$APP_CONFDIR|g" BUILD/etc/opt/myjenkins

# remove uneeded file in RPM
rm -f BUILD/$APPS_DIR/$APP_NAME/*.sh
rm -f BUILD/$APPS_DIR/$APP_NAME/*.bat
rm -f BUILD/$APPS_DIR/$APP_NAME/*.bat
rm -rf BUILD/$APPS_DIR/$APP_NAME/logs
rm -rf BUILD/$APPS_DIR/$APP_NAME/temp
rm -rf BUILD/$APPS_DIR/$APP_NAME/work

chmod 755 BUILD/$APPS_DIR/$APP_NAME/bin/*.sh

# Copy .skel
cp  SOURCES/*.skel BUILD/$APP_DIR/conf/


cp  SOURCES/setenv.sh BUILD/$APP_DIR/bin/
sed -i 's|@@SKEL_APP@@|$APP_NAME|g' BUILD/$APP_DIR/bin/



# create debian package
pushd BUILD
debuild -us -uc -B
#ls
popd


