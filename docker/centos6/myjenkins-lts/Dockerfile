# di-centos6-myjenkins-lts
#
# Devops Incubator image based on CentOS 6
#
# VERSION               0.0.1

FROM     hgomez/di-centos6-base
MAINTAINER Henri Gomez "henri.gomez@gmail.com"

# Install Jenkins LTS
RUN yum install myjenkins-lts -y

# Install supervisord config
add ./supervisord.conf /etc/supervisord.conf

# Jenkins HTTP port is 12355
EXPOSE 12355

# Start supervisor
cmd ["supervisord", "-n"]

