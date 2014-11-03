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

%if 0%{?JENKINS_REL:1}
%define jenkins_rel    %{JENKINS_REL}
%else
%define jenkins_rel    1.588
%endif

Name: myjenkins
Version: %{jenkins_rel}
Release: 1
Summary: Jenkins %{jenkins_rel} powered by Apache Tomcat %{tomcat_rel}
Group: Development/Tools/Building
URL: http://jenkins-ci.org/
Vendor: devops-incubator
License: MIT
BuildArch:  noarch

%define appname         myjenkins
%define appusername     myjenkins
%define appuserid       1235
%define appgroupid      1235

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

%if 0%{?suse_version}
Requires: cron
Requires: logrotate
%endif

%if 0%{?suse_version}
Requires:           java >= 1.6.0
%endif

%if 0%{?fedora} || 0%{?rhel} || 0%{?centos}
Requires:           java >= 1:1.6.0
%endif

Requires(pre):      %{_sbindir}/groupadd
Requires(pre):      %{_sbindir}/useradd

Source0: http://www.eu.apache.org/dist/tomcat/tomcat-7/v%{tomcat_rel}/bin/apache-tomcat-%{tomcat_rel}.tar.gz
Source1: jenkins-%{jenkins_rel}.war
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

# myjenkins and myjenkins-lts are exclusive
Conflicts: myjenkins-lts

%description
In a nutshell Jenkins CI is the leading open-source continuous integration server. Built with Java, it provides over 400 plugins to support building and testing virtually any project.
This package contains Jenkins %{jenkins_rel} powered by Apache Tomcat %{tomcat_rel}

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

# jenkins webapp is ROOT.war (will respond to /)
cp %{SOURCE1}  %{buildroot}%{appwebappdir}/ROOT.war

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
mkdir -p %{buildroot}%{_systemdir}
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
      touch %{applogdir}/rpm-update-stop
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
%fillup_only -n %{appname}
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

  # start application at first install (uncomment next line this behaviour not expected)
  # %{servicestart}
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
%dir %{appdir}
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

%{appdir}/bin
%{appdir}/conf
%{appdir}/lib
%attr(-,%{appusername}, %{appusername}) %{appdir}/webapps
%attr(0755,%{appusername},%{appusername}) %dir %{appconflocaldir}
%attr(0755,%{appusername},%{appusername}) %dir %{appdatadir}
%ghost %{apptempdir}
%attr(0755,%{appusername},%{appusername}) %dir %{appworkdir}
%doc %{appdir}/NOTICE
%doc %{appdir}/RUNNING.txt
%doc %{appdir}/LICENSE
%doc %{appdir}/RELEASE-NOTES

%changelog
* Mon Nov 3 2014 hgomez@gmail.com 1.588-1
- Jenkins 1.588

* Thu Oct 2 2014 hgomez@gmail.com 1.583-1
- Jenkins 1.583

* Mon Sep 22 2014 hgomez@gmail.com 1.581-1
- Jenkins 1.581

* Mon Sep 15 2014 hgomez@gmail.com 1.580-1
- Jenkins 1.580

* Mon Sep 8 2014 hgomez@gmail.com 1.579-1
- Jenkins 1.579
- Use Apache Tomcat 7.0.55

* Fri Aug 1 2014 hgomez@gmail.com 1.574-1
- Jenkins 1.574

* Tue Jul 1 2014 hgomez@gmail.com 1.570-1
- Jenkins 1.570

* Tue Jun 17 2014 henri.gomez@gmail.com 1.568-1
- Jenkins 1.568 released

* Tue Jun 3 2014 henri.gomez@gmail.com 1.566-1
- Jenkins 1.566 released
- Use Apache Tomcat 7.0.54

* Tue May 6 2014 henri.gomez@gmail.com 1.562-1
- Jenkins 1.562 released

* Mon Apr 14 2014 henri.gomez@gmail.com 1.559-1
- Jenkins 1.559 released

* Thu Apr 10 2014 henri.gomez@gmail.com 1.558-1
- Jenkins 1.558 released
- Use Apache Tomcat 7.0.53

* Mon Mar 24 2014 henri.gomez@gmail.com 1.556-1
- Jenkins 1.556 released

* Mon Mar 17 2014 henri.gomez@gmail.com 1.555-1
- Jenkins 1.555 released

* Mon Mar 10 2014 henri.gomez@gmail.com 1.554-1
- Jenkins 1.554 released

* Thu Feb 27 2014 henri.gomez@gmail.com 1.552-1
- Jenkins 1.552 released
- Use Apache Tomcat 7.0.52

* Tue Jan 28 2014 henri.gomez@gmail.com 1.549-1
- Jenkins 1.549 released

* Mon Jan 13 2014 henri.gomez@gmail.com 1.547-1
- Jenkins 1.547 released
- Apache Tomcat 7.0.50 released

* Wed Dec 18 2013 henri.gomez@gmail.com 1.544-1
- Jenkins 1.544 released
- Fix typo in seding init.d tempdir

* Tue Dec 3 2013 henri.gomez@gmail.com 1.542-1
- Jenkins 1.542 released

* Mon Nov 25 2013 henri.gomez@gmail.com 1.541-1
- Jenkins 1.541 released

* Thu Nov 21 2013 henri.gomez@gmail.com 1.540-1
- Jenkins 1.540 released

* Thu Nov 21 2013 henri.gomez@gmail.com 1.539-1
- Jenkins 1.539 released

* Sun Oct 27 2013 henri.gomez@gmail.com 1.536-2
- Update Tomcat to 7.0.47

* Thu Oct 24 2013 henri.gomez@gmail.com 1.536-1
- Jenkins 1.536 released

* Fri Oct 4 2013 henri.gomez@gmail.com 1.533-1
- Jenkins 1.533 released

* Wed Sep 18 2013 henri.gomez@gmail.com 1.531-1
- Jenkins 1.531 released

* Tue Aug 20 2013 henri.gomez@gmail.com 1.528-1
- Jenkins 1.528 released

* Mon Jul 8 2013 henri.gomez@gmail.com 1.522-1
- Apache Tomcat 7.0.42 released
- Jenkins 1.522 released
- Use %ghost directive for /var/run contents (rpmlint)
- cron contents should be marked as %config (rpmlint)
- cron/logrotate required for SUSE (rpmlint)

* Sat Jun 29 2013 henri.gomez@gmail.com 1.520-1
- Jenkins 1.520 released

* Wed Jun 12 2013 henri.gomez@gmail.com 1.517-2
- Apache Tomcat 7.0.41 released, update package

* Tue Jun 3 2013 henri.gomez@gmail.com 1.517-1
- Jenkins 1.517 released

* Fri May 17 2013 henri.gomez@gmail.com 1.514-1
- Apache Tomcat 7.0.40 released, update package
- Jenkins 1.514 released

* Tue Apr 23 2013 henri.gomez@gmail.com 1.512-1
- Jenkins 1.512 released

* Mon Apr 15 2013 henri.gomez@gmail.com 1.511-1
- Jenkins 1.511 released

* Tue Apr 9 2013 henri.gomez@gmail.com 1.510-1
- Jenkins 1.510 released
- Simplify logrotate
- Use cron for housekeeping
- Move temp contents to /var/run/myjenkins
- Move work contents to /var/spool/myjenkins
- Apache Tomcat 7.0.39 released

* Mon Mar 18 2013 henri.gomez@gmail.com 1.506-1
- Jenkins 1.506 released

* Mon Mar 11 2013 henri.gomez@gmail.com 1.505-1
- Jenkins 1.505 released

* Wed Mar 6 2013 henri.gomez@gmail.com 1.504-1
- Jenkins 1.504 released

* Fri Feb 22 2013 henri.gomez@gmail.com 1.502-1
- Jenkins 1.502 released

* Mon Feb 18 2013 henri.gomez@gmail.com 1.501-2
- Apache Tomcat 7.0.37 released, update package

* Fri Feb 15 2013 henri.gomez@gmail.com 1.501-1
- Jenkins 1.501 released

* Fri Feb 1 2013 henri.gomez@gmail.com 1.500-1
- Use startproc instead of start_daemon to ensure userid is not overrided 
- Jenkins 1.500 released

* Thu Jan 17 2013 henri.gomez@gmail.com 1.499-1
- Apache Tomcat 7.0.35 released, update package
- Jenkins 1.499 released

* Tue Jan 8 2013 henri.gomez@gmail.com 1.498-1
- Jenkins 1.498 released (security fix)

* Thu Jan 3 2013 henri.gomez@gmail.com 1.496-1
- Jenkins 1.496 released

* Tue Dec 19 2012 henri.gomez@gmail.com 1.494-1
- Jenkins 1.494 released
- Use Apache Tomcat 7.0.34

* Fri Oct 12 2012 henri.gomez@gmail.com 1.485-1
- Jenkins 1.485 released
- Use Apache Tomcat 7.0.32

* Wed Oct 3 2012 henri.gomez@gmail.com 1.484-1
- Jenkins 1.484 released
- Reduce number of log files (manager and host-manager)

* Fri Sep 28 2012 henri.gomez@gmail.com 1.483-1
- Use Apache Tomcat 7.0.30
- Jenkins 1.483 released

* Fri Aug 31 2012 henri.gomez@gmail.com 1.479-1
- Jenkins 1.479 released

* Tue Aug 21 2012 henri.gomez@gmail.com 1.478-1
- Jenkins 1.478 released

* Mon Aug 20 2012 henri.gomez@gmail.com 1.477-1
- Jenkins 1.477 released
- Remove duplicate JMX settings definition

* Wed Jul 11 2012 henri.gomez@gmail.com 1.474-1
- Jenkins 1.474 released
- Tomcat 7.0.29 released

* Wed Jun 20 2012 henri.gomez@gmail.com 1.471-1
- Jenkins 1.471 released
- Tomcat 7.0.28 released

* Thu May 24 2012 henri.gomez@gmail.com 1.465-1
- Jenkins 1.465 released

* Wed May 16 2012 henri.gomez@gmail.com 1.464-1
- Jenkins 1.464 released

* Wed Apr 25 2012 henri.gomez@gmail.com 1.461-1
- Jenkins 1.461 released

* Wed Mar 7 2012 henri.gomez@gmail.com 1.455-0
- Distribution dependant Requires for Java

* Fri Jan 6 2012 henri.gomez@gmail.com 1.454-0
- Create conf/Catalina/localhost with user rights

* Sat Dec 3 2011 henri.gomez@gmail.com 1.453-0
- Initial RPM
