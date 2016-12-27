#devops-incubator - Native Packaging

![devops-incubator Logo](https://raw.github.com/hgomez/devops-incubator/master/images/devops-incubator-33pct.png)

Native Packaging sample for DevOps easy operations.
These packages will bring you a ready to use Software, QA and Ops Factories.

# Gitblit on CentOS 6

This image contains Gitblit running on CentOS 6 base image 

## Start Container 

### Attached to console (but no tty so cannot be stopped by Control-C)
    docker run -p 12385:12385 hgomez/di-centos6-mygitblit

### Detached
    docker run -d -p 12385:12385 hgomez/di-centos6-mygitblit

### Interactive mode
    docker run -t -i -p 12385:12385 hgomez/di-centos6-mygitblit

## Externalize Gitblit Home

Create local directory and ensure it's available to all
mygitblit will use user mygitblt (uid 1238) and need access to this repo

    mkdir -p /home/henri/gitblit-data
    chmod 777 /home/henri/gitblit-data

Mount the local directory, /home/henri/gitblit-data, into the container as the /var/lib/mygitblit directory

    docker run -v /home/henri/gitblit-data:/var/lib/mygitblit -p 12385:12385 hgomez/di-centos6-mygitblit
 
