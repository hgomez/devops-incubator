#!/bin/sh

NEXUS_VERSION=2.10.0
NEXUS_DOWNLOAD_VERSION=2.10.0-02
TOMCAT_VERSION=7.0.55

if [ $# -gt 1 ]; then
  NEXUS_VERSION=$1
  NEXUS_DOWNLOAD_VERSION=$1
  shift
fi

if [ $# -gt 1 ]; then
  TOMCAT_VERSION=$1
  shift
fi

if [ $# -gt 1 ]; then
  NEXUS_DOWNLOAD_VERSION=$1
  shift
fi

NEXUS_URL=http://download.sonatype.com/nexus/oss/nexus-${NEXUS_DOWNLOAD_VERSION}.war
TOMCAT_URL=http://archive.apache.org/dist/tomcat/tomcat-7/v${TOMCAT_VERSION}/bin/apache-tomcat-${TOMCAT_VERSION}.tar.gz
CATALINA_JMX_REMOTE_URL=http://archive.apache.org/dist/tomcat/tomcat-7/v${TOMCAT_VERSION}/bin/extras/catalina-jmx-remote.jar

NEXUS_P2_BRIDGE_URL=http://repo1.maven.org/maven2/org/sonatype/nexus/plugins/nexus-p2-bridge-plugin/${NEXUS_DOWNLOAD_VERSION}/nexus-p2-bridge-plugin-${NEXUS_DOWNLOAD_VERSION}-bundle.zip
NEXUS_P2_REPO_URL=http://repo1.maven.org/maven2/org/sonatype/nexus/plugins/nexus-p2-repository-plugin/${NEXUS_DOWNLOAD_VERSION}/nexus-p2-repository-plugin-${NEXUS_DOWNLOAD_VERSION}-bundle.zip

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

fetch_remote_file $NEXUS_URL SOURCES/nexus-${NEXUS_VERSION}.war
fetch_remote_file $TOMCAT_URL SOURCES/apache-tomcat-${TOMCAT_VERSION}.tar.gz
fetch_remote_file $CATALINA_JMX_REMOTE_URL SOURCES/catalina-jmx-remote-${TOMCAT_VERSION}.jar
fetch_remote_file $NEXUS_P2_BRIDGE_URL SOURCES/nexus-p2-bridge-plugin-${NEXUS_DOWNLOAD_VERSION}-bundle.zip
fetch_remote_file $NEXUS_P2_REPO_URL SOURCES/nexus-p2-repository-plugin-${NEXUS_DOWNLOAD_VERSION}-bundle.zip

echo "Version to package is $NEXUS_VERSION, powered by Apache Tomcat $TOMCAT_VERSION"

# prepare fresh directories
rm -rf BUILD RPMS SRPMS TEMP
mkdir -p BUILD RPMS SRPMS TEMP

# Build using rpmbuild (use double-quote for define to have shell resolv vars !)
rpmbuild -bb --define="_topdir $PWD" --define="_tmppath $PWD/TEMP" --define="TOMCAT_REL $TOMCAT_VERSION" --define="NEXUS_REL $NEXUS_VERSION" --define="NEXUS_FULL_REL $NEXUS_DOWNLOAD_VERSION" SPECS/mynexus.spec

