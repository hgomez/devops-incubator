# devops-incubator-centos6
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
