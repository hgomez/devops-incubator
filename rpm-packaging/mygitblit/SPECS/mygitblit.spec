%if %{?TOMCAT_REL:1}
%define tomcat_rel        %{TOMCAT_REL}
%else
%define tomcat_rel        7.0.25
%endif

%if %{?GITBLIT_REL:1}
%define gitblit_rel    %{GITBLIT_REL}
%else
%define gitblit_rel    0.8.2
%endif

Name: mygitblit
Version: %{gitblit_rel}
Release: 3
Summary: GitBlit %{gitblit_rel} powered by Apache Tomcat %{tomcat_rel}
Group: Applications/Communications
URL: http://www.mycorp.org/
Vendor: MyCorp
Packager: MyCorp
License: AGPLv1
BuildArch:  noarch

%define gitblit             mygitblit
%define gitblitusername     mygitblit
%define gitblituserid       1238
%define gitblitgroupid      1238

%define gitblitdir          /opt/%{gitblit}
%define gitblitdatadir      %{_var}/lib/%{gitblit}
%define gitblitlogdir       %{_var}/log/%{gitblit}
%define gitblitexec         %{gitblitdir}/bin/catalina.sh
%define gitblitconfdir      %{gitblitdir}/conf
%define gitblitconflocaldir %{gitblitdir}/conf/Catalina/localhost
%define gitblitwebappdir    %{gitblitdir}/webapps
%define gitblittempdir      /tmp/%{gitblit}
%define gitblitworkdir      %{_var}/%{gitblit}

%define _systemdir          /lib/systemd/system
%define _initrddir          %{_sysconfdir}/init.d

BuildRoot: %{_tmppath}/build-%{name}-%{version}-%{release}

%if 0%{?suse_version} > 1140
BuildRequires: systemd
%{?systemd_requires}
%endif

%if 0%{suse_version} <= 1140
%define systemd_requires %{nil}
%endif

Requires:           java = 1.6.0
Requires(pre):      %{_sbindir}/groupadd
Requires(pre):      %{_sbindir}/useradd

Source0: apache-tomcat-%{tomcat_rel}.tar.gz
Source1: gitblit-%{gitblit_rel}.war
Source2: initd
Source3: sysconfig
Source4: jmxremote.access.skel
Source5: jmxremote.password.skel
Source6: setenv.sh
Source7: logrotate
Source8: server.xml.skel
Source9: limits.conf
Source10: systemd
Source11: catalina-jmx-remote-%{tomcat_rel}.jar
Source12: context.xml
#Source13: users.properties
Source13: users.conf


%description
GitBlit %{gitblit_rel} powered by Apache Tomcat %{tomcat_rel}

%prep
%setup -q -c

%build

%install
# Prep the install location.
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_initrddir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/security/limits.d
mkdir -p $RPM_BUILD_ROOT%{_systemdir}

mkdir -p $RPM_BUILD_ROOT%{gitblitdir}
mkdir -p $RPM_BUILD_ROOT%{gitblitdatadir}
mkdir -p $RPM_BUILD_ROOT%{gitblitdatadir}/conf
mkdir -p $RPM_BUILD_ROOT%{gitblitdatadir}/repos

mkdir -p $RPM_BUILD_ROOT%{gitblitlogdir}
mkdir -p $RPM_BUILD_ROOT%{gitblittempdir}
mkdir -p $RPM_BUILD_ROOT%{gitblitworkdir}
mkdir -p $RPM_BUILD_ROOT%{gitblitwebappdir}

# Copy tomcat
mv apache-tomcat-%{tomcat_rel}/* $RPM_BUILD_ROOT%{gitblitdir}

# Create conf/Catalina/localhost
mkdir -p $RPM_BUILD_ROOT%{gitblitconflocaldir}

# remove default webapps
rm -rf $RPM_BUILD_ROOT%{gitblitdir}/webapps/*

# patches to have logs under /var/log/gitblit
sed -i 's|\${catalina.base}/logs|%{gitblitlogdir}|g' $RPM_BUILD_ROOT%{gitblitdir}/conf/logging.properties

# gitblit webapp is ROOT.war (will respond to /)
cp %{SOURCE1}  $RPM_BUILD_ROOT%{gitblitwebappdir}/ROOT.war

# init.d
cp  %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}/%{gitblit}
sed -i 's|@@GITBLIT_APP@@|%{gitblit}|g' $RPM_BUILD_ROOT%{_initrddir}/%{gitblit}
sed -i 's|@@GITBLIT_USER@@|%{gitblitusername}|g' $RPM_BUILD_ROOT%{_initrddir}/%{gitblit}
sed -i 's|@@GITBLIT_VERSION@@|version %{version} release %{release}|g' $RPM_BUILD_ROOT%{_initrddir}/%{gitblit}
sed -i 's|@@GITBLIT_EXEC@@|%{gitblitexec}|g' $RPM_BUILD_ROOT%{_initrddir}/%{gitblit}

# sysconfig
cp  %{SOURCE3}  $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{gitblit}
sed -i 's|@@GITBLIT_APP@@|%{gitblit}|g' $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{gitblit}
sed -i 's|@@GITBLIT_APPDIR@@|%{gitblitdir}|g' $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{gitblit}
sed -i 's|@@GITBLIT_DATADIR@@|%{gitblitdatadir}|g' $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{gitblit}
sed -i 's|@@GITBLIT_LOGDIR@@|%{gitblitlogdir}|g' $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{gitblit}
sed -i 's|@@GITBLIT_USER@@|%{gitblitusername}|g' $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{gitblit}
sed -i 's|@@GITBLIT_CONFDIR@@|%{gitblitconfdir}|g' $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{gitblit}

# JMX (including JMX Remote)
cp %{SOURCE11} $RPM_BUILD_ROOT%{gitblitdir}/lib
cp %{SOURCE4}  $RPM_BUILD_ROOT%{gitblitconfdir}/jmxremote.access.skel
cp %{SOURCE5}  $RPM_BUILD_ROOT%{gitblitconfdir}/jmxremote.password.skel

# Our custom setenv.sh to get back env variables
cp  %{SOURCE6} $RPM_BUILD_ROOT%{gitblitdir}/bin/setenv.sh
sed -i 's|@@GITBLIT_APP@@|%{gitblit}|g' $RPM_BUILD_ROOT%{gitblitdir}/bin/setenv.sh

# Install logrotate
cp %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{gitblit}
sed -i 's|@@GITBLIT_LOGDIR@@|%{gitblitlogdir}|g' $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{gitblit}

# Install server.xml.skel
cp %{SOURCE8} $RPM_BUILD_ROOT%{gitblitconfdir}/server.xml.skel

# Setup user limits
cp %{SOURCE9} $RPM_BUILD_ROOT%{_sysconfdir}/security/limits.d/%{gitblit}.conf
sed -i 's|@@GITBLIT_USER@@|%{gitblitusername}|g' $RPM_BUILD_ROOT%{_sysconfdir}/security/limits.d/%{gitblit}.conf

# Setup Systemd
cp %{SOURCE10} $RPM_BUILD_ROOT%{_systemdir}/%{gitblit}.service
sed -i 's|@@GITBLIT_APP@@|%{gitblit}|g' $RPM_BUILD_ROOT%{_systemdir}/%{gitblit}.service
sed -i 's|@@GITBLIT_EXEC@@|%{gitblitexec}|g' $RPM_BUILD_ROOT%{_systemdir}/%{gitblit}.service

# Install context.xml (override previous one)
cp %{SOURCE12} $RPM_BUILD_ROOT%{gitblitconfdir}/context.xml
sed -i 's|@@GITBLIT_DATADIR@@|%{gitblitdatadir}|g' $RPM_BUILD_ROOT%{gitblitconfdir}/context.xml

# Install users.properties
cp %{SOURCE13} $RPM_BUILD_ROOT%{gitblitdatadir}/conf/users.conf

# remove uneeded file in RPM
rm -f $RPM_BUILD_ROOT%{gitblitdir}/*.sh
rm -f $RPM_BUILD_ROOT%{gitblitdir}/*.bat
rm -f $RPM_BUILD_ROOT%{gitblitdir}/bin/*.bat
rm -rf $RPM_BUILD_ROOT%{gitblitdir}/logs
rm -rf $RPM_BUILD_ROOT%{gitblitdir}/temp
rm -rf $RPM_BUILD_ROOT%{gitblitdir}/work

# ensure shell scripts are executable
chmod 755 $RPM_BUILD_ROOT%{gitblitdir}/bin/*.sh

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%if 0%{?suse_version} > 1140
%service_add_pre %{gitblit}.service
%endif
# First install time, add user and group
if [ "$1" == "1" ]; then
  %{_sbindir}/groupadd -r -g %{gitblitgroupid} %{gitblitusername} 2>/dev/null || :
  %{_sbindir}/useradd -s /sbin/nologin -c "%{gitblit} user" -g %{gitblitusername} -r -d %{gitblitdatadir} -u %{gitblituserid} %{gitblitusername} 2>/dev/null || :
else
# Update time, stop service if running
  if [ "$1" == "2" ]; then
    if [ -f %{_var}/run/%{gitblit}.pid ]; then
      %{_initrddir}/%{gitblit} stop
      touch %{gitblitdir}/logs/rpm-update-stop
    fi
  fi
fi

%post
%if 0%{?suse_version} > 1140
%service_add_post %{gitblit}.service
%endif
# First install time, register service, generate random passwords and start application
if [ "$1" == "1" ]; then
  # register app as service
  systemctl enable %{gitblit}.service >/dev/null 2>&1

  # Generated random password for RO and RW accounts
  RANDOMVAL=`echo $RANDOM | md5sum | sed "s| -||g" | tr -d " "`
  sed -i "s|@@GITBLIT_RO_PWD@@|$RANDOMVAL|g" %{_sysconfdir}/sysconfig/%{gitblit}
  RANDOMVAL=`echo $RANDOM | md5sum | sed "s| -||g" | tr -d " "`
  sed -i "s|@@GITBLIT_RW_PWD@@|$RANDOMVAL|g" %{_sysconfdir}/sysconfig/%{gitblit}

  pushd %{gitblitdir} >/dev/null
  ln -s %{gitblitlogdir}  logs
  ln -s %{gitblittempdir} temp
  ln -s %{gitblitworkdir} work
  popd >/dev/null

  # start application at first install (uncomment next line this behaviour not expected)
  # %{_initrddir}/%{name} start
else
  # Update time, restart application if it was running
  if [ "$1" == "2" ]; then
    if [ -f %{gitblitdir}/logs/rpm-update-stop ]; then
      # restart application after update (comment next line this behaviour not expected)
      %{_initrddir}/%{name} start
      rm -f %{gitblitdir}/logs/rpm-update-stop
    fi
  fi
fi

%preun
%if 0%{?suse_version} > 1140
%service_del_preun %{gitblit}.service
%endif
if [ "$1" == "0" ]; then
  # Uninstall time, stop service and cleanup

  # stop service
  %{_initrddir}/%{gitblit} stop

  # unregister app from services
  systemctl disable %{gitblit}.service >/dev/null 2>&1

  # finalize housekeeping
  rm -rf %{gitblitdir}
  rm -rf %{gitblitlogdir}
  rm -rf %{gitblittempdir}
  rm -rf %{gitblitworkdir}
fi

%postun
%if 0%{?suse_version} > 1140
%service_del_postun %{gitblit}.service
%endif

%files
%defattr(-,root,root)
%attr(0755,%{gitblitusername},%{gitblitusername}) %dir %{gitblitlogdir}
%attr(0755, root,root) %{_initrddir}/%{gitblit}
%attr(0644,root,root) %{_systemdir}/%{gitblit}.service
%config(noreplace) %{_sysconfdir}/sysconfig/%{gitblit}
%config %{_sysconfdir}/logrotate.d/%{gitblit}
%config %{_sysconfdir}/security/limits.d/%{gitblit}.conf
%{gitblitdir}/bin
%{gitblitdir}/conf
%{gitblitdir}/lib
%attr(-,%{gitblitusername}, %{gitblitusername}) %{gitblitdir}/webapps
%attr(0755,%{gitblitusername},%{gitblitusername}) %dir %{gitblitconflocaldir}
%attr(0755,%{gitblitusername},%{gitblitusername}) %dir %{gitblitdatadir}
%attr(0755,%{gitblitusername},%{gitblitusername}) %dir %{gitblitdatadir}/repos
%attr(0644,%{gitblitusername},%{gitblitusername}) %config(noreplace) %{gitblitdatadir}/conf/users.properties
%attr(0755,%{gitblitusername},%{gitblitusername}) %dir %{gitblittempdir}
%attr(0755,%{gitblitusername},%{gitblitusername}) %dir %{gitblitworkdir}
%doc %{gitblitdir}/NOTICE
%doc %{gitblitdir}/RUNNING.txt
%doc %{gitblitdir}/LICENSE
%doc %{gitblitdir}/RELEASE-NOTES

%changelog
* Fri Jan 6 2012 henri.gomez@gmail.com 1.0.0-2
- Create conf/Catalina/localhost with user rights

* Sat Dec 3 2011 henri.gomez@gmail.com 1.0.0-1
- Initial RPM