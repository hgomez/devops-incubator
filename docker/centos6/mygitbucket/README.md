#devops-incubator - Native Packaging

![devops-incubator Logo](https://raw.github.com/hgomez/devops-incubator/master/images/devops-incubator-33pct.png)

Native Packaging sample for DevOps easy operations.
These packages will bring you a ready to use Software, QA and Ops Factories.

# Gitbucket on CentOS 6

This image contains Gitbucket running on CentOS 6 base image 

## Start Container 

### Attached to console (but no tty so cannot be stopped by Control-C)
    docker run -p 12545:12545 hgomez/di-centos6-mygitbucket

### Detached
    docker run -d -p 12545:12545 hgomez/di-centos6-mygitbucket

### Interactive mode
    docker run -t -i -p 12545:12545 hgomez/di-centos6-mygitbucket

## Externalize Gitbucket Home

Create local directory and ensure it's available to all
mygitbucket will use user mygitbuc (uid 1246) and need access to this repo

    mkdir -p /home/henri/gitbucket-data
    chmod 777 /home/henri/gitbucket-data

Mount the local directory, /home/henri/gitbucket-data, into the container as the /var/lib/mygitbucket directory

    docker run -v /home/henri/gitbucket-data:/var/lib/mygitbucket -p 12545:12545 hgomez/di-centos6-mygitbucket
 
