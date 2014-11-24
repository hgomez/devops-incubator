# di-centos6-base
#
# Devops Incubator image based on CentOS 6
#
# VERSION               0.0.1

FROM     centos:centos6
MAINTAINER Henri Gomez "henri.gomez@gmail.com"

# Register Devops Incubator for CentOS 6
RUN echo "[home_henri_gomez_devops-incubator]" >> /etc/yum.repos.d/devops-incubator.repo
RUN echo "name=Devops Incubator Packages   (CentOS_CentOS-6)" >> /etc/yum.repos.d/devops-incubator.repo
RUN echo "type=rpm-md" >> /etc/yum.repos.d/devops-incubator.repo
RUN echo "baseurl=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/CentOS_CentOS-6/" >> /etc/yum.repos.d/devops-incubator.repo
RUN echo "gpgcheck=1" >> /etc/yum.repos.d/devops-incubator.repo
RUN echo "gpgkey=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/CentOS_CentOS-6/repodata/repomd.xml.key" >> /etc/yum.repos.d/devops-incubator.repo
RUN echo "enabled=1" >> /etc/yum.repos.d/devops-incubator.repo

# Update distribution
RUN yum clean all
RUN yum update -y

# Install wget
RUN yum install wget

# Install Oracle Java 7 
RUN wget --no-check-certificate --no-cookies --no-check-certificate --header "Cookie: oraclelicense=accept-securebackup-cookie" -O jdk7-linux-x64.rpm "http://download.oracle.com/otn-pub/java/jdk/7u71-b14/jdk-7u71-linux-x64.rpm"
RUN rpm -Uvh jdk7-linux-x64.rpm
RUN rm jdk7-linux-x64.rpm
ENV JAVA_HOME /usr/java/default
