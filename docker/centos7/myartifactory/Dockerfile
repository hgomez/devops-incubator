# di-centos7-myartifactory
#
# Devops Incubator Artifactory image based on CentOS 7
#
# VERSION               0.0.1

FROM     hgomez/di-centos7-base
MAINTAINER Henri Gomez "henri.gomez@gmail.com"

# Install artifactory
RUN yum install myartifactory -y

# Artifactory HTTP port is 12365
EXPOSE 12365

ADD ./run.sh /usr/bin/run.sh
RUN chmod 755 /usr/bin/run.sh

#
# http://stackoverflow.com/questions/21553353/what-is-the-difference-between-cmd-and-entrypoint-in-a-dockerfile
#

#
# ENTRYPOINT mode
#
# docker run -i -t -p 12365:12365 hgomez/di-centos6-myartifactory
#
#ENTRYPOINT ["/usr/bin/run.sh"]

#
# CMD mode
#
# docker run -p 12365:12365 hgomez/di-centos6-myartifactory
#
#CMD ["/usr/bin/monitor-service.sh", "myartifactory"]
CMD ["/usr/bin/run.sh"]
