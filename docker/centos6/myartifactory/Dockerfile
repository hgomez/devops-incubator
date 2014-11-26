# di-centos6-myartifactory
#
# Devops Incubator Artifactory image based on CentOS 6
#
# VERSION               0.0.1

FROM     hgomez/di-centos6-base
MAINTAINER Henri Gomez "henri.gomez@gmail.com"

# Install artifactory
RUN yum install myartifactory -y

# Artifactory HTTP port is 12365
EXPOSE 12365

add ./run.sh /usr/bin/run.sh
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
#cmd ["/usr/bin/monitor-service.sh", "myartifactory"]
cmd ["/usr/bin/run.sh"]
