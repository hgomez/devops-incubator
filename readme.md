#devops-incubator - Native Packaging

Native Packaging sample for DevOps easy operations.
These packages will bring you a ready to use Software Factory.

##RPM packages

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

Note these RPM packages are OpenSuse/SLES 11.4-12.1 ready.

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

###Install Yum repository

    wget https://www.bintray.com/repo/rpm/hgomez/devops-incubator-rpm -O bintray-hgomez-devops-incubator-rpm.repo
    sudo mv bintray-hgomez-devops-incubator-rpm.repo /etc/etc/yum.repos.d/
    sudo yum update

###Install a package (jenkins for example)

    sudo yum install myjenkins

##Suse/openSUSE

###Install Yum repository

    wget https://www.bintray.com/repo/rpm/hgomez/devops-incubator-rpm -O bintray-hgomez-devops-incubator-rpm.repo
    sudo mv bintray-hgomez-devops-incubator-rpm.repo /etc/zypp/repos.d/
    sudo zypper update

### Install a package (jenkins for example)

    sudo zypper install myjenkins

