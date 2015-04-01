 VERSION 0.1
# DOCKER-VERSION  0.9.1
# AUTHOR:         Henri Gomez <henri.gomez@gmail.com>
# DESCRIPTION:    Image with docker-registry-easyinstall project and dependencies
# TO_BUILD:       docker build --no-cache --rm -t registry-easyinstall  .
# TO_RUN:         docker run -p 5000:5000 registry-easyinstall
#

# Latest CentOS 7 
FROM     centos:centos7
MAINTAINER Henri Gomez "henri.gomez@gmail.com"


# Update
RUN yum clean all \
   && yum update -y \
     && yum install -y \
        gcc \
        swig \
        python-pip \
        python-setuptools \
        python-devel \
        openssl-devel \
        xz-devel \
        wget \
        tar

# easy_install way
#RUN easy_install M2crypto==0.22.3
# I love this way to compile M2Crypto
RUN wget https://pypi.python.org/packages/source/M/M2Crypto/M2Crypto-0.22.3.tar.gz \
   && tar xvzf M2Crypto-0.22.3.tar.gz \
    && cd M2Crypto-0.22.3 \
      && export SWIG_FEATURES="-cpperraswarn -includeall -D__`uname -m`__ -I/usr/include/openssl" \
       && python setup.py install
RUN easy_install docker-registry==0.9.1

COPY ./config_sample.yml /

ENV DOCKER_REGISTRY_CONFIG /config_sample.yml
ENV SETTINGS_FLAVOR dev

EXPOSE 5000

CMD ["docker-registry"]

