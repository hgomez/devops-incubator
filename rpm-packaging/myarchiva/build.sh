#!/bin/sh

if [ -z "$ARCHIVA_VERSION" ]; then
  ARCHIVA_VERSION=2.1.1
fi

if [ -z "$TOMCAT_VERSION" ]; then
  TOMCAT_VERSION=7.0.65
fi

if [ -z "$ACTIVATION_VERSION" ]; then
  ACTIVATION_VERSION=1.1.1
fi

if [ -z "$MAIL_VERSION" ]; then
  MAIL_VERSION=1.4.7
fi

if [ -z "$DERBY_VERSION" ]; then
  DERBY_VERSION=10.10.2.0
fi

ARCHIVA_URL=http://apache.mirrors.multidist.eu/archiva/${ARCHIVA_VERSION}/binaries/apache-archiva-${ARCHIVA_VERSION}.war
TOMCAT_URL=http://apache.mirrors.multidist.eu/tomcat/tomcat-7/v${TOMCAT_VERSION}/bin/apache-tomcat-${TOMCAT_VERSION}.tar.gz
CATALINA_JMX_REMOTE_URL=http://apache.mirrors.multidist.eu/tomcat/tomcat-7/v${TOMCAT_VERSION}/bin/extras/catalina-jmx-remote.jar
ACTIVATION_URL=http://central.maven.org/maven2/javax/activation/activation/${ACTIVATION_VERSION}/activation-${ACTIVATION_VERSION}.jar
MAIL_URL=http://central.maven.org/maven2/javax/mail/mail/${MAIL_VERSION}/mail-${MAIL_VERSION}.jar
DERBY_URL=http://central.maven.org/maven2/org/apache/derby/derby/${DERBY_VERSION}/derby-${DERBY_VERSION}.jar

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


fetch_remote_file $ARCHIVA_URL SOURCES/apache-archiva-${ARCHIVA_VERSION}.war
fetch_remote_file $TOMCAT_URL SOURCES/apache-tomcat-${TOMCAT_VERSION}.tar.gz
fetch_remote_file $CATALINA_JMX_REMOTE_URL SOURCES/catalina-jmx-remote-${TOMCAT_VERSION}.jar
fetch_remote_file $ACTIVATION_URL SOURCES/activation-${ACTIVATION_VERSION}.jar
fetch_remote_file $MAIL_URL SOURCES/mail-${MAIL_VERSION}.jar
fetch_remote_file $DERBY_URL SOURCES/derby-${DERBY_VERSION}.jar

echo "Version to package is $ARCHIVA_VERSION, powered by Apache Tomcat $TOMCAT_VERSION"

# prepare fresh directories
rm -rf BUILD RPMS SRPMS TEMP
mkdir -p BUILD RPMS SRPMS TEMP

# Build using rpmbuild (use double-quote for define to have shell resolv vars !)
rpmbuild -bb --define="_topdir $PWD" --define="_tmppath $PWD/TEMP" --define="TOMCAT_REL $TOMCAT_VERSION" --define="ARCHIVA_REL $ARCHIVA_VERSION" \
	     --define="ACTIVATION_REL $ACTIVATION_VERSION" --define="MAIL_REL $MAIL_VERSION" --define="DERBY_REL $DERBY_VERSION" \
	     SPECS/myarchiva.spec

