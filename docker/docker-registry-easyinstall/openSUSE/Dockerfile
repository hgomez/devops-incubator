 VERSION 0.1
# DOCKER-VERSION  0.9.1
# AUTHOR:         Henri Gomez <henri.gomez@gmail.com>
# DESCRIPTION:    Image with docker-registry-easyinstall project and dependencies
# TO_BUILD:       docker build --no-cache --rm -t registry-easyinstall  .
# TO_RUN:         docker run -p 5000:5000 registry-easyinstall
#

# openSUSE 13.2
FROM     opensuse:13.2
MAINTAINER Henri Gomez "henri.gomez@gmail.com"


# Update
RUN zypper clean \
   && zypper --gpg-auto-import-keys --non-interactive ref \
    && zypper --non-interactive update \
     && zypper install -y \
        gcc \
        swig \
        python-pip \
        python-setuptools \
        python-devel \
        libopenssl-devel \
        libyaml-devel \
        xz-devel \
        wget \
        tar

# easy_install way
RUN easy_install docker-registry==0.9.1

COPY ./config_sample.yml /

ENV DOCKER_REGISTRY_CONFIG /config_sample.yml
ENV SETTINGS_FLAVOR dev

EXPOSE 5000

CMD ["docker-registry"]

