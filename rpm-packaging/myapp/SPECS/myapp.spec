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
%define tomcat_rel        7.0.54
%endif

%if 0%{?app_REL:1}
%define app_rel    %{app_REL}
%else
%define app_rel    1.0.0
%endif

Name:      app
Version:   %{app_rel}
Release:   16
Summary:   app %{app_rel} powered by Apache Tomcat %{tomcat_rel}
Group:     Applications/Communications
URL:       https://github.com/hgomez/devops-incubator
Vendor:    devops-incubator
Packager:  devops-incubator
License:   ASL 2.0
BuildArch: noarch

%define appname         myapp
%define appusername     myapp
%define appuserid       1234
%define appgroupid      1234

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

%define _cronddir         %{_sysconfdir}/cron.d
%define _initrddir        %{_sysconfdir}/init.d
%define _systemddir       /lib/systemd
%define _systemdir        %{_systemddir}/system

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
Requires:           java >= 1.6.0
%endif

%if 0%{?fedora} || 0%{?rhel} || 0%{?centos}
Requires:           java >= 1:1.6.0
%endif

Requires(pre):      %{_sbindir}/groupadd
Requires(pre):      %{_sbindir}/useradd

Source0: http://www.eu.apache.org/dist/tomcat/tomcat-7/v%{tomcat_rel}/bin/apache-tomcat-%{tomcat_rel}.tar.gz
Source1: https://github.com/hgomez/devops-incubator/blob/master/rpm-packaging/myapp/SOURCES/myapp-%{app_rel}.war
Source2: initd.skel
Source3: sysconfig.skel
Source4: jmxremote.access.skel
Source5: jmxremote.password.skel
Source6: setenv.sh.skel
Source7: logrotate.skel
Source8: server.xml.skel
Source9: limits.conf.skel
Source10: systemd.skel
Source11: http://www.eu.apache.org/dist/tomcat/tomcat-7/v%{tomcat_rel}/bin/extras/catalina-jmx-remote-%{tomcat_rel}.jar
Source12: crond.skel
Source13: cron.sh.skel

%description
Sample PerfWebApp %{app_rel} powered by Apache Tomcat %{tomcat_rel}.
This Web application could be used to tune your web benchmark systems

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
mkdir -p %{buildroot}%{_systemdir}

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
%{__portsed} 's|\${catalina.base}/logs|%{applogdir}|g' %{buildroot}%{appdir}/conf/logging.properties

# app webapp is ROOT.war (will respond to /)
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
cp %{SOURCE10} %{buildroot}%{_systemdir}/%{appname}.service
%{__portsed} 's|@@MYAPP_APP@@|%{appname}|g' %{buildroot}%{_systemdir}/%{appname}.service
%{__portsed} 's|@@MYAPP_EXEC@@|%{appexec}|g' %{buildroot}%{_systemdir}/%{appname}.service
%endif

# Setup cron.d
cp %{SOURCE12} %{buildroot}%{_cronddir}/%{appname}
%{__portsed} 's|@@MYAPP_APP@@|%{appname}|g' %{buildroot}%{_cronddir}/%{appname}
%{__portsed} 's|@@MYAPP_CRON@@|%{appcron}|g' %{buildroot}%{_cronddir}/%{appname}
%{__portsed} 's|@@MYAPP_USER@@|%{appusername}|g' %{buildroot}%{_cronddir}/%{appname}

# Setup cron.sh
cp %{SOURCE13} %{buildroot}%{appcron}
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
      %{_initrddir}/%{appname} stop
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
%if 0%{?fedora} || 0%{?rhel} || 0%{?centos} || 0%{?suse_version} < 1200
  chkconfig %{appname} on
%else
  systemctl enable %{appname}.service >/dev/null 2>&1
%endif

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
  # %{_initrddir}/%{name} start
else
  # Update time, restart application if it was running
  if [ "$1" == "2" ]; then
    if [ -f %{applogdir}/rpm-update-stop ]; then
      # restart application after update (comment next line this behaviour not expected)
      %{_initrddir}/%{name} start
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
  %{_initrddir}/%{appname} stop

  # unregister app from services
%if 0%{?fedora} || 0%{?rhel} || 0%{?centos} || 0%{?suse_version} < 1200
  chkconfig %{appname} off
%else
  systemctl disable %{appname}.service >/dev/null 2>&1
%endif

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

# Specific actions in relations with others packages
#%triggerin -- otherapp
# Do something if otherapp is installed

#%triggerun -- otherapp
# Do something if otherapp is uninstalled


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
* Thu Jun 19 2014 henri.gomez@gmail.com 1.0.0-16
- Apache Tomcat 7.0.54

* Sat Mar 1 2014 henri.gomez@gmail.com 1.0.0-15
- Apache Tomcat 7.0.52

* Mon Jan 13 2014 henri.gomez@gmail.com 1.0.0-14
- Apache Tomcat 7.0.50

* Wed Dec 18 2013 henri.gomez@gmail.com 1.0.0-13
- Add seding init.d tempdir

* Sun Oct 27 2013 henri.gomez@gmail.com 1.0.0-12
- Apache Tomcat 7.0.47
- Move to OBS

* Wed Jun 12 2013 henri.gomez@gmail.com 1.0.0-11
- Apache Tomcat 7.0.41 released, update package

* Fri May 17 2013 henri.gomez@gmail.com 1.0.0-10
- Apache Tomcat 7.0.40 released, update package

* Tue Apr 9 2013 henri.gomez@gmail.com 1.0.0-9
- Simplify logrotate
- Use cron for housekeeping
- Move temp contents to /var/run/myapp
- Move work contents to /var/spool/myapp

* Fri Mar 29 2013 henri.gomez@gmail.com 1.0.0-8
- Apache Tomcat 7.0.39 released, update package

* Mon Feb 18 2013 henri.gomez@gmail.com 1.0.0-7
- Apache Tomcat 7.0.37 released, update package

* Fri Feb 1 2013 henri.gomez@gmail.com 1.0.0-6
- Use startproc instead of start_daemon to ensure userid is not overrided 

* Thu Jan 17 2013 henri.gomez@gmail.com 1.0.0-5
- Apache Tomcat 7.0.35 released, update package

* Wed Mar 7 2012 henri.gomez@gmail.com 1.0.0-4
- Distribution dependant Requires for Java

* Fri Jan 6 2012 henri.gomez@gmail.com 1.0.0-2
- Create conf/Catalina/localhost with user rights

* Sat Dec 3 2011 henri.gomez@gmail.com 1.0.0-1
- Initial RPM
