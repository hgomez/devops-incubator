# di-centos7-myarchiva
#
# Devops Incubator Archiva image based on CentOS 7
#
# VERSION               0.0.1

FROM     hgomez/di-centos7-base
MAINTAINER Henri Gomez "henri.gomez@gmail.com"

# Install Archiva
RUN yum install myarchiva -y

# Archiva HTTP port is 12365
EXPOSE 12365

ADD ./run.sh /usr/bin/run.sh
RUN chmod 755 /usr/bin/run.sh

#
# http://stackoverflow.com/questions/21553353/what-is-the-difference-between-cmd-and-entrypoint-in-a-dockerfile
#

#
# ENTRYPOINT mode
#
# docker run -i -t -p 12365:12365 hgomez/di-centos6-myarchiva
#
#ENTRYPOINT ["/usr/bin/run.sh"]

#
# CMD mode
#
# docker run -p 12365:12365 hgomez/di-centos6-myarchiva
#
#CMD ["/usr/bin/monitor-service.sh", "myarchiva"]
CMD ["/usr/bin/run.sh"]
