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

APPLICATION_URL=http://mirrors.jenkins-ci.org/war/${APP_VERSION}/jenkins.war
JENKINS_LTS_URL=http://mirrors.jenkins-ci.org/war-stable/${JENKINS_LTS_VERSION}/jenkins.war

if $USE_LTS; then
 APPLICATION_URL=$JENKINS_LTS_URL
 APP_VERSION=$JENKINS_LTS_VERSION
fi


# Global variables

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

#####################################
# Build tasks                       #
#####################################

check_build_dependency
prepare_build

fetch_remote_file $APPLICATION_URL $DOWNLOAD_APP_DIR/${APP_NAME}-${APP_VERSION}.war
fetch_remote_file $TOMCAT_URL $DOWNLOAD_APP_DIR/apache-tomcat-${TOMCAT_VERSION}.tar.gz
fetch_remote_file $CATALINA_JMX_REMOTE_URL $DOWNLOAD_APP_DIR/catalina-jmx-remote-${TOMCAT_VERSION}.jar

build_debian
build_tomcat
build_config
build_limitd 
copy_war
package_deb


popd >> /dev/null
