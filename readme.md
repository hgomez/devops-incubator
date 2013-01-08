#devops-incubator - Native Packaging

Native Packaging sample for DevOps easy operations.
These packages will bring you a ready to use Software Factory.

##RPM packages
[![Build Status](https://buildhive.cloudbees.com/job/danielpetisme/job/devops-incubator/badge/icon)](https://buildhive.cloudbees.com/job/danielpetisme/job/devops-incubator/)

* myarchiva - Apache Archiva powered by Apache Tomcat 7.x.
* myapp - simple web application powered by Apache Tomcat 7.x
* myartifactory - JFrog Artifactory powered by Apache Tomcat 7.x
* myforge-apache2-front - Apache HTTPd front-ends for Forge service via Named VHosts
* mygit - Git repositories hosted by Apache HTTPd and cgit
* mygitblit - GitBlig (Git Repositories manager) powered by Apache Tomcat 7.x
* myjenkins - Jenkins-CI powered by Apache Tomcat 7.x
* mynexus - Sonatype Nexus OSS powered by Apache Tomcat 7.x
* mysonar - Sonar powered by Apache Tomcat 7.x
* mysvn - Suversion hosted by Apache HTTPd

RPM packages version number follow application version number.
RPM packages release number are revision, used when something is updated in RPM like Apache Tomcat or in packaging.

##DEB packages

* mygitblit - GitBlig (Git Repositories manager) powered by Apache Tomcat 7.x
* myjenkins - Jenkins-CI powered by Apache Tomcat 7.x
* mynexus - Nexus OSS powered by Apache Tomcat 7.x

#Yum Repository

Thanks to JFrog Bintray and CloudBees BuildHive, RPM packages are now built in continuous and push to a Yum repository.
They could be installed on CentOS/Fedora/RHEL/Suse/openSUSE.

##CentOS/Fedora/RHEL

Add Yum repository by editing repo file **/etc/yum.repos.d/bintray-hgomez-devops-incubator-rpm.repo**

    #bintraybintray-hgomez-devops-incubator-rpm - packages by hgomez from Bintray
    [bintraybintray-hgomez-devops-incubator-rpm]
    name=bintray-hgomez-devops-incubator-rpm
    baseurl=http://dl.bintray.com/content/hgomez/devops-incubator-rpm
    gpgcheck=0
    enabled=1
 
Install a package (jenkins for example)

    sudo yum update
    sudo yum install myjenkins

##Suse/openSUSE

Add Zypper repository by editing repo file **/etc/zypp/repos.d/bintray-hgomez-devops-incubator-rpm.repo**

    #bintraybintray-hgomez-devops-incubator-rpm - packages by hgomez from Bintray
    [bintraybintray-hgomez-devops-incubator-rpm]
    name=bintray-hgomez-devops-incubator-rpm
    baseurl=http://dl.bintray.com/content/hgomez/devops-incubator-rpm
    type=rpm-md
    gpgcheck=0


Install a package (jenkins for example)

    sudo zypper ref 
    sudo zypper update
    sudo zypper install myjenkins

