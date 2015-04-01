 VERSION 0.1
# DOCKER-VERSION  0.9.1
# AUTHOR:         Henri Gomez <henri.gomez@gmail.com>
# DESCRIPTION:    Image with docker-registry-easyinstall project and dependencies
# TO_BUILD:       docker build --no-cache --rm -t registry-easyinstall  .
# TO_RUN:         docker run -p 5000:5000 registry-easyinstall

# Latest Ubuntu LTS
#
# {"host": ["Linux", "a17610144663", "3.13.0-37-generic", "#64-Ubuntu SMP Mon Sep 22 21:28:38 UTC 2014", "x86_64", "x86_64"], "launch": ["/usr/local/bin/gunicorn", "--access-logfile", "-", "--error-logfile", "-", "--max-requests", "100", "-k", "gevent", "--graceful-timeout", "3600", "-t", "3600", "-w", "4", "-b", "0.0.0.0:5000", "--reload", "docker_registry.wsgi:application"], "versions": {"M2Crypto.m2xmlrpclib": "0.22", "SocketServer": "0.4", "argparse": "1.1", "backports.lzma": "0.0.3", "blinker": "1.3", "cPickle": "1.71", "cgi": "2.6", "ctypes": "1.1.0", "decimal": "1.70", "distutils": "2.7.6", "docker_registry.app": "0.9.1", "docker_registry.core": "2.0.3", "docker_registry.server": "0.9.1", "email": "4.0.3", "flask": "0.10.1", "gevent": "1.0.1", "greenlet": "0.4.5", "gunicorn": "19.1.1", "gunicorn.arbiter": "19.1.1", "gunicorn.config": "19.1.1", "gunicorn.six": "1.2.0", "jinja2": "2.7.3", "json": "2.0.9", "logging": "0.5.1.2", "parser": "0.5", "pickle": "$Revision: 72223 $", "platform": "1.0.7", "pyexpat": "2.7.6", "python": "2.7.6 (default, Mar 22 2014, 22:59:56) \n[GCC 4.8.2]", "re": "2.2.1", "redis": "2.10.3", "requests": "2.3.0", "requests.packages.chardet": "2.2.1", "requests.packages.urllib3": "dev", "requests.packages.urllib3.packages.six": "1.2.0", "requests.utils": "2.3.0", "simplejson": "3.6.2", "sqlalchemy": "0.9.4", "tarfile": "$Revision: 85213 $", "urllib": "1.17", "urllib2": "2.7", "werkzeug": "0.10.4", "xml.parsers.expat": "$Revision: 17640 $", "xmlrpclib": "1.0.1", "yaml": "3.11", "zlib": "1.0"}}

# FROM ubuntu:14.04.2

# Latest Ubuntu 14.x (14.10)
# 
# {"host": ["Linux", "9b8a2094604a", "3.13.0-37-generic", "#64-Ubuntu SMP Mon Sep 22 21:28:38 UTC 2014", "x86_64", "x86_64"], "launch": ["/usr/local/bin/gunicorn", "--access-logfile", "-", "--error-logfile", "-", "--max-requests", "100", "-k", "gevent", "--graceful-timeout", "3600", "-t", "3600", "-w", "4", "-b", "0.0.0.0:5000", "--reload", "docker_registry.wsgi:application"], "versions": {"M2Crypto.m2xmlrpclib": "0.22", "SocketServer": "0.4", "argparse": "1.1", "backports.lzma": "0.0.3", "blinker": "1.3", "cPickle": "1.71", "cgi": "2.6", "chardet": "2.2.1", "ctypes": "1.1.0", "decimal": "1.70", "distutils": "2.7.8", "docker_registry.app": "0.9.1", "docker_registry.core": "2.0.3", "docker_registry.server": "0.9.1", "email": "4.0.3", "flask": "0.10.1", "gevent": "1.0.1", "greenlet": "0.4.5", "gunicorn": "19.1.1", "gunicorn.arbiter": "19.1.1", "gunicorn.config": "19.1.1", "gunicorn.six": "1.2.0", "jinja2": "2.7.3", "json": "2.0.9", "logging": "0.5.1.2", "parser": "0.5", "pickle": "$Revision: 72223 $", "platform": "1.0.7", "pyexpat": "2.7.8", "python": "2.7.8 (default, Oct 20 2014, 15:05:19) \n[GCC 4.9.1]", "re": "2.2.1", "redis": "2.10.3", "requests": "2.3.0", "requests.utils": "2.3.0", "simplejson": "3.6.2", "six": "1.7.3", "sqlalchemy": "0.9.4", "tarfile": "$Revision: 85213 $", "urllib": "1.17", "urllib2": "2.7", "urllib3": "1.8.3", "werkzeug": "0.10.4", "xml.parsers.expat": "$Revision: 17640 $", "xmlrpclib": "1.0.1", "yaml": "3.11", "zlib": "1.0"}}

# FROM ubuntu:14.10

# Latest Ubuntu 15.x (15.04)
# 

FROM ubuntu:15.04


# Update
RUN apt-get update \
# Install pip
    && apt-get install -y \
        swig \
        python-pip \
        python-setuptools \
# Install deps for backports.lmza (python2 requires it)
        python-dev \
        libssl-dev \
        liblzma-dev \
        libevent1-dev \
    && rm -rf /var/lib/apt/lists/*

# easy_install way
RUN easy_install docker-registry==0.9.1

COPY ./config_sample.yml /

ENV DOCKER_REGISTRY_CONFIG /config_sample.yml
ENV SETTINGS_FLAVOR dev

EXPOSE 5000

CMD ["docker-registry"]

