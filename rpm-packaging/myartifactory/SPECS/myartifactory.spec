# Avoid unnecessary debug-information (native code)
%define		debug_package %{nil}

# Avoid jar repack (brp-java-repack-jars)
#%define __jar_repack 0

# Avoid CentOS 5/6 extras processes on contents (especially brp-java-repack-jars)
%define __os_install_post %{nil}

%ifos darwin
%define __portsed sed -i "" -e
%else
%define __portsed sed -i
%endif

%if 0%{?TOMCAT_REL:1}
%define tomcat_rel        %{TOMCAT_REL}
%else
%define tomcat_rel        7.0.55
%endif

%if 0%{?ARTIFACTORY_REL:1}
%define artifactory_rel    %{ARTIFACTORY_REL}
%else
%define artifactory_rel    3.3.0
%endif

Name: myartifactory
Version: %{artifactory_rel}
Release: 2
Summary: JFrog Artifactory %{artifactory_rel} powered by Apache Tomcat %{tomcat_rel}
Group: Development/Tools/Building
URL: http://www.jfrog.com/
Vendor: devops-incubator
License: GPL-3.0
BuildArch:  noarch

%define appname         myartifactory
%define appusername     myarti
%define appuserid       1239
%define appgroupid      1239

%define appdir          /opt/%{appname}
%define appdatadir      %{_var}/lib/%{appname}
%define applogdir       %{_var}/log/%{appname}
%define appexec         %{appdir}/bin/catalina.sh
%define appconfdir      %{appdir}/conf
%define appconflocaldir %{appdir}/conf/Catalina/localhost
%define appwebappdir    %{appdir}/webapps
%define apptempdir      %{_var}/run/%{appname}
%define appworkdir      %{_var}/spool/%{appname}
%define appcron         %{appdir}/bin/cron.sh

%define _cronddir       %{_sysconfdir}/cron.d
%define _initrddir      %{_sysconfdir}/init.d
%define _systemddir     /lib/systemd
%define _systemdir      %{_systemddir}/system

%if 0%{?fedora} || 0%{?rhel} || 0%{?centos} || 0%{?suse_version} < 1200
%define servicestart %{_initrddir}/%{appname} start
%define servicestop  %{_initrddir}/%{appname} stop
%define serviceon    chkconfig %{appname} on
%define serviceoff   chkconfig %{appname} off
%else
%define servicestart service %{appname} start
%define servicestop  service %{appname} stop
%define serviceon    systemctl enable %{appname}
%define serviceoff   systemctl disable %{appname} 
%endif

BuildRoot: %{_tmppath}/build-%{name}-%{version}-%{release}

%if 0%{?suse_version} > 1140
BuildRequires: systemd
%{?systemd_requires}
%else
%define systemd_requires %{nil}
%endif

%if 0%{?suse_version} > 1000
PreReq: %fillup_prereq
%endif

BuildRequires: unzip

%if 0%{?suse_version}
Requires: cron
Requires: logrotate
%endif

%if 0%{?suse_version}
Requires:           java >= 1.7.0
%endif

%if 0%{?fedora} || 0%{?rhel} || 0%{?centos}
Requires:           java >= 1:1.7.0
%endif

Requires(pre):      %{_sbindir}/groupadd
Requires(pre):      %{_sbindir}/useradd

Source0: http://www.eu.apache.org/dist/tomcat/tomcat-7/v%{tomcat_rel}/bin/apache-tomcat-%{tomcat_rel}.tar.gz
Source1: http://dl.bintray.com/jfrog/artifactory/artifactory-%{artifactory_rel}.zip
Source2: initd.skel
Source3: sysconfig.skel
Source4: jmxremote.access.skel
Source5: jmxremote.password.skel
Source6: setenv.sh.skel
Source7: logrotate.skel
Source8: server.xml.skel
Source9: limits.conf.skel
Source10: systemd.skel
Source11: catalina-jmx-remote-%{tomcat_rel}.jar
Source12: logging.properties.skel
Source13: crond.skel
Source14: cron.sh.skel

%description
Artifactory offers powerful enterprise features and fine-grained permission control behind a sleek and easy-to-use UI.
Artifactory acts as a proxy between your build tool (Maven, Ant, Ivy, Gradle etc.) and the outside world.
This package contains JFrog Artifactory %{artifactory_rel} powered by Apache Tomcat %{tomcat_rel}

%prep
%setup -q -c

%build

%install
# Prep the install location.
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_cronddir}
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}%{_sysconfdir}/security/limits.d
%if 0%{?suse_version} > 1140
mkdir -p %{buildroot}%{_systemdir}
%endif

mkdir -p %{buildroot}%{appdir}
mkdir -p %{buildroot}%{appdatadir}
mkdir -p %{buildroot}%{applogdir}
mkdir -p %{buildroot}%{apptempdir}
mkdir -p %{buildroot}%{appworkdir}

# Copy tomcat
mv apache-tomcat-%{tomcat_rel}/* %{buildroot}%{appdir}

# Create conf/Catalina/localhost
mkdir -p %{buildroot}%{appconflocaldir}

# remove default webapps
rm -rf %{buildroot}%{appdir}/webapps/*

# patches to have logs under /var/log/app
# remove manager and host-manager logs (via .skel file)
cp %{SOURCE12} %{buildroot}%{appdir}/conf/logging.properties
%{__portsed} 's|\${catalina.base}/logs|%{applogdir}|g' %{buildroot}%{appdir}/conf/logging.properties

# artifactory webapp is ROOT.war (will respond to /), get it from zip file
unzip %{SOURCE1}
mv artifactory-%{artifactory_rel}/webapps/artifactory.war %{buildroot}%{appwebappdir}/ROOT.war
# artifactory config dir/subdirs
mv artifactory-%{artifactory_rel}/etc %{buildroot}%{appdatadir}
# artifactory misc files
mv artifactory-%{artifactory_rel}/misc %{buildroot}%{appdir}

# cleanup
rm -rf artifactory-%{artifactory_rel}

# setup derby-storage
%{__portsed} 's|#artifactory.jcr.configDir=null|artifactory.jcr.configDir=repo/filesystem-derby|g' %{buildroot}%{appdatadir}/etc/artifactory.system.properties

# init.d
cp  %{SOURCE2} %{buildroot}%{_initrddir}/%{appname}
%{__portsed} 's|@@MYAPP_APP@@|%{appname}|g' %{buildroot}%{_initrddir}/%{appname}
%{__portsed} 's|@@MYAPP_USER@@|%{appusername}|g' %{buildroot}%{_initrddir}/%{appname}
%{__portsed} 's|@@MYAPP_VERSION@@|version %{version} release %{release}|g' %{buildroot}%{_initrddir}/%{appname}
%{__portsed} 's|@@MYAPP_EXEC@@|%{appexec}|g' %{buildroot}%{_initrddir}/%{appname}
%{__portsed} 's|@@MYAPP_DATADIR@@|%{appdatadir}|g' %{buildroot}%{_initrddir}/%{appname}
%{__portsed} 's|@@MYAPP_LOGDIR@@|%{applogdir}|g' %{buildroot}%{_initrddir}/%{appname}
%{__portsed} 's|@@MYAPP_TMPDIR@@|%{apptempdir}|g' %{buildroot}%{_initrddir}/%{appname}

# sysconfig
cp  %{SOURCE3}  %{buildroot}%{_sysconfdir}/sysconfig/%{appname}
%{__portsed} 's|@@MYAPP_APP@@|%{appname}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{appname}
%{__portsed} 's|@@MYAPP_APPDIR@@|%{appdir}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{appname}
%{__portsed} 's|@@MYAPP_DATADIR@@|%{appdatadir}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{appname}
%{__portsed} 's|@@MYAPP_LOGDIR@@|%{applogdir}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{appname}
%{__portsed} 's|@@MYAPP_USER@@|%{appusername}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{appname}
%{__portsed} 's|@@MYAPP_CONFDIR@@|%{appconfdir}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{appname}

%if 0%{?suse_version} > 1000
mkdir -p %{buildroot}%{_var}/adm/fillup-templates
mv %{buildroot}%{_sysconfdir}/sysconfig/%{appname} %{buildroot}%{_var}/adm/fillup-templates/sysconfig.%{appname}
%endif

# JMX (including JMX Remote)
cp %{SOURCE11} %{buildroot}%{appdir}/lib
cp %{SOURCE4}  %{buildroot}%{appconfdir}/jmxremote.access.skel
cp %{SOURCE5}  %{buildroot}%{appconfdir}/jmxremote.password.skel

# Our custom setenv.sh to get back env variables
cp  %{SOURCE6} %{buildroot}%{appdir}/bin/setenv.sh
%{__portsed} 's|@@MYAPP_APP@@|%{appname}|g' %{buildroot}%{appdir}/bin/setenv.sh

# Install logrotate
cp %{SOURCE7} %{buildroot}%{_sysconfdir}/logrotate.d/%{appname}
%{__portsed} 's|@@MYAPP_LOGDIR@@|%{applogdir}|g' %{buildroot}%{_sysconfdir}/logrotate.d/%{appname}

# Install server.xml.skel
cp %{SOURCE8} %{buildroot}%{appconfdir}/server.xml.skel

# Setup user limits
cp %{SOURCE9} %{buildroot}%{_sysconfdir}/security/limits.d/%{appname}.conf
%{__portsed} 's|@@MYAPP_USER@@|%{appusername}|g' %{buildroot}%{_sysconfdir}/security/limits.d/%{appname}.conf

%if 0%{?suse_version} > 1140
# Setup Systemd
cp %{SOURCE10} %{buildroot}%{_systemdir}/%{appname}.service
%{__portsed} 's|@@MYAPP_APP@@|%{appname}|g' %{buildroot}%{_systemdir}/%{appname}.service
%{__portsed} 's|@@MYAPP_EXEC@@|%{appexec}|g' %{buildroot}%{_systemdir}/%{appname}.service
%endif

# Setup cron.d
cp %{SOURCE13} %{buildroot}%{_cronddir}/%{appname}
%{__portsed} 's|@@MYAPP_APP@@|%{appname}|g' %{buildroot}%{_cronddir}/%{appname}
%{__portsed} 's|@@MYAPP_CRON@@|%{appcron}|g' %{buildroot}%{_cronddir}/%{appname}
%{__portsed} 's|@@MYAPP_USER@@|%{appusername}|g' %{buildroot}%{_cronddir}/%{appname}

# Setup cron.sh
cp %{SOURCE14} %{buildroot}%{appcron}
%{__portsed} 's|@@MYAPP_APP@@|%{appname}|g' %{buildroot}%{appcron}
%{__portsed} 's|@@MYAPP_LOGDIR@@|%{applogdir}|g' %{buildroot}%{appcron}
%{__portsed} 's|@@MYAPP_USER@@|%{appusername}|g' %{buildroot}%{appcron}

# remove uneeded file in RPM
rm -f %{buildroot}%{appdir}/*.sh
rm -f %{buildroot}%{appdir}/*.bat
rm -f %{buildroot}%{appdir}/bin/*.bat
rm -rf %{buildroot}%{appdir}/logs
rm -rf %{buildroot}%{appdir}/temp
rm -rf %{buildroot}%{appdir}/work

# ensure shell scripts are executable
chmod 755 %{buildroot}%{appdir}/bin/*.sh

%clean
rm -rf %{buildroot}

%pre
%if 0%{?suse_version} > 1140
%service_add_pre %{appname}.service
%endif
# First install time, add user and group
if [ "$1" == "1" ]; then
  %{_sbindir}/groupadd -r -g %{appgroupid} %{appusername} 2>/dev/null || :
  %{_sbindir}/useradd -s /sbin/nologin -c "%{appname} user" -g %{appusername} -r -d %{appdatadir} -u %{appuserid} %{appusername} 2>/dev/null || :
else
# Update time, stop service if running
  if [ "$1" == "2" ]; then
    if [ -f %{_var}/run/%{appname}.pid ]; then
      %{servicestop}
      touch %{applogdir}rpm-update-stop
    fi
    # clean up deployed webapp
    rm -rf %{appwebappdir}/ROOT
    # clean up Tomcat workdir 
    rm -rf %{appworkdir}/Catalina
  fi
fi

%post
%if 0%{?suse_version} > 1140
%service_add_post %{appname}.service
%endif
%if 0%{?suse_version} > 1000
%fillup_only
%endif

# First install time, register service, generate random passwords and start application
if [ "$1" == "1" ]; then
  # register app as service
  %{serviceon}

  # Generated random password for RO and RW accounts
  if [ -f %{_sysconfdir}/sysconfig/%{appname} ]; then
    RANDOMVAL=`echo $RANDOM | md5sum | sed "s| -||g" | tr -d " "`
    sed -i "s|@@MYAPP_RO_PWD@@|$RANDOMVAL|g" %{_sysconfdir}/sysconfig/%{appname}
    RANDOMVAL=`echo $RANDOM | md5sum | sed "s| -||g" | tr -d " "`
    sed -i "s|@@MYAPP_RW_PWD@@|$RANDOMVAL|g" %{_sysconfdir}/sysconfig/%{appname}
  fi

  pushd %{appdir} >/dev/null
  ln -s %{applogdir}  logs
  ln -s %{apptempdir} temp
  ln -s %{appworkdir} work
  popd >/dev/null

  pushd %{appdatadir} >/dev/null
  rm -rf logs
  ln -s %{applogdir} logs
  popd >/dev/null

  # start application at first install (uncomment next line this behaviour not expected)
  # %{_initrddir}/%{name} start
else
  # Update time, restart application if it was running
  if [ "$1" == "2" ]; then
    if [ -f %{applogdir}/rpm-update-stop ]; then
      # restart application after update (comment next line this behaviour not expected)
      %{servicestart}
      rm -f %{applogdir}/rpm-update-stop
    fi
  fi
fi

%preun
%if 0%{?suse_version} > 1140
%service_del_preun %{appname}.service
%endif
if [ "$1" == "0" ]; then
  # Uninstall time, stop service and cleanup

  # stop service
  %{servicestop}

  # unregister app from services
  %{serviceoff}

  # finalize housekeeping
  rm -rf %{appdir}
  rm -rf %{applogdir}
  rm -rf %{apptempdir}
  rm -rf %{appworkdir}
fi

%postun
%if 0%{?suse_version} > 1140
%service_del_postun %{appname}.service
%endif
if [ "$1" == "0" ]; then
  if [ -d %{appwebappdir}/ROOT ]; then 
    rm -rf %{appwebappdir}/ROOT
  fi
fi

%files
%defattr(-,root,root)
%attr(0755,%{appusername},%{appusername}) %dir %{applogdir}
%attr(0755, root,root) %{_initrddir}/%{appname}

%if 0%{?suse_version} > 1140
%dir %{_systemddir}
%dir %{_systemdir}
%attr(0644,root,root) %{_systemdir}/%{appname}.service
%endif

%if 0%{?suse_version} > 1000
%{_var}/adm/fillup-templates/sysconfig.%{appname}
%else
%dir %{_sysconfdir}/sysconfig
%config(noreplace) %{_sysconfdir}/sysconfig/%{appname}
%endif

%config %{_sysconfdir}/logrotate.d/%{appname}
%dir %{_sysconfdir}/security/limits.d
%config %{_sysconfdir}/security/limits.d/%{appname}.conf
%config %{_cronddir}/%{appname}

# Suse Lint requires new dirs to be defined (owned)
%dir %{appdir}
%{appdir}/bin
%{appdir}/conf
%{appdir}/lib
%{appdir}/misc
%attr(-,%{appusername}, %{appusername}) %{appdir}/webapps
%attr(0755,%{appusername},%{appusername}) %dir %{appconflocaldir}
%attr(0755,%{appusername},%{appusername}) %dir %{appdatadir}
%ghost %{apptempdir}
%attr(0755,%{appusername},%{appusername}) %dir %{appworkdir}
# etc should be owned by app
%attr(-,%{appusername}, %{appusername})  %{appdatadir}/etc
%doc %{appdir}/NOTICE
%doc %{appdir}/RUNNING.txt
%doc %{appdir}/LICENSE
%doc %{appdir}/RELEASE-NOTES

%changelog
* Fri Sep 5 2014 henri.gomez@gmail.com 3.3.0-2
- Update Tomcat to 7.0.55

* Wed Aug 27 2014 henri.gomez@gmail.com 3.3.0-1
- Artifactory 3.3.0 released
- Download url moved to Bintray

* Wed Jun 4 2014 henri.gomez@gmail.com 3.2.1-1
- Artifactory 3.2.1 released
- Update Tomcat to 7.0.54

* Thu Apr 10 2014 henri.gomez@gmail.com 3.2.0-1
- Artifactory 3.2.0 released
- Update Tomcat to 7.0.53

* Thu Feb 27 2014 henri.gomez@gmail.com 3.1.1.1-1
- Artifactory 3.1.1.1 released
- Update Tomcat to 7.0.52

* Mon Jan 13 2014 henri.gomez@gmail.com 3.1.0-3
- Update Tomcat to 7.0.50

* Wed Dec 18 2013 henri.gomez@gmail.com 3.1.0-2
- Fix typo in seding init.d tempdir

* Mon Dec 16 2013 henri.gomez@gmail.com 3.1.0-1
- Artifactory 3.1.0 released

* Tue Nov 5 2013 henri.gomez@gmail.com 3.0.4-1
- Artifactory 3.0.4 released

* Sun Oct 27 2013 henri.gomez@gmail.com 3.0.3-2
- Update Tomcat to 7.0.47

* Tue Aug 20 2013 henri.gomez@gmail.com 3.0.3-1
- Artifactory 3.0.3 released

* Mon Jul 8 2013 henri.gomez@gmail.com 3.0.2-1
- Apache Tomcat 7.0.42 released
- Artifactory 3.0.2 released
- Use %ghost directive for /var/run contents (rpmlint)
- cron contents should be marked as %config (rpmlint)
- cron/logrotate required for SUSE (rpmlint)

* Wed Jun 12 2013 henri.gomez@gmail.com 3.0.1-2
- Apache Tomcat 7.0.41 released, update package

* Tue Jun 4 2013 henri.gomez@gmail.com 3.0.1-1
- Artifactory 3.0.1 released

* Fri May 17 2013 henri.gomez@gmail.com 3.0.0-2
- Apache Tomcat 7.0.40 released, update package

* Sun Apr 21 2013 henri.gomez@gmail.com 3.0.0-1
- Artifactory 3.0.0 released

- Simplify logrotate
- Use cron for housekeeping
- Move temp contents to /var/run/myartifactory
- Move work contents to /var/spool/myartifactory

* Mon Feb 18 2013 henri.gomez@gmail.com 2.6.7-1
- Apache Tomcat 7.0.39 released
- Artifactory 2.6.7 released

* Mon Feb 18 2013 henri.gomez@gmail.com 2.6.6-4
- Apache Tomcat 7.0.37 released, update package

* Fri Feb 1 2013 henri.gomez@gmail.com 2.6.6-3
- Use startproc instead of start_daemon to ensure userid is not overrided 

* Thu Jan 17 2013 henri.gomez@gmail.com 2.6.6-2
- Apache Tomcat 7.0.35 released, update package

* Thu Jan 3 2013 henri.gomez@gmail.com 2.6.6-1
- Artifactory 2.6.6 released

* Tue Dec 19 2012 henri.gomez@gmail.com 2.6.5-1
- Artifactory 2.6.5 released
- Use Apache Tomcat 7.0.34

* Fri Oct 12 2012 henri.gomez@gmail.com 2.6.4-3
- Use Apache Tomcat 7.0.32

* Wed Oct 3 2012 henri.gomez@gmail.com 2.6.4-2
- Reduce number of log files (manager and host-manager)

* Fri Sep 28 2012 henri.gomez@gmail.com 2.6.4-1
- Artifactory 2.6.4 released
- Use Apache Tomcat 7.0.30

* Mon Aug 20 2012 henri.gomez@gmail.com 2.6.3-1
- Artifactory 2.6.3 released
- Remove duplicate JMX settings definition

* Wed Jul 25 2012 henri.gomez@gmail.com 2.6.2-1
- Artifactory 2.6.2 released

* Wed Jul 11 2012 henri.gomez@gmail.com 2.6.1-3
- Tomcat 7.0.29 released

* Wed Jun 20 2012 henri.gomez@gmail.com 2.6.1-2
- Tomcat 7.0.28 released

* Wed May 16 2012 henri.gomez@gmail.com 2.6.1-1
- Artifactory 2.6.1 released

* Sun May 6 2012 henri.gomez@gmail.com 2.6.0-1
- Artifactory 2.6.0 released

* Wed Apr 25 2012 henri.gomez@gmail.com 2.5.2-1
- Artifactory 2.5.2 released

* Wed Mar 7 2012 henri.gomez@gmail.com 2.5.1-1
- Distribution dependant Requires for Java

* Fri Jan 6 2012 henri.gomez@gmail.com 2.5.1-0
- Create conf/Catalina/localhost with user rights

* Sat Dec 3 2011 henri.gomez@gmail.com 2.5.0-0
- Initial RPM
