#!/bin/bash

set -e 


pushd `dirname $0` >> /dev/null

source ../commons-script/functions.sh

APP_VERSION=1.502
JENKINS_LTS_VERSION=1.480.2
TOMCAT_VERSION=7.0.37
USE_LTS=false

if [ $# -gt 1 ]; then
  JENKINS_VERSION=$1
  shift
fi

if [ $# -gt 1 ]; then
  TOMCAT_VERSION=$1
  shift
fi

if [ $# -gt 1 ]; then
  USE_LTS=$1
  shift
fi

JENKINS_URL=http://mirrors.jenkins-ci.org/war/${APP_VERSION}/jenkins.war
JENKINS_LTS_URL=http://mirrors.jenkins-ci.org/war-stable/${JENKINS_LTS_VERSION}/jenkins.war

if $USE_LTS; then
 JENKINS_URL=$JENKINS_LTS_URL
 APP_VERSION=$JENKINS_LTS_VERSION
fi

TOMCAT_URL=http://mir2.ovh.net/ftp.apache.org/dist/tomcat/tomcat-7/v${TOMCAT_VERSION}/bin/apache-tomcat-${TOMCAT_VERSION}.tar.gz
CATALINA_JMX_REMOTE_URL=http://mir2.ovh.net/ftp.apache.org/dist/tomcat/tomcat-7/v${TOMCAT_VERSION}/bin/extras/catalina-jmx-remote.jar


#####################################
# Applications variables            #
#####################################

APP_NAME=myjenkins
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

check_build_dependency
prepare_build


fetch_remote_file $JENKINS_URL $DOWNLOAD_APP_DIR/${APP_NAME}-${APP_VERSION}.war
fetch_remote_file $TOMCAT_URL $DOWNLOAD_APP_DIR/apache-tomcat-${TOMCAT_VERSION}.tar.gz
fetch_remote_file $CATALINA_JMX_REMOTE_URL $DOWNLOAD_APP_DIR/catalina-jmx-remote-${TOMCAT_VERSION}.jar




#####################################
# Prepare Debian packaging files    #
#####################################

for DEBIANFILE in `ls SOURCES/debian/app.*`; do
  debiandestfile=$APP_NAME${DEBIANFILE#SOURCES/debian/app}
  cp $DEBIANFILE $BUILD_DIR/debian/$debiandestfile;
  sed -i "s|@@APP_NAME@@|$APP_NAME|g" $BUILD_DIR/debian/$debiandestfile
  sed -i "s|@@APP_USER@@|$APP_USER|g" $BUILD_DIR/debian/$debiandestfile
  sed -i "s|@@APP_VERSION@@|version $APP_VERSION release $APP_RELEASE powered by Apache Tomcat $TOMCAT_VERSION|g" $BUILD_DIR/debian/$debiandestfile
  sed -i "s|@@APP_EXEC@@|$APP_EXEC|g" $BUILD_DIR/debian/$debiandestfile
  sed -i "s|@@APP_LOGDIR@@|$APP_LOGDIR|g" $BUILD_DIR/debian/$debiandestfile
  sed -i "s|@@APP_TMPDIR@@|$APP_TMPDIR|g" $BUILD_DIR/debian/$debiandestfile
done


cp SOURCES/control $BUILD_DIR/debian

sed -i "s|@@APP_NAME@@|$APP_NAME|g" $BUILD_DIR/debian/control
sed -i "s|@@APP_VERSION@@|$APP_VERSION|g" $BUILD_DIR/debian/control
sed -i "s|@@APP_TOMCATVERSION@@|$TOMCAT_VERSION|g" $BUILD_DIR/debian/control

cp SOURCES/changelog $BUILD_DIR/debian

sed -i "s|@@APP_NAME@@|$APP_NAME|g" $BUILD_DIR/debian/changelog
sed -i "s|@@APP_VERSION@@|$APP_VERSION|g" $BUILD_DIR/debian/changelog



#####################################
# Prepare tomcat container          #
#####################################

tar -zxf SOURCES/downloaded/apache-tomcat-${TOMCAT_VERSION}.tar.gz -C TMP
mv TMP/apache-tomcat-${TOMCAT_VERSION}/* $BUILD_DIR/$APP_DIR
cp SOURCES/downloaded/catalina-jmx-remote-${TOMCAT_VERSION}.jar $BUILD_DIR/$APP_DIR/lib

# remove unneeded file in Debian
rm -f $BUILD_DIR/$APP_DIR/*.sh
rm -f $BUILD_DIR/$APP_DIR/*.bat
rm -f $BUILD_DIR/$APP_DIR/bin/*.bat
rm -rf $BUILD_DIR/$APP_DIR/logs
rm -rf $BUILD_DIR/$APP_DIR/temp
rm -rf $BUILD_DIR/$APP_DIR/work

# Copy setenv.sh
cp  SOURCES/setenv.sh $BUILD_DIR/$APP_DIR/bin/
sed -i "s|@@JENKINS_APP@@|$APP_NAME|g" $BUILD_DIR/$APP_DIR/bin/setenv.sh
sed -i "s|@@APP_TMPDIR@@|$APP_TMPDIR|g" $BUILD_DIR/$APP_DIR/bin/setenv.sh


chmod 755 $BUILD_DIR/$APP_DIR/bin/*.sh

# Copy .skel
cp  SOURCES/*.skel $BUILD_DIR/$APP_DIR/conf/



#####################################
# Prepare config                    #
#####################################

mkdir -p $BUILD_DIR/etc/opt/


cp SOURCES/app.config $BUILD_DIR/etc/opt/$APP_NAME
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

#####################################
# Prepare Limit.d                   #
#####################################

mkdir -p $BUILD_DIR/etc/security/limits.d/
cp SOURCES/app.limits.conf $BUILD_DIR/etc/security/limits.d/$APP_NAME.conf

sed -i "s|@@APP_USER@@|$APP_USER|g" $BUILD_DIR/etc/security/limits.d/$APP_NAME.conf

#####################################
# Install app.war into tomcat       #
#####################################

rm -rf $BUILD_DIR/$APP_DIR/webapps/*
cp  SOURCES/downloaded/$APP_NAME-${APP_VERSION}.war $BUILD_DIR/$APP_DIR/webapps/ROOT.war



#####################################
# Create package                    #
#####################################
pushd $BUILD_DIR
debuild -us -uc -B
#ls
popd

#####################################
# Copy .deb into work dirctory      #
#####################################
cp $BUILD_DIR/../$APP_NAME*.deb .


popd >> /dev/null
