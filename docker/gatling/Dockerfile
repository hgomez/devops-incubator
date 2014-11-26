# hgomez/gatling
#
# Gatling based on CentOS 6
#
# VERSION               0.0.1

FROM     centos:centos6
MAINTAINER Henri Gomez "henri.gomez@gmail.com"

# Install EPEL
RUN curl -L http://mir01.syntis.net/epel/6/x86_64/epel-release-6-8.noarch.rpm -o epel-release.noarch.rpm
RUN rpm -Uvh epel-release.noarch.rpm
RUN rm -f epel-release.noarch.rpm

# Update distribution
RUN yum clean all
RUN yum update -y

# Install tar
RUN yum install tar -y

# Install Oracle Java 8 
RUN curl -j -k -L -H "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u25-b17/jdk-8u25-linux-x64.rpm -o jdk8-linux-x64.rpm
RUN rpm -Uvh jdk8-linux-x64.rpm
RUN rm jdk8-linux-x64.rpm

# Install Oracle Java 7
#RUN curl -j -k -L -H "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/7u71-b14/jdk-7u71-linux-x64.rpm -o jdk7-linux-x64.rpm
#RUN rpm -Uvh jdk7-linux-x64.rpm
#RUN rm jdk7-linux-x64.rpm

# Install Gatling
RUN curl -L -v http://repository.excilys.com/content/repositories/releases/io/gatling/gatling-bundle/2.0.0-M3a/gatling-bundle-2.0.0-M3a-bundle.tar.gz -o gatling-bundle-2.0.0-M3a-bundle.tar.gz
RUN tar xvzf gatling-bundle-2.0.0-M3a-bundle.tar.gz
RUN mv gatling-bundle-2.0.0-M3a /opt/gatling

ENV PATH $PATH:/opt/gatling/bin
ENV JAVA_HOME /usr/java/default

CMD ["/bin/bash"]
