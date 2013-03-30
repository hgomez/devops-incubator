#!/bin/sh

if [ -z "$ARCHIVA_VERSION" ]; then
  ARCHIVA_VERSION=1.4-M3
fi

if [ -z "$TOMCAT_VERSION" ]; then
  TOMCAT_VERSION=7.0.39
fi

if [ -z "$ACTIVATION_VERSION" ]; then
  ACTIVATION_VERSION=1.1.1
fi

if [ -z "$MAIL_VERSION" ]; then
  MAIL_VERSION=1.4.5
fi

if [ -z "$DERBY_VERSION" ]; then
  DERBY_VERSION=10.9.1.0
fi

ARCHIVA_URL=http://mir2.ovh.net/ftp.apache.org/dist/archiva/${ARCHIVA_VERSION}/binaries/apache-archiva-js-${ARCHIVA_VERSION}.war
TOMCAT_URL=http://archive.apache.org/dist/tomcat/tomcat-7/v${TOMCAT_VERSION}/bin/apache-tomcat-${TOMCAT_VERSION}.tar.gz
CATALINA_JMX_REMOTE_URL=http://archive.apache.org/dist/tomcat/tomcat-7/v${TOMCAT_VERSION}/bin/extras/catalina-jmx-remote.jar
ACTIVATION_URL=http://central.maven.org/maven2/javax/activation/activation/${ACTIVATION_VERSION}/activation-${ACTIVATION_VERSION}.jar
MAIL_URL=http://central.maven.org/maven2/javax/mail/mail/${MAIL_VERSION}/mail-${MAIL_VERSION}.jar
DERBY_URL=http://central.maven.org/maven2/org/apache/derby/derby/${DERBY_VERSION}/derby-${DERBY_VERSION}.jar

download_file_if_needed()
{
	URL=$1
	DEST=$2

	if [ ! -f $DEST ]; then

		echo "downloading from $URL to $DEST..."
		curl -L $URL -o $DEST

		case $DEST in
			*.tar.gz)
	        	tar tzf $DEST >>/dev/null 2>&1
	        	;;
	    	*.zip)
	        	unzip -t $DEST >>/dev/null 2>&1
	        	;;
	    	*.jar)
	        	unzip -t $DEST >>/dev/null 2>&1
	        	;;
	    	*.war)
	        	unzip -t $DEST >>/dev/null 2>&1
	        	;;
		esac

		if [ $? != 0 ]; then
			rm -f $DEST
			echo "invalid content for `basename $DEST` downloaded from $URL, discarding content and aborting build."
			exit -1
		fi

	fi
}

download_file_if_needed $ARCHIVA_URL SOURCES/apache-archiva-${ARCHIVA_VERSION}.war
download_file_if_needed $TOMCAT_URL SOURCES/apache-tomcat-${TOMCAT_VERSION}.tar.gz
download_file_if_needed $CATALINA_JMX_REMOTE_URL SOURCES/catalina-jmx-remote-${TOMCAT_VERSION}.jar
download_file_if_needed $ACTIVATION_URL SOURCES/activation-${ACTIVATION_VERSION}.jar
download_file_if_needed $MAIL_URL SOURCES/mail-${MAIL_VERSION}.jar
download_file_if_needed $DERBY_URL SOURCES/derby-${DERBY_VERSION}.jar

echo "Version to package is $ARCHIVA_VERSION, powered by Apache Tomcat $TOMCAT_VERSION"

# prepare fresh directories
rm -rf BUILD RPMS SRPMS TEMP
mkdir -p BUILD RPMS SRPMS TEMP

# Build using rpmbuild (use double-quote for define to have shell resolv vars !)
rpmbuild -bb --define="_topdir $PWD" --define="_tmppath $PWD/TEMP" --define="TOMCAT_REL $TOMCAT_VERSION" --define="ARCHIVA_REL $ARCHIVA_VERSION" \
	     --define="ACTIVATION_REL $ACTIVATION_VERSION" --define="MAIL_REL $MAIL_VERSION" --define="DERBY_REL $DERBY_VERSION" \
	     SPECS/myarchiva.spec

