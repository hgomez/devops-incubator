# di-centos6-base
#
# Devops Incubator image based on CentOS 6
#
# VERSION               0.0.1

FROM     centos:centos6
MAINTAINER Henri Gomez "henri.gomez@gmail.com"

# Install EPEL
RUN curl -L http://mir01.syntis.net/epel/6/x86_64/epel-release-6-8.noarch.rpm -o epel-release.noarch.rpm
RUN rpm -Uvh epel-release.noarch.rpm
RUN rm -f epel-release.noarch.rpm

# Install Devops Incubator
RUN curl -L http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/CentOS_CentOS-6/home:henri_gomez:devops-incubator.repo -o /etc/yum.repos.d/devops-incubator.repo

# Update distribution
RUN yum clean all
RUN yum update -y

# Install Oracle Java 7 
RUN curl -j -k -L -H "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/7u71-b14/jdk-7u71-linux-x64.rpm -o jdk7-linux-x64.rpm
RUN rpm -Uvh jdk7-linux-x64.rpm
RUN rm jdk7-linux-x64.rpm
ENV JAVA_HOME /usr/java/default

# Install basic monitor script
add ./monitor-service.sh /usr/bin/monitor-service.sh
RUN chmod 755 /usr/bin/monitor-service.sh

