#!/bin/sh

GITBLIT_VERSION=0.8.2
TOMCAT_VERSION=7.0.26

if [ $# -gt 1 ]; then
  GITBLIT_VERSION=$1
  shift
fi

if [ $# -gt 1 ]; then
  TOMCAT_VERSION=$1
  shift
fi

GITBLIT_URL=http://gitblit.googlecode.com/files/gitblit-${GITBLIT_VERSION}.war
TOMCAT_URL=http://mir2.ovh.net/ftp.apache.org/dist/tomcat//tomcat-7/v${TOMCAT_VERSION}/bin/apache-tomcat-${TOMCAT_VERSION}.tar.gz
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

fetch_remote_file $GITBLIT_URL SOURCES/gitblit-${GITBLIT_VERSION}.war
fetch_remote_file $TOMCAT_URL SOURCES/apache-tomcat-${TOMCAT_VERSION}.tar.gz
fetch_remote_file $CATALINA_JMX_REMOTE_URL SOURCES/catalina-jmx-remote-${TOMCAT_VERSION}.jar

echo "Version to package is $GITBLIT_VERSION powered by Apache Tomcat $TOMCAT_VERSION"

# prepare fresh directories
rm -rf BUILD RPMS SRPMS TEMP
mkdir -p BUILD RPMS SRPMS TEMP

# Build using rpmbuild (use double-quote for define to have shell resolv vars !)
rpmbuild -ba --define="_topdir $PWD" --define="_tmppath $PWD/TEMP" --define="TOMCAT_REL $TOMCAT_VERSION" --define="GITBLIT_REL $GITBLIT_VERSION"  SPECS/mygitblit.spec

