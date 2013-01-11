# Avoid unnecessary debug-information (native code)
%define    debug_package %{nil}

# Avoid jar repack (brp-java-repack-jars)
#%define __jar_repack 0

# Avoid CentOS 5/6 extras processes on contents (especially brp-java-repack-jars)
%define __os_install_post %{nil}

%ifos darwin
%define __portsed sed -i "" -e
%else
%define __portsed sed -i
%endif

%if %{?TOMCAT_REL:1}
%define tomcat_rel        %{TOMCAT_REL}
%else
%define tomcat_rel        7.0.34
%endif

%if %{?SONAR_REL:1}
%define sonar_rel    %{SONAR_REL}
%else
%define sonar_rel    3.4.1
%endif

Name: mysonar
Version: %{sonar_rel}
Release: 1
Summary: Sonar %{sonar_rel} powered by Apache Tomcat %{tomcat_rel}
Group: Development/Tools
URL: https://github.com/hgomez/devops-incubator
Vendor: devops-incubator
License: LGPL
BuildArch:  noarch

%define app             mysonar
%define appusername     mysonar
%define appuserid       1237
%define appgroupid      1237

%define appdir          /opt/%{app}
%define appdatadir      %{_var}/lib/%{app}
%define applogdir       %{_var}/log/%{app}
%define appexec         %{appdir}/bin/catalina.sh
%define appconfdir      %{appdir}/conf
%define appconflocaldir %{appdir}/conf/Catalina/localhost
%define appwebappdir    %{appdir}/webapps
%define apptempdir      /tmp/%{app}
%define appworkdir      %{_var}/%{app}

%define _systemdir        /lib/systemd/system
%define _initrddir        %{_sysconfdir}/init.d

BuildRoot: %{_tmppath}/build-%{name}-%{version}-%{release}

%if 0%{?suse_version} > 1140
BuildRequires: systemd
%{?systemd_requires}
%else
%define systemd_requires %{nil}
%endif

BuildRequires:      unzip

%if 0%{?suse_version}
Requires:           java = 1.6.0
%endif

%if 0%{?fedora} || 0%{?rhel} || 0%{?centos}
Requires:           java = 1:1.6.0
%endif

Requires(pre):      %{_sbindir}/groupadd
Requires(pre):      %{_sbindir}/useradd

Source0: apache-tomcat-%{tomcat_rel}.tar.gz
Source1: sonar-%{sonar_rel}.zip
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
Source12: sonar.properties
Source13: sonar-setup-mysql.sh
Source14: logging.properties.skel

%description
Sonar %{sonar_rel} powered by Apache Tomcat %{tomcat_rel}

%prep
%setup -q -c

%build
unzip %{SOURCE1}
cp -f %{SOURCE12} sonar-%{sonar_rel}/conf
pushd sonar-%{sonar_rel}/war >>/dev/null
./build-war.sh
popd >>/dev/null

%install
# Prep the install location.
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}%{_sysconfdir}/security/limits.d
mkdir -p %{buildroot}%{_systemdir}

mkdir -p %{buildroot}%{appdir}
mkdir -p %{buildroot}%{appdatadir}
mkdir -p %{buildroot}%{appdatadir}/conf
mkdir -p %{buildroot}%{applogdir}
mkdir -p %{buildroot}%{apptempdir}
mkdir -p %{buildroot}%{appworkdir}
mkdir -p %{buildroot}%{appwebappdir}

# Copy tomcat
mv apache-tomcat-%{tomcat_rel}/* %{buildroot}%{appdir}

# Create conf/Catalina/localhost
mkdir -p %{buildroot}%{appconflocaldir}

# remove default webapps
rm -rf %{buildroot}%{appdir}/webapps/*

# patches to have logs under /var/log/app
# patches to have logs under /var/log/app
# remove manager and host-manager logs (via .skel file)
cp %{SOURCE14} %{buildroot}%{appdir}/conf/logging.properties
%{__portsed} 's|\${catalina.base}/logs|%{applogdir}|g' %{buildroot}%{appdir}/conf/logging.properties

# copy Sonar generated webapp as ROOT.war (will respond to /)
cp sonar-%{sonar_rel}/war/sonar.war  %{buildroot}%{appwebappdir}/ROOT.war

# copy logback.xml in SONAR_HOME/conf
cp sonar-%{sonar_rel}/conf/logback.xml %{buildroot}%{appdatadir}/conf
# copy sonar.properties also in SONAR_HOME/conf
cp %{SOURCE12} %{buildroot}%{appdatadir}/conf
# copy required stuff in SONAR_HOME
cp -r sonar-%{sonar_rel}/extras %{buildroot}%{appdatadir}
cp -r sonar-%{sonar_rel}/extensions %{buildroot}%{appdatadir}
find %{buildroot}%{appdatadir}/extensions -type f -name "*.jar" -exec chmod 644 \{\} \;
cp -r sonar-%{sonar_rel}/lib %{buildroot}%{appdatadir}
# data dir (if derby usage)
mkdir -p %{buildroot}%{appdatadir}/data

# init.d
cp  %{SOURCE2} %{buildroot}%{_initrddir}/%{app}
%{__portsed} 's|@@SONAR_APP@@|%{app}|g' %{buildroot}%{_initrddir}/%{app}
%{__portsed} 's|@@SONAR_USER@@|%{appusername}|g' %{buildroot}%{_initrddir}/%{app}
%{__portsed} 's|@@SONAR_VERSION@@|version %{version} release %{release}|g' %{buildroot}%{_initrddir}/%{app}
%{__portsed} 's|@@SONAR_EXEC@@|%{appexec}|g' %{buildroot}%{_initrddir}/%{app}

# sysconfig
cp  %{SOURCE3}  %{buildroot}%{_sysconfdir}/sysconfig/%{app}
%{__portsed} 's|@@SONAR_APP@@|%{app}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{app}
%{__portsed} 's|@@SONAR_APPDIR@@|%{appdir}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{app}
%{__portsed} 's|@@SONAR_DATADIR@@|%{appdatadir}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{app}
%{__portsed} 's|@@SONAR_LOGDIR@@|%{applogdir}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{app}
%{__portsed} 's|@@SONAR_USER@@|%{appusername}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{app}
%{__portsed} 's|@@SONAR_CONFDIR@@|%{appconfdir}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{app}

# JMX (including JMX Remote)
cp %{SOURCE11} %{buildroot}%{appdir}/lib
cp %{SOURCE4}  %{buildroot}%{appconfdir}/jmxremote.access.skel
cp %{SOURCE5}  %{buildroot}%{appconfdir}/jmxremote.password.skel

# Our custom setenv.sh to get back env variables
cp  %{SOURCE6} %{buildroot}%{appdir}/bin/setenv.sh
%{__portsed} 's|@@SONAR_APP@@|%{app}|g' %{buildroot}%{appdir}/bin/setenv.sh

# Install logrotate
cp %{SOURCE7} %{buildroot}%{_sysconfdir}/logrotate.d/%{app}
%{__portsed} 's|@@SONAR_LOGDIR@@|%{applogdir}|g' %{buildroot}%{_sysconfdir}/logrotate.d/%{app}

# Install server.xml.skel
cp %{SOURCE8} %{buildroot}%{appconfdir}/server.xml.skel

# Setup user limits
cp %{SOURCE9} %{buildroot}%{_sysconfdir}/security/limits.d/%{app}.conf
%{__portsed} 's|@@SONAR_USER@@|%{appusername}|g' %{buildroot}%{_sysconfdir}/security/limits.d/%{app}.conf

# Setup Systemd
cp %{SOURCE10} %{buildroot}%{_systemdir}/%{app}.service
%{__portsed} 's|@@SONAR_APP@@|%{app}|g' %{buildroot}%{_systemdir}/%{app}.service
%{__portsed} 's|@@SONAR_EXEC@@|%{appexec}|g' %{buildroot}%{_systemdir}/%{app}.service

# remove uneeded file in RPM
rm -f %{buildroot}%{appdir}/*.sh
rm -f %{buildroot}%{appdir}/*.bat
rm -f %{buildroot}%{appdir}/bin/*.bat
rm -rf %{buildroot}%{appdir}/logs
rm -rf %{buildroot}%{appdir}/temp
rm -rf %{buildroot}%{appdir}/work

# ensure shell scripts are executable
chmod 755 %{buildroot}%{appdir}/bin/*.sh

# install mysql setup for sonar
cp %{SOURCE13} %{buildroot}%{_bindir}

%clean
rm -rf %{buildroot}

%pre
%if 0%{?suse_version} > 1140
%service_add_pre %{app}.service
%endif
# First install time, add user and group
if [ "$1" == "1" ]; then
  %{_sbindir}/groupadd -r -g %{appgroupid} %{appusername} 2>/dev/null || :
  %{_sbindir}/useradd -s /sbin/nologin -c "%{app} user" -g %{appusername} -r -d %{appdatadir} -u %{appuserid} %{appusername} 2>/dev/null || :
else
# Update time, stop service if running
  if [ "$1" == "2" ]; then
    if [ -f %{_var}/run/%{app}.pid ]; then
      %{_initrddir}/%{app} stop
      touch %{applogdir}/rpm-update-stop
    fi
    # clean up deployed webapp
    rm -rf %{appwebappdir}/ROOT
  fi
fi

%post
%if 0%{?suse_version} > 1140
%service_add_post %{app}.service
%endif
# First install time, register service, generate random passwords and start application
if [ "$1" == "1" ]; then
  # register app as service
  systemctl enable %{app}.service >/dev/null 2>&1

  # Generated random password for RO and RW accounts
  RANDOMVAL=`echo $RANDOM | md5sum | sed "s| -||g" | tr -d " "`
  sed -i "s|@@SONAR_RO_PWD@@|$RANDOMVAL|g" %{_sysconfdir}/sysconfig/%{app}
  RANDOMVAL=`echo $RANDOM | md5sum | sed "s| -||g" | tr -d " "`
  sed -i "s|@@SONAR_RW_PWD@@|$RANDOMVAL|g" %{_sysconfdir}/sysconfig/%{app}

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
%service_del_preun %{app}.service
%endif
if [ "$1" == "0" ]; then
  # Uninstall time, stop service and cleanup

  # stop service
  %{_initrddir}/%{app} stop

  # unregister app from services
  systemctl disable %{app}.service >/dev/null 2>&1

  # finalize housekeeping
  rm -rf %{appdir}
  rm -rf %{applogdir}
  rm -rf %{apptempdir}
  rm -rf %{appworkdir}
fi

%postun
%if 0%{?suse_version} > 1140
%service_del_postun %{app}.service
%endif

%files
%defattr(-,root,root)
%attr(0755,%{appusername},%{appusername}) %dir %{applogdir}
%attr(0755, root,root) %{_initrddir}/%{app}
%attr(0644,root,root) %{_systemdir}/%{app}.service
%config(noreplace) %{_sysconfdir}/sysconfig/%{app}
%config %{_sysconfdir}/logrotate.d/%{app}
%config %{_sysconfdir}/security/limits.d/%{app}.conf
%{appdir}/bin
%{appdir}/conf
%{appdir}/lib
%attr(-,%{appusername}, %{appusername}) %{appdir}/webapps
%attr(0755,%{appusername},%{appusername}) %dir %{appconflocaldir}
%attr(0755,%{appusername},%{appusername}) %dir %{appdatadir}
%attr(0755,%{appusername},%{appusername}) %dir %{apptempdir}
%attr(0755,%{appusername},%{appusername}) %dir %{appworkdir}
%config(noreplace) %{appdatadir}/conf
%attr(0755,%{appusername},%{appusername}) %dir %{appdatadir}/data
%attr(-,%{appusername},%{appusername}) %{appdatadir}/extensions
%{appdatadir}/extras
%{appdatadir}/lib
%{_bindir}
%doc %{appdir}/NOTICE
%doc %{appdir}/RUNNING.txt
%doc %{appdir}/LICENSE
%doc %{appdir}/RELEASE-NOTES

%changelog
* Tue Jan 8 2013 henri.gomez@gmail.com 3.4.1-1
- Sonar 3.4.1 released

* Mon Jan 7 2013 henri.gomez@gmail.com 3.4-1
- Sonar 3.4 released

* Fri Dec 21 2012 henri.gomez@gmail.com 3.3.2-2
- Sonar came with H2 as default SQL engine since 3.2, replace Derby defaults by H2

* Tue Dec 19 2012 henri.gomez@gmail.com 3.3.2-1
- Sonar 3.3.2 released
- Use Apache Tomcat 7.0.34

* Fri Oct 12 2012 henri.gomez@gmail.com 3.2.1-2
- Use Apache Tomcat 7.0.32

* Wed Oct 3 2012 henri.gomez@gmail.com 3.2.1-1
- Sonar 3.2.1 released
- Reduce number of log files (manager and host-manager)

* Fri Sep 28 2012 henri.gomez@gmail.com 3.2-2
- Use Apache Tomcat 7.0.30

* Mon Aug 20 2012 henri.gomez@gmail.com 3.2-1
- Sonar 3.2 released
- Remove duplicate JMX settings definition

* Wed Jul 11 2012 henri.gomez@gmail.com 3.1.1-1
- Sonar 3.1.1 released
- Tomcat 7.0.29 released

* Wed Jun 20 2012 henri.gomez@gmail.com 3.1-2
- Tomcat 7.0.28 released

* Thu Jun 14 2012 henri.gomez@gmail.com 3.1-1
- Sonar 3.1 released

* Wed May 16 2012 henri.gomez@gmail.com 3.0.1-1
- Sonar 3.0.1 released

* Mon Apr 23 2012 henri.gomez@gmail.com 3.0-1
- Sonar 3.0 released

* Tue Mar 20 2012 henri.gomez@gmail.com 2.14-0
- Sonar 2.14 released
- Fix RPM for CentOS

* Wed Mar 7 2012 henri.gomez@gmail.com 2.13.1-2
- Distribution dependant Requires for Java

* Fri Jan 6 2012 henri.gomez@gmail.com 2.12-1
- Create conf/Catalina/localhost with user rights

* Sat Dec 3 2011 henri.gomez@gmail.com 2.12-0
- Initial RPM
