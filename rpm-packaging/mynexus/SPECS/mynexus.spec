# Avoid unnecessary debug-information (native code)
%define     debug_package %{nil}

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
%define tomcat_rel        7.0.57
%endif

%if 0%{?NEXUS_REL:1}
%define nexus_rel    %{NEXUS_REL}
%else
%define nexus_rel    2.10.0
%endif

%if 0%{?NEXUS_FULL_REL:1}
%define nexus_full_rel    %{NEXUS_FULL_REL}
%else
%define nexus_full_rel    2.10.0-02
%endif

Name: mynexus
Version: %{nexus_rel}
Release: 2
Summary: Sonatype Nexus OSS %{nexus_rel} powered by Apache Tomcat %{tomcat_rel}
Group: Development/Tools/Building
URL: http://www.sonatype.org/nexus/
Vendor: devops-incubator
License: EPL-1.0
BuildArch:  noarch

%define appname         mynexus
%define appusername     mynexus
%define appuserid       1236
%define appgroupid      1236

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

BuildRequires:      zip
BuildRequires:      unzip

%if 0%{?suse_version} > 1000
PreReq: %fillup_prereq
%endif

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
Source1: http://download.sonatype.com/nexus/oss/nexus-%{nexus_rel}.war
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
Source15: http://repo1.maven.org/maven2/org/sonatype/nexus/plugins/nexus-p2-bridge-plugin/%{nexus_full_rel}/nexus-p2-bridge-plugin-%{nexus_full_rel}-bundle.zip
Source16: http://repo1.maven.org/maven2/org/sonatype/nexus/plugins/nexus-p2-repository-plugin/%{nexus_full_rel}/nexus-p2-repository-plugin-%{nexus_full_rel}-bundle.zip

%description
Nexus manages software artifacts required for development. If you develop software, your builds can download dependencies from Nexus and can publish artifacts to Nexus creating a new way to share artifacts within an organization.
This package contains Sonatype Nexus OSS %{nexus_rel} powered by Apache Tomcat %{tomcat_rel}

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

# hack nexus.properties inside war
mkdir webapp
cd webapp
unzip %{SOURCE1}
# remove /sonatype-work/nexus
%{__portsed} 's|/sonatype-work/nexus||g' WEB-INF/classes/nexus.properties
zip -r ROOT.war *
cp ROOT.war %{buildroot}%{appwebappdir}/ROOT.war
cd ..
rm -rf webapp

# Copy P2 Plugins
mkdir -p %{buildroot}%{appdatadir}/plugin-repository
unzip %{SOURCE15}
mv nexus-p2-bridge-plugin-* %{buildroot}%{appdatadir}/plugin-repository
unzip %{SOURCE16}
mv nexus-p2-repository-plugin-* %{buildroot}%{appdatadir}/plugin-repository
# fix mad rights (rpmlint)
find %{buildroot}%{appdatadir}/plugin-repository -type f -exec chmod 644 \{\} \;
find %{buildroot}%{appdatadir}/plugin-repository -type d -exec chmod 755 \{\} \;

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
%attr(-,%{appusername},%{appusername}) %{appdatadir}/plugin-repository

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
* Sun Nov 23 2014 henri.gomez@gmail.com 2.10.0-2
- Use Apache Tomcay 7.0.57

* Sat Nov 8 2014 henri.gomez@gmail.com 2.10.0-1
- Nexus 2.10.0-02 released

* Thu Oct 2 2014 henri.gomez@gmail.com 2.9.2-1
- Nexus 2.9.2-01 released

* Tue Sep 23 2014 henri.gomez@gmail.com 2.9.1-2
- Add P2 support via P2 OSS Plugins

* Tue Sep 9 2014 henri.gomez@gmail.com 2.9.1-1
- Nexus 2.9.1-02 released

* Fri Sep 5 2014 henri.gomez@gmail.com 2.9.0-1
- Nexus 2.9.0-04 released
- Use Apache Tomcay 7.0.55

* Tue Jun 17 2014 henri.gomez@gmail.com 2.8.1-1
- Nexus 2.8.1-01 released
- Use Apache Tomcay 7.0.54

* Thu Apr 10 2014 henri.gomez@gmail.com 2.8.0-1
- Nexus 2.8.0-05 released
- Apache Tomcay 7.0.53 released
- Hack nexus.properties inside webapp

* Mon Feb 24 2014 henri.gomez@gmail.com 2.7.2-1
- Nexus 2.7.2-03 released
- Apache Tomcay 7.0.52 released

* Mon Jan 13 2014 henri.gomez@gmail.com 2.7.0-3
- Apache Tomcay 7.0.50 released

* Tue Jan 7 2014 henri.gomez@gmail.com 2.7.0-2
- Nexus 2.7.0-06 released

* Wed Dec 18 2013 henri.gomez@gmail.com 2.7.0-1
- Nexus 2.7.0 released
- Fix typo in seding init.d tempdir

* Sun Oct 27 2013 henri.gomez@gmail.com 2.6.3-2
- Update Tomcat to 7.0.47

* Wed Sep 18 2013 henri.gomez@gmail.com 2.6.3-1
- Nexus 2.6.3 released

* Tue Aug 20 2013 henri.gomez@gmail.com 2.6.1-1
- Nexus 2.6.1 released

* Mon Jul 8 2013  henri.gomez@gmail.com 2.5.1-1
- Apache Tomcat 7.0.42 released
- Nexus 2.5.1 released
- Use %ghost directive for /var/run contents (rpmlint)
- cron contents should be marked as %config (rpmlint)

* Wed Jun 12 2013 henri.gomez@gmail.com 2.5.0-2
- Apache Tomcat 7.0.41 released, update package

* Tue Jun 4 2013 henri.gomez@gmail.com 2.5.0-1
- Nexus 2.5.0 released
- Java 7 required, Nexus 2.6+ will mandate it

* Fri May 17 2013 henri.gomez@gmail.com 2.4.0-2
- Apache Tomcat 7.0.40 released, update package

* Tue Apr 23 2013 henri.gomez@gmail.com 2.4.0-1
- Nexus 2.4.0 released

* Tue Apr 9 2013 henri.gomez@gmail.com 2.3.1-3
- Simplify logrotate
- Use cron for housekeeping
- Move temp contents to /var/run/mynexus
- Move work contents to /var/spool/mynexus
- Apache Tomcat 7.0.39 released

* Mon Feb 18 2013 henri.gomez@gmail.com 2.3.1-2
- Apache Tomcat 7.0.37 released, update package

* Fri Feb 15 2013 henri.gomez@gmail.com 2.3.1-1
- Nexus 2.3.1 released 

* Fri Feb 1 2013 henri.gomez@gmail.com 2.3.0-2
- Use startproc instead of start_daemon to ensure userid is not overrided 

* Thu Jan 17 2013 henri.gomez@gmail.com 2.3.0-1
- Apache Tomcat 7.0.35 released, update package
- Nexus 2.3.0

* Tue Dec 19 2012 henri.gomez@gmail.com 2.2-1
- Use Apache Tomcat 7.0.34
- Nexus 2.2

* Fri Oct 12 2012 henri.gomez@gmail.com 2.1.2-4
- Use Apache Tomcat 7.0.32

* Wed Oct 3 2012 henri.gomez@gmail.com 2.1.2-3
- Reduce number of log files (manager and host-manager)

* Fri Sep 28 2012 henri.gomez@gmail.com 2.1.2-2
- Use Apache Tomcat 7.0.30

* Fri Aug 31 2012 henri.gomez@gmail.com 2.1.2-1
- Nexus 2.1.2 released

* Mon Aug 20 2012 henri.gomez@gmail.com 2.1.1-1
- Nexus 2.1.1 released
- Remove duplicate JMX settings definition

* Wed Jul 11 2012 henri.gomez@gmail.com 2.0.6-1
- Nexus 2.0.6 released
- Tomcat 7.0.29 released

* Wed Jun 20 2012 henri.gomez@gmail.com 2.0.5-2
- Tomcat 7.0.28 released

* Thu Jun 14 2012 henri.gomez@gmail.com 2.0.5-1
- Nexus 2.0.5 released, RPM updated

* Thu May 24 2012 henri.gomez@gmail.com 2.0.4-1
- Nexus 2.0.4 released, RPM updated

* Wed Apr 25 2012 henri.gomez@gmail.com 2.0.3-1
- Set default release to 1 instead of 0

* Wed Mar 7 2012 henri.gomez@gmail.com 2.0.2-0
- Distribution dependant Requires for Java
- Nexus 2.0.2 released

* Fri Jan 6 2012 henri.gomez@gmail.com 2.0.1-0
- Create conf/Catalina/localhost with user rights

* Sat Dec 3 2011 henri.gomez@gmail.com 1.99-0
- Initial RPM
