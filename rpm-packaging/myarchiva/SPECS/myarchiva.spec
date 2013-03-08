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
%define tomcat_rel		%{TOMCAT_REL}
%else
%define tomcat_rel		7.0.37
%endif

%if 0%{?ARCHIVA_REL:1}
%define archiva_rel		%{ARCHIVA_REL}
%else
%define archiva_rel		1.4-M3
%endif

%if 0%{?MAIL_REL:1}
%define mail_rel		%{MAIL_REL}
%else
%define mail_rel		1.4.5
%endif

%if 0%{?ACTIVATION_REL:1}
%define activation_rel	%{ACTIVATION_REL}
%else
%define activation_rel	1.1.1
%endif

%if 0%{?DERBY_REL:1}
%define derby_rel       %{DERBY_REL}
%else
%define derby_rel    	10.9.1.0
%endif

# Adjust RPM version (- is not allowed, lowercase strings)
%define rpm_archiva_rel %(version_rel=`echo %{archiva_rel} | sed "s/-/./g" | tr "[:upper:]" "[:lower:]"`; echo "$version_rel")

Name: myarchiva

Version: %{rpm_archiva_rel}
Release: 6
Summary: Apache Archiva %{archiva_rel} powered by Apache Tomcat %{tomcat_rel}
Group: Development/Tools
URL: https://github.com/hgomez/devops-incubator
Vendor: devops-incubator
License: ASL 2.0
BuildArch:  noarch

%define appname         myarchiva
%define appusername     myarchiv
%define appuserid       1250
%define appgroupid      1250

%define appdir                     /opt/%{appname}
%define appdatadir                 %{_var}/lib/%{appname}
%define appdbdir          		   %{appdir}/db
%define applogdir                  %{_var}/log/%{appname}
%define appexec                    %{appdir}/bin/catalina.sh
%define appconfdir                 %{appdir}/conf
%define appconflocaldir            %{appdir}/conf/Catalina/localhost
%define applibdir                  %{appdir}/lib
%define appwebappdir               %{appdir}/webapps
%define apptempdir                 /tmp/%{appname}
%define appworkdir                 %{_var}/%{appname}

%define _systemdir        /lib/systemd/system
%define _initrddir        %{_sysconfdir}/init.d

BuildRoot: %{_tmppath}/build-%{name}-%{version}-%{release}

%if 0%{?suse_version} > 1140
BuildRequires: systemd
%{?systemd_requires}
%else
%define systemd_requires %{nil}
%endif

%if 0%{?suse_version}
Requires:           java = 1.6.0
%endif

%if 0%{?fedora} || 0%{?rhel} || 0%{?centos}
Requires:           java = 1:1.6.0
%endif

Requires(pre):      %{_sbindir}/groupadd
Requires(pre):      %{_sbindir}/useradd

Source0: apache-tomcat-%{tomcat_rel}.tar.gz
Source1: apache-archiva-%{archiva_rel}.war
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
Source12: mail-%{mail_rel}.jar
Source13: activation-%{activation_rel}.jar
Source14: derby-%{derby_rel}.jar
Source15: ROOT.xml
Source16: logging.properties.skel

%description
archiva %{archiva_rel} powered by Apache Tomcat

%prep
%setup -q -c

%build

%install
# Prep the install location.
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}%{_sysconfdir}/security/limits.d

mkdir -p %{buildroot}%{appdir}
mkdir -p %{buildroot}%{appdatadir}
mkdir -p %{buildroot}%{appdatadir}/conf
mkdir -p %{buildroot}%{applogdir}
mkdir -p %{buildroot}%{apptempdir}
mkdir -p %{buildroot}%{appworkdir}
mkdir -p %{buildroot}%{appwebappdir}
mkdir -p %{buildroot}%{appdbdir}

# Copy tomcat
mv apache-tomcat-%{tomcat_rel}/* %{buildroot}%{appdir}

# Create conf/Catalina/localhost
mkdir -p %{buildroot}%{appconflocaldir}

# remove default webapps
rm -rf %{buildroot}%{appdir}/webapps/*

# patches to have logs under /var/log/app
# remove manager and host-manager logs (via .skel file)
cp %{SOURCE16} %{buildroot}%{appdir}/conf/logging.properties
%{__portsed} 's|\${catalina.base}/logs|%{applogdir}|g' %{buildroot}%{appdir}/conf/logging.properties

# archiva webapp is ROOT.war (will respond to /), get it from zip file
cp %{SOURCE1} %{buildroot}%{appwebappdir}/ROOT.war

# copy libs
cp %{SOURCE12} %{buildroot}%{applibdir}
cp %{SOURCE13} %{buildroot}%{applibdir}
cp %{SOURCE14} %{buildroot}%{applibdir}

# ROOT.xml
cp %{SOURCE15} %{buildroot}%{appconflocaldir}
%{__portsed} 's|@@ARCHIVA_DATADIR@@|%{appdatadir}|g' %{buildroot}%{appconflocaldir}/ROOT.xml

# init.d
cp  %{SOURCE2} %{buildroot}%{_initrddir}/%{appname}
%{__portsed} 's|@@ARCHIVA_APP@@|%{appname}|g' %{buildroot}%{_initrddir}/%{appname}
%{__portsed} 's|@@ARCHIVA_USER@@|%{appusername}|g' %{buildroot}%{_initrddir}/%{appname}
%{__portsed} 's|@@ARCHIVA_VERSION@@|version %{version} release %{release}|g' %{buildroot}%{_initrddir}/%{appname}
%{__portsed} 's|@@ARCHIVA_EXEC@@|%{appexec}|g' %{buildroot}%{_initrddir}/%{appname}
%{__portsed} 's|@@ARCHIVA_DATADIR@@|%{appdatadir}|g' %{buildroot}%{_initrddir}/%{appname}
%{__portsed} 's|@@ARCHIVA_LOGDIR@@|%{applogdir}|g' %{buildroot}%{_initrddir}/%{appname}
%{__portsed} 's|@@ARCHIVA_TMPIR@@|%{apptempdir}|g' %{buildroot}%{_initrddir}/%{appname}

# sysconfig
cp  %{SOURCE3}  %{buildroot}%{_sysconfdir}/sysconfig/%{appname}
%{__portsed} 's|@@ARCHIVA_APP@@|%{appname}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{appname}
%{__portsed} 's|@@ARCHIVA_APPDIR@@|%{appdir}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{appname}
%{__portsed} 's|@@ARCHIVA_DATADIR@@|%{appdatadir}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{appname}
%{__portsed} 's|@@ARCHIVA_LOGDIR@@|%{applogdir}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{appname}
%{__portsed} 's|@@ARCHIVA_USER@@|%{appusername}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{appname}
%{__portsed} 's|@@ARCHIVA_CONFDIR@@|%{appconfdir}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{appname}

# JMX (including JMX Remote)
cp %{SOURCE11} %{buildroot}%{appdir}/lib
cp %{SOURCE4}  %{buildroot}%{appconfdir}/jmxremote.access.skel
cp %{SOURCE5}  %{buildroot}%{appconfdir}/jmxremote.password.skel

# Our custom setenv.sh to get back env variables
cp  %{SOURCE6} %{buildroot}%{appdir}/bin/setenv.sh
%{__portsed} 's|@@ARCHIVA_APP@@|%{appname}|g' %{buildroot}%{appdir}/bin/setenv.sh

# Install logrotate
cp %{SOURCE7} %{buildroot}%{_sysconfdir}/logrotate.d/%{appname}
%{__portsed} 's|@@ARCHIVA_LOGDIR@@|%{applogdir}|g' %{buildroot}%{_sysconfdir}/logrotate.d/%{appname}

# Install server.xml.skel
cp %{SOURCE8} %{buildroot}%{appconfdir}/server.xml.skel

# Setup user limits
cp %{SOURCE9} %{buildroot}%{_sysconfdir}/security/limits.d/%{appname}.conf
%{__portsed} 's|@@ARCHIVA_USER@@|%{appusername}|g' %{buildroot}%{_sysconfdir}/security/limits.d/%{appname}.conf

# Setup Systemd
%ifos linux
mkdir -p %{buildroot}%{_systemdir}
cp %{SOURCE10} %{buildroot}%{_systemdir}/%{appname}.service
%{__portsed} 's|@@ARCHIVA_APP@@|%{appname}|g' %{buildroot}%{_systemdir}/%{appname}.service
%{__portsed} 's|@@ARCHIVA_EXEC@@|%{appexec}|g' %{buildroot}%{_systemdir}/%{appname}.service
%endif

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
	# clean up deployed webapps
	rm -rf %{appwebappdir}/ROOT
  fi
fi

%post
%if 0%{?suse_version} > 1140
%service_add_post %{appname}.service
%endif
# First install time, register service, generate random passwords and start application
if [ "$1" == "1" ]; then
  # register app as service
  systemctl enable %{appname}.service >/dev/null 2>&1

%if 0%{?fedora} || 0%{?rhel} || 0%{?centos}
  chkconfig %{appname} on
%endif

  # Generated random password for RO and RW accounts
  RANDOMVAL=`echo $RANDOM | md5sum | sed "s| -||g" | tr -d " "`
  %{__portsed} "s|@@ARCHIVA_RO_PWD@@|$RANDOMVAL|g" %{_sysconfdir}/sysconfig/%{appname}
  RANDOMVAL=`echo $RANDOM | md5sum | sed "s| -||g" | tr -d " "`
  %{__portsed} "s|@@ARCHIVA_RW_PWD@@|$RANDOMVAL|g" %{_sysconfdir}/sysconfig/%{appname}

  pushd %{appdir} >/dev/null
  ln -s %{applogdir}  logs
  ln -s %{apptempdir} temp
  ln -s %{appworkdir} work
  popd >/dev/null

  # start application at first install (uncomment next line this behaviour not expected)
  # %{_initrddir}/%{appname} start
else
  # Update time, restart application if it was running
  if [ "$1" == "2" ]; then
    if [ -f %{applogdir}/rpm-update-stop ]; then
      # restart application after update (comment next line this behaviour not expected)
      %{_initrddir}/%{appname} start
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
  systemctl disable %{appname}.service >/dev/null 2>&1

%if 0%{?fedora} || 0%{?rhel} || 0%{?centos}
  chkconfig %{appname} off
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

%files
%defattr(-,root,root)
%attr(0755,%{appusername},%{appusername}) %dir %{applogdir}
%attr(0755, root,root) %{_initrddir}/%{appname}
%ifos linux
%attr(0644,root,root) %{_systemdir}/%{appname}.service
%endif
%config(noreplace) %{_sysconfdir}/sysconfig/%{appname}
%config %{_sysconfdir}/logrotate.d/%{appname}
%config %{_sysconfdir}/security/limits.d/%{appname}.conf

%{appdir}/bin
%{appdir}/conf
%{appdir}/lib

%attr(-,%{appusername}, %{appusername}) %{appdir}/webapps
%attr(0755,%{appusername},%{appusername}) %dir %{appconflocaldir}
%attr(0755,%{appusername},%{appusername}) %dir %{appdatadir}
%attr(0755,%{appusername},%{appusername}) %dir %{appdatadir}/conf
%attr(0755,%{appusername},%{appusername}) %dir %{apptempdir}
%attr(0755,%{appusername},%{appusername}) %dir %{appworkdir}
%doc %{appdir}/NOTICE
%doc %{appdir}/RUNNING.txt
%doc %{appdir}/LICENSE
%doc %{appdir}/RELEASE-NOTES

%changelog
* Mon Feb 18 2013 henri.gomez@gmail.com 1.4.m3-6
- Apache Tomcat 7.0.37 released, update package

* Fri Feb 1 2013 henri.gomez@gmail.com 1.4.m3-5
- Use startproc instead of start_daemon to ensure userid is not overrided 

* Thu Jan 17 2013 henri.gomez@gmail.com 1.4.m3-4
- Apache Tomcat 7.0.35 released, update package

* Tue Dec 19 2012 henri.gomez@gmail.com 1.4.m3-3
- Update to Apache Tomcat 7.0.34
- Apply patch from Brett Potter

* Fri Oct 12 2012 henri.gomez@gmail.com 1.4.m3-1
- Update Apache Tomcat 7.0.32
- Update to Archiva 1.4-M3, with new js based ui

* Wed Oct 3 2012 henri.gomez@gmail.com 1.4.m2-2
- Reduce number of log files (manager and host-manager)

* Mon Sep 28 2012 henri.gomez@gmail.com 1.4.m2-1
- Initial RPM
