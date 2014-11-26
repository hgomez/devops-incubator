#devops-incubator - Native Packaging

![devops-incubator Logo](https://raw.github.com/hgomez/devops-incubator/master/images/devops-incubator-33pct.png)

Native Packaging sample for DevOps easy operations.
These packages will bring you a ready to use Software, QA and Ops Factories.

# Nexus on CentOS 6

This image contains Nexus running on CentOS 6 base image 

## Start Container 

### Attached to console (but no tty so cannot be stopped by Control-C)
    docker run  -p 12365:12365 hgomez/di-centos6-mynexus

### Detached
    docker run -d -p 12365:12365 hgomez/di-centos6-mynexus

### Interactive mode
    docker run -t -i -v -p 12365:12365 hgomez/di-centos6-mynexus

## Externalize Artifactory Home

Create local directory and ensure it's available to all
mynexus will use user mynexus (uid 1236) and need access to this repo

    mkdir -p /home/henri/nexus-data
    chmod 777 /home/henri/nexus-data

Mount the local directory, /home/henri/nexus-data, into the container as the /var/lib/mynexus directory

    docker run -v /home/henri/nexus-data:/var/lib/mynexus -p 12365:12365 hgomez/di-centos6-mynexus
 
