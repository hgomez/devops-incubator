#devops-incubator - Native Packaging

![devops-incubator Logo](https://raw.github.com/hgomez/devops-incubator/master/images/devops-incubator-33pct.png)

Native Packaging sample for DevOps easy operations.
These packages will bring you a ready to use Software, QA and Ops Factories.

# Archiva on CentOS 6

This image contains Archiva running on CentOS 6 base image 

## Start Container 

### Attached to console (but no tty so cannot be stopped by Control-C)
    docker run  -p 12365:12365 hgomez/di-centos6-myarchiva

### Detached
    docker run -d -p 12365:12365 hgomez/di-centos6-myarchiva

### Interactive mode
    docker run -t -i -v -p 12365:12365 hgomez/di-centos6-myarchiva

## Externalize Archiva Home

Create local directory and ensure it's available to all
myarchiva will use user myarchiv (uid 1250) and need access to this repo

    mkdir -p /home/henri/archiva-data
    chmod 777 /home/henri/archiva-data

Mount the local directory, /home/henri/archiva-data, into the container as the /var/lib/myarchiva directory

    docker run -v /home/henri/archiva-data:/var/lib/myarchiva -p 12365:12365 hgomez/di-centos6-myarchiva
 
