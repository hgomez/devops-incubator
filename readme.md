#devops-incubator - Native Packaging

![devops-incubator Logo](https://raw.github.com/hgomez/devops-incubator/master/images/devops-incubator-33pct.png)

Native Packaging sample for DevOps easy operations.
These packages will bring you a ready to use Software Factory.

##RPM packages
[![Build Status](https://buildhive.cloudbees.com/job/hgomez/job/devops-incubator/badge/icon)](https://buildhive.cloudbees.com/job/hgomez/job/devops-incubator/)

* myarchiva - Apache Archiva powered by Apache Tomcat 7.x.
* myapp - simple web application powered by Apache Tomcat 7.x
* myartifactory - JFrog Artifactory powered by Apache Tomcat 7.x
* mycarbon - Graphite suite data collector
* myforge-apache2-front - Apache HTTPd front-ends for Forge service via Named VHosts
* mygraphite-web - Graphite suite web adaptor
* mygraphite-suite - Graphite suite (designed for openSUSE 12.x and SUSE SLES 11+)
* mygit - Git repositories hosted by Apache HTTPd and cgit
* mygitblit - GitBlig (Git Repositories manager) powered by Apache Tomcat 7.x
* myjenkins - Jenkins-CI powered by Apache Tomcat 7.x
* mynexus - Sonatype Nexus OSS powered by Apache Tomcat 7.x
* mysonar - Sonar powered by Apache Tomcat 7.x
* mysvn - Suversion hosted by Apache HTTPd
* mywhisper - Graphite suite data storage backend

RPM packages version number follow application version number.
RPM packages release number are revision, used when something is updated in RPM like Apache Tomcat or in packaging.

##DEB packages

* mygitblit - GitBlig (Git Repositories manager) powered by Apache Tomcat 7.x
* myjenkins - Jenkins-CI powered by Apache Tomcat 7.x
* mynexus - Nexus OSS powered by Apache Tomcat 7.x

#Yum Repository

Thanks to JFrog Bintray and CloudBees BuildHive, RPM packages are now built in continuous and push to a Yum repository.
They could be installed on CentOS/Fedora/RHEL/Suse/openSUSE.

##CentOS/RHEL 5

Add Yum repository by editing repo file **/etc/yum.repos.d/bintray-devops-incubator-noarch.repo**

    #devops-incubator-noarch.repo - packages by hgomez from Bintray
    [bintray-devops-incubator-noarch]
    name=bintray-devops-incubator-noarch
    baseurl=http://dl.bintray.com/content/hgomez/devops-incubator-rpm-centos5-noarch
    gpgcheck=0
    enabled=1
 
Install a package (jenkins for example)

    sudo yum update
    sudo yum install myjenkins

##CentOS/RHEL 6

Add Yum repository by editing repo file **/etc/yum.repos.d/bintray-devops-incubator-noarch.repo**

    #devops-incubator-noarch.repo - packages by hgomez from Bintray
    [bintray-devops-incubator-noarch]
    name=bintray-devops-incubator-noarch
    baseurl=http://dl.bintray.com/content/hgomez/devops-incubator-rpm-centos6-noarch
    gpgcheck=0
    enabled=1
 
Install a package (jenkins for example)

    sudo yum update
    sudo yum install myjenkins

##Fedora 18

Add Yum repository by editing repo file **/etc/yum.repos.d/bintray-devops-incubator-noarch.repo**

    #devops-incubator-noarch.repo - packages by hgomez from Bintray
    [bintray-devops-incubator-noarch]
    name=bintray-devops-incubator-noarch
    baseurl=http://dl.bintray.com/content/hgomez/devops-incubator-rpm-fedora18-noarch
    gpgcheck=0
    enabled=1
 
Install a package (jenkins for example)

    sudo yum update
    sudo yum install myjenkins

##openSUSE 12.1/12.2/12.3

Add Zypper repository by editing repo file **/etc/zypp/repos.d/bintray-devops-incubator-noarch.repo**

    #devops-incubator-noarch.repo - packages by hgomez from Bintray
    [bintray-devops-incubator-noarch]
    name=bintray-devops-incubator-noarch
    baseurl=http://dl.bintray.com/content/hgomez/devops-incubator-rpm-opensuse122-noarch
    type=rpm-md
    gpgcheck=0

For native code (like mycarbon), you should also add architecture dependant repo ;

    #devops-incubator-x86-64.repo - packages by hgomez from Bintray
    [bintray-devops-incubator-x86-64]
    name=bintray-devops-incubator-x86-64
    baseurl=http://dl.bintray.com/content/hgomez/devops-incubator-rpm-opensuse122-x86-64
    type=rpm-md
    gpgcheck=0


Install a package (jenkins for example)

    sudo zypper ref 
    sudo zypper update
    sudo zypper install myjenkins

