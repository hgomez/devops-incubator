# di-centos6-mygitbucket
#
# Devops Incubator gitbucket image based on CentOS 6
#
# VERSION               0.0.1

FROM     hgomez/di-centos6-base
MAINTAINER Henri Gomez "henri.gomez@gmail.com"

# Install gitbucket
RUN yum install mygitbucket -y

# gitbucket HTTP port is 12545
EXPOSE 12545  

ADD ./run.sh /usr/bin/run.sh
RUN chmod 755 /usr/bin/run.sh

#
# http://stackoverflow.com/questions/21553353/what-is-the-difference-between-cmd-and-entrypoint-in-a-dockerfile
#

#
# ENTRYPOINT mode
#
# docker run -i -t -p 12545:12545 hgomez/di-centos6-mygitbucket
#
#ENTRYPOINT ["/usr/bin/run.sh"]

#
# CMD mode
#
# docker run -p 12545:12545 hgomez/di-centos6-mygitbucket
#
#CMD ["/usr/bin/monitor-service.sh", "mygitbucket"]
CMD ["/usr/bin/run.sh"]
