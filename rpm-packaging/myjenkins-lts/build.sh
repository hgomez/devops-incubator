#!/bin/sh

JENKINS_LTS_VERSION=1.651.3
TOMCAT_VERSION=7.0.70

if [ $# -gt 1 ]; then
  JENKINS_VERSION=$1
  shift
fi

if [ $# -gt 1 ]; then
  TOMCAT_VERSION=$1
  shift
fi

JENKINS_LTS_URL=http://mirrors.jenkins-ci.org/war-stable/${JENKINS_LTS_VERSION}/jenkins.war

JENKINS_URL=$JENKINS_LTS_URL
JENKINS_VERSION=$JENKINS_LTS_VERSION

TOMCAT_URL=http://archive.apache.org/dist/tomcat/tomcat-7/v${TOMCAT_VERSION}/bin/apache-tomcat-${TOMCAT_VERSION}.tar.gz
CATALINA_JMX_REMOTE_URL=http://archive.apache.org/dist/tomcat/tomcat-7/v${TOMCAT_VERSION}/bin/extras/catalina-jmx-remote.jar

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

fetch_remote_file $JENKINS_URL SOURCES/jenkins-${JENKINS_VERSION}.war
fetch_remote_file $TOMCAT_URL SOURCES/apache-tomcat-${TOMCAT_VERSION}.tar.gz
fetch_remote_file $CATALINA_JMX_REMOTE_URL SOURCES/catalina-jmx-remote-${TOMCAT_VERSION}.jar

echo "Version to package is $JENKINS_VERSION, powered by Apache Tomcat $TOMCAT_VERSION"

# prepare fresh directories
rm -rf BUILD RPMS SRPMS TEMP
mkdir -p BUILD RPMS SRPMS TEMP

# Build using rpmbuild (use double-quote for define to have shell resolv vars !)
rpmbuild -bb --define="_topdir $PWD" --define="_tmppath $PWD/TEMP" --define="TOMCAT_REL $TOMCAT_VERSION" --define="JENKINS_REL $JENKINS_VERSION"  SPECS/myjenkins-lts.spec

