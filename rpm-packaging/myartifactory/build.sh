#!/bin/sh

ARTIFACTORY_VERSION=2.5.1
TOMCAT_VERSION=7.0.26

if [ $# -ge 1 ]; then
	ARTIFACTORY_VERSION=$1
	shift
fi

if [ $# -ge 1 ]; then
	TOMCAT_VERSION=$1
	shift
fi

ARTIFACTORY_URL=http://dfn.dl.sourceforge.net/project/artifactory/artifactory/${ARTIFACTORY_VERSION}/artifactory-${ARTIFACTORY_VERSION}.zip
TOMCAT_URL=http://mir2.ovh.net/ftp.apache.org/dist/tomcat/tomcat-7/v${TOMCAT_VERSION}/bin/apache-tomcat-${TOMCAT_VERSION}.tar.gz
CATALINA_JMX_REMOTE_URL=http://mir2.ovh.net/ftp.apache.org/dist/tomcat/tomcat-7/v${TOMCAT_VERSION}/bin/extras/catalina-jmx-remote.jar

fetch_remote_file()
{
	URL=$1
	DEST=$2

	if [ ! -f $2 ]; then

		DROP_DIR=~/DROP_DIR
		mkdir -p $DROP_DIR
		DD_FILE=$DROP_DIR\`basename $2`

		if [ -f $DD_FILE ]; then
			cp $DD_FILE $2
		else
			echo "downloading from $1 to $2..."
			curl -L $1 -o $DD_FILE

			case $1 in
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
				echo "invalid content `basename $2` downloaded from $1, discarding content and aborting build."
				exit -1
			else
				cp $DD_FILE $2
			fi

	fi
}

fetch_remote_file $ARTIFACTORY_URL SOURCES/artifactory-${ARTIFACTORY_VERSION}.zip
fetch_remote_file $TOMCAT_URL SOURCES/apache-tomcat-${TOMCAT_VERSION}.tar.gz
fetch_remote_file $CATALINA_JMX_REMOTE_URL SOURCES/catalina-jmx-remote-${TOMCAT_VERSION}.jar

echo "Version to package is $ARTIFACTORY_VERSION, powered by Apache Tomcat $TOMCAT_VERSION"

# prepare fresh directories
rm -rf BUILD RPMS SRPMS TEMP
mkdir -p BUILD RPMS SRPMS TEMP

# Build using rpmbuild (use double-quote for define to have shell resolv vars !)
rpmbuild -bb --define="_topdir $PWD" --define="_tmppath $PWD/TEMP" --define="TOMCAT_REL $TOMCAT_VERSION" --define="ARTIFACTORY_REL $ARTIFACTORY_VERSION" SPECS/myartifactory.spec

