# di-centos6-myjenkins-lts
#
# Devops Incubator Jenkins LTS image based on CentOS 6
#
# VERSION               0.0.1

FROM     hgomez/di-centos6-base
MAINTAINER Henri Gomez "henri.gomez@gmail.com"

# Install Jenkins LTS
RUN yum install myjenkins-lts -y

# Jenkins HTTP port is 12355
EXPOSE 12355

ADD ./run.sh /usr/bin/run.sh
RUN chmod 755 /usr/bin/run.sh

#
# http://stackoverflow.com/questions/21553353/what-is-the-difference-between-cmd-and-entrypoint-in-a-dockerfile
#

#
# ENTRYPOINT mode
#
# docker run -i -t -p 12355:12355 hgomez/di-centos6-myjenkins-lts
#
#ENTRYPOINT ["/usr/bin/run.sh"]

#
# CMD mode
#
# docker run -p 12355:12355 hgomez/di-centos6-myjenkins-lts
#
#CMD ["/usr/bin/monitor-service.sh", "myjenkins"]
CMD ["/usr/bin/run.sh"]
