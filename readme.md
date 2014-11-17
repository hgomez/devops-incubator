#devops-incubator - Native Packaging

![devops-incubator Logo](https://raw.github.com/hgomez/devops-incubator/master/images/devops-incubator-33pct.png)

Native Packaging sample for DevOps easy operations.
These packages will bring you a ready to use Software, QA and Ops Factories.

##RPM packages
[![Is maintained?](http://stillmaintained.com/hgomez/devops-incubator.png)](http://stillmaintained.com/hgomez/devops-incubator)

###Packages for Software Factories

* golo-lang - A lightweight dynamic language for the JVM, [Golo](http://golo-lang.org/)
* myarchiva - Apache [Archiva](http://archiva.apache.org/) powered by Apache Tomcat 7.x.
* myartifactory - JFrog [Artifactory](http://www.jfrog.org/) powered by Apache Tomcat 7.x
* myforge-apache2-front - Apache HTTPd front-ends for Forge service via Named VHosts
* mygit - Git repositories hosted by Apache HTTPd and cgit
* mygitblit - [GitBlit](http://gitblit.com/) powered by Apache Tomcat 7.x
* myjenkins - [Jenkins-CI](http://jenkins-ci.org/) powered by Apache Tomcat 7.x
* mynexus - Sonatype [Nexus OSS](http://www.sonatype.org/nexus/) powered by Apache Tomcat 7.x
* mysonar - SonarQube [Sonar](http://www.sonarqube.org/)  powered by Apache Tomcat 7.x
* mysvn - Apache [Subversion](http://subversion.apache.org/) hosted by Apache HTTPd

###Packages for QA Factories

* jstatd-daemon - [JStatd](http://docs.oracle.com/javase/7/docs/technotes/tools/share/jstatd.html) 
* myapp - [Simple web application](https://github.com/hgomez/devops-incubator/tree/master/basic-perf-webapp) powered by Apache Tomcat 7.x
* mycarbon - [Graphite suite](http://graphite.wikidot.com/) data collector
* mygraphite-web - [Graphite suite](http://graphite.wikidot.com/) web adaptor
* mygraphite-suite - [Graphite suite](http://graphite.wikidot.com/) (designed for openSUSE 12.x and SUSE SLES 11+)
* mywhisper - [Graphite](http://graphite.wikidot.com/) data storage backend

###Packages for Ops Factories
* crash - The shell for the Java Platform, [Crash](http://www.crashub.org/) 
* tomee-jaxrx - Apache [TomEE](http://tomee.apache.org/) with JAXRS
* tomee-plus - Apache [TomEE](http://tomee.apache.org/) with Plus
* tomee-webprofile - Apache [TomEE](http://tomee.apache.org/) with WebProfile
 
RPM packages version number follow application version number.
RPM packages release number are revision, used when something is updated in RPM like Apache Tomcat or in packaging.

#Yum Repository

Thanks to [openSUSE Build Service](https://build.opensuse.org), RPM packages are now [built and pushed](https://build.opensuse.org/project/show/home:henri_gomez:devops-incubator) to Yum repositories on OBS.
They could be installed on CentOS/Fedora/RHEL/Suse SLES/openSUSE.

##CentOS

###CentOS 5

Add Yum repository by editing repo file **/etc/yum.repos.d/devops-incubator.repo**

    [home_henri_gomez_devops-incubator]
    name=Devops Incubator Packages   (CentOS_CentOS-5)
    type=rpm-md
    baseurl=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/CentOS_CentOS-5/
    gpgcheck=1
    gpgkey=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/CentOS_CentOS-5/repodata/repomd.xml.key
    enabled=1
 
###CentOS 6

Add Yum repository by editing repo file **/etc/yum.repos.d/devops-incubator.repo**

    [home_henri_gomez_devops-incubator]
    name=Devops Incubator Packages   (CentOS_CentOS-6)
    type=rpm-md
    baseurl=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/CentOS_CentOS-6/
    gpgcheck=1
    gpgkey=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/CentOS_CentOS-6/repodata/repomd.xml.key
    enabled=1
 
Install a package (jenkins for example)

    sudo yum update
    sudo yum install myjenkins

##Fedora

###Fedora 18

Add Yum repository by editing repo file **/etc/yum.repos.d/devops-incubator.repo**

    [home_henri_gomez_devops-incubator]
    name=Devops Incubator Packages   (Fedora_18)
    type=rpm-md
    baseurl=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/Fedora_18/
    gpgcheck=1
    gpgkey=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/Fedora_18/repodata/repomd.xml.key
    enabled=1
 
###Fedora 19

Add Yum repository by editing repo file **/etc/yum.repos.d/devops-incubator.repo**

    [home_henri_gomez_devops-incubator]
    name=Devops Incubator Packages   (Fedora_19)
    type=rpm-md
    baseurl=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/Fedora_19/
    gpgcheck=1
    gpgkey=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/Fedora_19/repodata/repomd.xml.key
    enabled=1
 
###Fedora 20

Add Yum repository by editing repo file **/etc/yum.repos.d/devops-incubator.repo**

    [home_henri_gomez_devops-incubator]
    name=Devops Incubator Packages   (Fedora_20)
    type=rpm-md
    baseurl=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/Fedora_20/
    gpgcheck=1
    gpgkey=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/Fedora_19/repodata/repomd.xml.key
    enabled=1
 
Install a package (crash for example)

    sudo yum update
    sudo yum install crash

##RHEL

###RHEL 5

Add Yum repository by editing repo file **/etc/yum.repos.d/devops-incubator.repo**

    [home_henri_gomez_devops-incubator]
    name=Devops Incubator Packages   (RedHat_RHEL-5)
    type=rpm-md
    baseurl=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/RedHat_RHEL-5/
    gpgcheck=1
    gpgkey=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/RedHat_RHEL-5/repodata/repomd.xml.key
    enabled=1
 
###RHEL 6

Add Yum repository by editing repo file **/etc/yum.repos.d/devops-incubator.repo**

    [home_henri_gomez_devops-incubator]
    name=Devops Incubator Packages   (RedHat_RHEL-6)
    type=rpm-md
    baseurl=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/RedHat_RHEL-6/
    gpgcheck=1
    gpgkey=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/RedHat_RHEL-6/repodata/repomd.xml.key
    enabled=1
 
Install a package (jenkins for example)

    sudo yum update
    sudo yum install myjenkins



##openSUSE

###openSUSE 12.2

Add Zypper repository by editing repo file **/etc/zypp/repos.d/devops-incubator.repo**

    [home_henri_gomez_devops-incubator]
    name=Devops Incubator Packages   (openSUSE_12.2)
    type=rpm-md
    baseurl=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/openSUSE_12.2/
    gpgcheck=1
    gpgkey=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/openSUSE_12.2/repodata/repomd.xml.key
    enabled=1

###openSUSE 12.3

Add Zypper repository by editing repo file **/etc/zypp/repos.d/devops-incubator.repo**

    [home_henri_gomez_devops-incubator]
    name=Devops Incubator Packages   (openSUSE_12.3)
    type=rpm-md
    baseurl=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/openSUSE_12.3/
    gpgcheck=1
    gpgkey=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/openSUSE_12.3/repodata/repomd.xml.key
    enabled=1

###openSUSE 13.1

Add Zypper repository by editing repo file **/etc/zypp/repos.d/devops-incubator.repo**

    [home_henri_gomez_devops-incubator]
    name=Devops Incubator Packages   (openSUSE_13.1)
    type=rpm-md
    baseurl=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/openSUSE_13.1/
    gpgcheck=1
    gpgkey=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/openSUSE_13.1/repodata/repomd.xml.key
    enabled=1

###openSUSE 13.2

Add Zypper repository by editing repo file **/etc/zypp/repos.d/devops-incubator.repo**

    [home_henri_gomez_devops-incubator]
    name=Devops Incubator Packages   (openSUSE_13.2)
    type=rpm-md
    baseurl=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/openSUSE_13.2/
    gpgcheck=1
    gpgkey=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/openSUSE_13.2/repodata/repomd.xml.key
    enabled=1

Install a package (jenkins for example)

    sudo zypper ref 
    sudo zypper update
    sudo zypper install myjenkins


##SUSE Enterprise

###SLES 10

Add Zypper repository by editing repo file **/etc/zypp/repos.d/devops-incubator.repo**

    [home_henri_gomez_devops-incubator]
    name=Devops Incubator Packages   (SLE_10_SDK)
    type=rpm-md
    baseurl=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/SLE_10_SDK/
    gpgcheck=1
    gpgkey=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/SLE_10_SDK/repodata/repomd.xml.key
    enabled=1

###SLES 11

Add Zypper repository by editing repo file **/etc/zypp/repos.d/devops-incubator.repo**

    [home_henri_gomez_devops-incubator]
    name=Devops Incubator Packages   (SLE_11)
    type=rpm-md
    baseurl=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/SLE_11/
    gpgcheck=1
    gpgkey=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/SLE_11/repodata/repomd.xml.key
    enabled=1

###SLES 11 SP1

Add Zypper repository by editing repo file **/etc/zypp/repos.d/devops-incubator.repo**

    [home_henri_gomez_devops-incubator]
    name=Devops Incubator Packages   (SLE_11_SP1)
    type=rpm-md
    baseurl=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/SLE_11_SP1/
    gpgcheck=1
    gpgkey=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/SLE_11_SP1/repodata/repomd.xml.key
    enabled=1

###SLES 11 SP2

Add Zypper repository by editing repo file **/etc/zypp/repos.d/devops-incubator.repo**

    [home_henri_gomez_devops-incubator]
    name=Devops Incubator Packages   (SLE_11_SP2)
    type=rpm-md
    baseurl=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/SLE_11_SP2/
    gpgcheck=1
    gpgkey=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/SLE_11_SP2/repodata/repomd.xml.key
    enabled=1

###SLES 11 SP3

Add Zypper repository by editing repo file **/etc/zypp/repos.d/devops-incubator.repo**

    [home_henri_gomez_devops-incubator]
    name=Devops Incubator Packages   (SLE_11_SP3)
    type=rpm-md
    baseurl=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/SLE_11_SP3/
    gpgcheck=1
    gpgkey=http://download.opensuse.org/repositories/home:/henri_gomez:/devops-incubator/SLE_11_SP3/repodata/repomd.xml.key
    enabled=1


Install a package (jenkins for example)

    sudo zypper ref 
    sudo zypper update
    sudo zypper install myjenkins


