# di-centos6-base
#
# Devops Incubator image based on CentOS 6
#
# VERSION               0.0.1

FROM     centos:centos6
MAINTAINER Henri Gomez "henri.gomez@gmail.com"

# Java 7 - 7u79 / 7u79-b15
# Java 8 - 8u25 / 8u25-b17

# Default to Java 7
ENV JAVA_VERSION 7u79
ENV JAVA_FULLVERSION 7u79-b15

# Install EPEL
RUN curl -L http://mir01.syntis.net/epel/6/x86_64/epel-release-6-8.noarch.rpm -o epel-release.noarch.rpm && \
    rpm -Uvh epel-release.noarch.rpm && \
    rm -f epel-release.noarch.rpm

# Install Devops Incubator
RUN curl -L http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/CentOS_CentOS-6/home:henri_gomez:devops-incubator.repo -o /etc/yum.repos.d/devops-incubator.repo

# Update distribution
RUN yum clean all && \
    yum update -y

# 
# http://download.oracle.com/otn-pub/java/jdk/7u79-b15/jdk-7u79-linux-i586.tar.gz
#
# Install Oracle Java
RUN curl -j -k -L -H "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/${JAVA_FULLVERSION}/jdk-${JAVA_VERSION}-linux-x64.rpm -o jdk-linux-x64.rpm && \
    rpm -Uvh jdk-linux-x64.rpm && \
    rm jdk-linux-x64.rpm

ENV JAVA_HOME /usr/java/default

# Install basic monitor script
add ./monitor-service.sh /usr/bin/monitor-service.sh
RUN chmod 755 /usr/bin/monitor-service.sh

