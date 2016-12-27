#devops-incubator - Native Packaging

![devops-incubator Logo](https://raw.github.com/hgomez/devops-incubator/master/images/devops-incubator-33pct.png)

Native Packaging sample for DevOps easy operations.
These packages will bring you a ready to use Software, QA and Ops Factories.

# Jenkins on CentOS 6

This image contains Jenkins running on CentOS 6 base image 

## Start Container 

### Attached to console (but no tty so cannot be stopped by Control-C)
    docker run -p 12355:12355 hgomez/di-centos6-myjenkins

### Detached
    docker run -d -p 12355:12355 hgomez/di-centos6-myjenkins

### Interactive mode
    docker run -t -i -p 12355:12355 hgomez/di-centos6-myjenkins

## Externalize Jenkins Home

Create local directory and ensure it's available to all
myjenkins will use user myjenkins (uid 1235) and need access to this repo

    mkdir -p /home/henri/jenkins-data
    chmod 777 /home/henri/jenkins-data

Mount the local directory, /home/henri/jenkins-data, into the container as the /var/lib/myjenkins directory

    docker run -v /home/henri/jenkins-data:/var/lib/myjenkins -p 12355:12355 hgomez/di-centos6-myjenkins
 
