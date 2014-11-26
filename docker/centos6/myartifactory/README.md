#devops-incubator - Native Packaging

![devops-incubator Logo](https://raw.github.com/hgomez/devops-incubator/master/images/devops-incubator-33pct.png)

Native Packaging sample for DevOps easy operations.
These packages will bring you a ready to use Software, QA and Ops Factories.

# Artifactory on CentOS 6

This image contains Artifactory running on CentOS 6 base image 

## Start Container 

### Attached to console (but no tty so cannot be stopped by Control-C)
    docker run  -p 12365:12365 hgomez/di-centos6-myartifactory

### Detached
    docker run -d -p 12365:12365 hgomez/di-centos6-myartifactory

### Interactive mode
    docker run -t -i -v -p 12365:12365 hgomez/di-centos6-myartifactory

## Externalize Artifactory Home

Create local directory and ensure it's available to all
myartifactory will use user myartifactory (uid 1250) and need access to this repo

    mkdir -p /home/henri/artifactory-data
    chmod 777 /home/henri/artifactory-data

Mount the local directory, /home/henri/artifactory-data, into the container as the /var/lib/myartifactory directory

    docker run -v /home/henri/artifactory-data:/var/lib/myartifactory -p 12365:12365 hgomez/di-centos6-myartifactory
 
