#!/bin/sh

JENKINS_VERSION=1.441
TOMCAT_VERSION=7.0.23

if [ $# -gt 1 ]; then
  JENKINS_VERSION=$1
  shift
fi

if [ $# -gt 1 ]; then
  TOMCAT_VERSION=$1
  shift
fi

JENKINS_URL=http://mirrors.jenkins-ci.org/war/${JENKINS_VERSION}/jenkins.war
TOMCAT_URL=http://apache.cict.fr/tomcat/tomcat-7/v${TOMCAT_VERSION}/bin/apache-tomcat-${TOMCAT_VERSION}.tar.gz

if [ ! -f SOURCES/apache-tomcat-${TOMCAT_VERSION}.tar.gz ]; then
  echo "downloading apache-tomcat-${TOMCAT_VERSION}.tar.gz from $TOMCAT_URL"
  curl -L $TOMCAT_URL -o SOURCES/apache-tomcat-${TOMCAT_VERSION}.tar.gz
fi

if [ ! -f SOURCES/jenkins-${JENKINS_VERSION}.war ]; then
  echo "downloading jenkins-${JENKINS_VERSION}.war from $JENKINS_URL"
  curl -L $JENKINS_URL -o SOURCES/jenkins-${JENKINS_VERSION}.war
fi

echo "Version to package is $JENKINS_VERSION, powered by Apache Tomcat $TOMCAT_VERSION"

# prepare fresh directories
rm -rf BUILD RPMS SRPMS TEMP
mkdir -p BUILD RPMS SRPMS TEMP

# Build using rpmbuild (use double-quote for define to have shell resolv vars !)
rpmbuild -bb --define="_topdir $PWD" --define="_tmppath $PWD/TEMP" --define="tomcat_rel $TOMCAT_VERSION" --define="jenkinsrel_rel $JENKINS_VERSION"  SPECS/myjenkins.spec

