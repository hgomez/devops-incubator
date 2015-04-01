 VERSION 0.1
# DOCKER-VERSION  0.9.1
# AUTHOR:         Henri Gomez <henri.gomez@gmail.com>
# DESCRIPTION:    Image with docker-registry-easyinstall project and dependencies
# TO_BUILD:       docker build --no-cache --rm -t registry-easyinstall  .
# TO_RUN:         docker run -p 5000:5000 registry-easyinstall
#

# Latest Ubuntu LTS
# FROM ubuntu:14.04.2

# Latest Ubuntu 14.x (14.10)
# FROM ubuntu:14.10

# Latest Ubuntu 15.x (15.04)
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

