# hgomez/gatling
#
# Gatling based on CentOS 6
# Bundle Gatling 2.0.3 with Java 8u25 
#
# VERSION               0.0.1
# 

FROM     centos:centos6
MAINTAINER Henri Gomez "henri.gomez@gmail.com"

# Gatling 2.0.3
ENV GATLING_VERSION 2.0.3

# Java 7 - 7u71 / 7u71-b14 
# Java 8 - 8u25 / 8u25-b17
ENV JAVA_VERSION 8u25
ENV JAVA_FULLVERSION 8u25-b17


# Install EPEL
RUN curl -L http://mir01.syntis.net/epel/6/x86_64/epel-release-6-8.noarch.rpm -o epel-release.noarch.rpm
RUN rpm -Uvh epel-release.noarch.rpm
RUN rm -f epel-release.noarch.rpm

# Update distribution
RUN yum clean all
RUN yum update -y

# Install unzip
RUN yum install unzip -y

# Install Oracle Java 
RUN curl -j -k -L -H "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/${JAVA_FULLVERSION}/jdk-${JAVA_VERSION}-linux-x64.rpm -o jdk-linux-x64.rpm
RUN rpm -Uvh jdk-linux-x64.rpm
RUN rm jdk-linux-x64.rpm

# Install Gatling
RUN curl -L -v http://repo1.maven.org/maven2/io/gatling/highcharts/gatling-charts-highcharts/${GATLING_VERSION}/gatling-charts-highcharts-${GATLING_VERSION}-bundle.zip -o gatling-charts-highcharts-${GATLING_VERSION}-bundle.zip
RUN unzip gatling-charts-highcharts-${GATLING_VERSION}-bundle.zip
RUN rm -f gatling-charts-highcharts-${GATLING_VERSION}-bundle.zip
RUN mv gatling-charts-highcharts-${GATLING_VERSION} /opt/gatling

ENV PATH $PATH:/opt/gatling/bin
ENV JAVA_HOME /usr/java/default
ENV GATLING_HOME /opt/gatling

ENTRYPOINT ["gatling.sh"]

