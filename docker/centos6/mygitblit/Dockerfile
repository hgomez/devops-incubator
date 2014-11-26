# di-centos6-mygitblit
#
# Devops Incubator Gitblit image based on CentOS 6
#
# VERSION               0.0.1

FROM     hgomez/di-centos6-base
MAINTAINER Henri Gomez "henri.gomez@gmail.com"

# Install gitblit
RUN yum install mygitblit -y

# gitblit HTTP port is 12385
EXPOSE 12385  

ADD ./run.sh /usr/bin/run.sh
RUN chmod 755 /usr/bin/run.sh

#
# http://stackoverflow.com/questions/21553353/what-is-the-difference-between-cmd-and-entrypoint-in-a-dockerfile
#

#
# ENTRYPOINT mode
#
# docker run -i -t -p 12385:12385 hgomez/di-centos6-mygitblit
#
#ENTRYPOINT ["/usr/bin/run.sh"]

#
# CMD mode
#
# docker run -p 12385:12385 hgomez/di-centos6-mygitblit
#
#CMD ["/usr/bin/monitor-service.sh", "mygitblit"]
CMD ["/usr/bin/run.sh"]
