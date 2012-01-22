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

%define myapp             mygitblit
%define myappusername     mygitblit
%define myappuserid       1238
%define myappgroupid      1238

%define myappdir          /opt/%{myapp}
%define myappdatadir      %{_var}/lib/%{myapp}
%define myapplogdir       %{_var}/log/%{myapp}
%define myappexec         %{myappdir}/bin/catalina.sh
%define myappconfdir      %{myappdir}/conf
%define myappconflocaldir %{myappdir}/conf/Catalina/localhost
%define myappwebappdir    %{myappdir}/webapps
%define myapptempdir      /tmp/%{myapp}
%define myappworkdir      %{_var}/%{myapp}

%define _systemdir        /lib/systemd/system
%define _initrddir        %{_sysconfdir}/init.d

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
Source2: myapp-initd
Source3: myapp-sysconfig
Source4: myapp-jmxremote.access.skel
Source5: myapp-jmxremote.password.skel
Source6: myapp-setenv.sh
Source7: myapp-logrotate
Source8: myapp-server.xml.skel
Source9: myapp-limits.conf
Source10: myapp-systemd
Source11: catalina-jmx-remote-%{tomcat_rel}.jar
Source12: myapp-context.xml
#Source13: myapp-users.properties
Source13: myapp-users.conf


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

mkdir -p $RPM_BUILD_ROOT%{myappdir}
mkdir -p $RPM_BUILD_ROOT%{myappdatadir}
mkdir -p $RPM_BUILD_ROOT%{myappdatadir}/conf
mkdir -p $RPM_BUILD_ROOT%{myappdatadir}/repos

mkdir -p $RPM_BUILD_ROOT%{myapplogdir}
mkdir -p $RPM_BUILD_ROOT%{myapptempdir}
mkdir -p $RPM_BUILD_ROOT%{myappworkdir}
mkdir -p $RPM_BUILD_ROOT%{myappwebappdir}

# Copy tomcat
mv apache-tomcat-%{tomcat_rel}/* $RPM_BUILD_ROOT%{myappdir}

# Create conf/Catalina/localhost
mkdir -p $RPM_BUILD_ROOT%{myappconflocaldir}

# remove default webapps
rm -rf $RPM_BUILD_ROOT%{myappdir}/webapps/*

# patches to have logs under /var/log/myapp
sed -i 's|\${catalina.base}/logs|%{myapplogdir}|g' $RPM_BUILD_ROOT%{myappdir}/conf/logging.properties

# myapp webapp is ROOT.war (will respond to /)
cp %{SOURCE1}  $RPM_BUILD_ROOT%{myappwebappdir}/ROOT.war

# init.d
cp  %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}/%{myapp}
sed -i 's|@@SKEL_APP@@|%{myapp}|g' $RPM_BUILD_ROOT%{_initrddir}/%{myapp}
sed -i 's|@@SKEL_USER@@|%{myappusername}|g' $RPM_BUILD_ROOT%{_initrddir}/%{myapp}
sed -i 's|@@SKEL_VERSION@@|version %{version} release %{release}|g' $RPM_BUILD_ROOT%{_initrddir}/%{myapp}
sed -i 's|@@SKEL_EXEC@@|%{myappexec}|g' $RPM_BUILD_ROOT%{_initrddir}/%{myapp}

# sysconfig
cp  %{SOURCE3}  $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{myapp}
sed -i 's|@@SKEL_APP@@|%{myapp}|g' $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{myapp}
sed -i 's|@@SKEL_APPDIR@@|%{myappdir}|g' $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{myapp}
sed -i 's|@@SKEL_DATADIR@@|%{myappdatadir}|g' $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{myapp}
sed -i 's|@@SKEL_LOGDIR@@|%{myapplogdir}|g' $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{myapp}
sed -i 's|@@SKEL_USER@@|%{myappusername}|g' $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{myapp}
sed -i 's|@@SKEL_CONFDIR@@|%{myappconfdir}|g' $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{myapp}

# JMX (including JMX Remote)
cp %{SOURCE11} $RPM_BUILD_ROOT%{myappdir}/lib
cp %{SOURCE4}  $RPM_BUILD_ROOT%{myappconfdir}/jmxremote.access.skel
cp %{SOURCE5}  $RPM_BUILD_ROOT%{myappconfdir}/jmxremote.password.skel

# Our custom setenv.sh to get back env variables
cp  %{SOURCE6} $RPM_BUILD_ROOT%{myappdir}/bin/setenv.sh
sed -i 's|@@SKEL_APP@@|%{myapp}|g' $RPM_BUILD_ROOT%{myappdir}/bin/setenv.sh

# Install logrotate
cp %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{myapp}
sed -i 's|@@SKEL_LOGDIR@@|%{myapplogdir}|g' $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{myapp}

# Install server.xml.skel
cp %{SOURCE8} $RPM_BUILD_ROOT%{myappconfdir}/server.xml.skel

# Setup user limits
cp %{SOURCE9} $RPM_BUILD_ROOT%{_sysconfdir}/security/limits.d/%{myapp}.conf
sed -i 's|@@SKEL_USER@@|%{myappusername}|g' $RPM_BUILD_ROOT%{_sysconfdir}/security/limits.d/%{myapp}.conf

# Setup Systemd
cp %{SOURCE10} $RPM_BUILD_ROOT%{_systemdir}/%{myapp}.service
sed -i 's|@@SKEL_APP@@|%{myapp}|g' $RPM_BUILD_ROOT%{_systemdir}/%{myapp}.service
sed -i 's|@@SKEL_EXEC@@|%{myappexec}|g' $RPM_BUILD_ROOT%{_systemdir}/%{myapp}.service

# Install context.xml (override previous one)
cp %{SOURCE12} $RPM_BUILD_ROOT%{myappconfdir}/context.xml
sed -i 's|@@SKEL_DATADIR@@|%{myappdatadir}|g' $RPM_BUILD_ROOT%{myappconfdir}/context.xml

# Install users.properties
cp %{SOURCE13} $RPM_BUILD_ROOT%{myappdatadir}/conf/users.conf

# remove uneeded file in RPM
rm -f $RPM_BUILD_ROOT%{myappdir}/*.sh
rm -f $RPM_BUILD_ROOT%{myappdir}/*.bat
rm -f $RPM_BUILD_ROOT%{myappdir}/bin/*.bat
rm -rf $RPM_BUILD_ROOT%{myappdir}/logs
rm -rf $RPM_BUILD_ROOT%{myappdir}/temp
rm -rf $RPM_BUILD_ROOT%{myappdir}/work

# ensure shell scripts are executable
chmod 755 $RPM_BUILD_ROOT%{myappdir}/bin/*.sh

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%if 0%{?suse_version} > 1140
%service_add_pre %{myapp}.service
%endif
# First install time, add user and group
if [ "$1" == "1" ]; then
  %{_sbindir}/groupadd -r -g %{myappgroupid} %{myappusername} 2>/dev/null || :
  %{_sbindir}/useradd -s /sbin/nologin -c "%{myapp} user" -g %{myappusername} -r -d %{myappdatadir} -u %{myappuserid} %{myappusername} 2>/dev/null || :
else
# Update time, stop service if running
  if [ "$1" == "2" ]; then
    if [ -f %{_var}/run/%{myapp}.pid ]; then
      %{_initrddir}/%{myapp} stop
      touch %{myappdir}/logs/rpm-update-stop
    fi
  fi
fi

%post
%if 0%{?suse_version} > 1140
%service_add_post %{myapp}.service
%endif
# First install time, register service, generate random passwords and start application
if [ "$1" == "1" ]; then
  # register app as service
  systemctl enable %{myapp}.service >/dev/null 2>&1

  # Generated random password for RO and RW accounts
  RANDOMVAL=`echo $RANDOM | md5sum | sed "s| -||g" | tr -d " "`
  sed -i "s|@@SKEL_RO_PWD@@|$RANDOMVAL|g" %{_sysconfdir}/sysconfig/%{myapp}
  RANDOMVAL=`echo $RANDOM | md5sum | sed "s| -||g" | tr -d " "`
  sed -i "s|@@SKEL_RW_PWD@@|$RANDOMVAL|g" %{_sysconfdir}/sysconfig/%{myapp}

  pushd %{myappdir} >/dev/null
  ln -s %{myapplogdir}  logs
  ln -s %{myapptempdir} temp
  ln -s %{myappworkdir} work
  popd >/dev/null

  # start application at first install (uncomment next line this behaviour not expected)
  # %{_initrddir}/%{name} start
else
  # Update time, restart application if it was running
  if [ "$1" == "2" ]; then
    if [ -f %{myappdir}/logs/rpm-update-stop ]; then
      # restart application after update (comment next line this behaviour not expected)
      %{_initrddir}/%{name} start
      rm -f %{myappdir}/logs/rpm-update-stop
    fi
  fi
fi

%preun
%if 0%{?suse_version} > 1140
%service_del_preun %{myapp}.service
%endif
if [ "$1" == "0" ]; then
  # Uninstall time, stop service and cleanup

  # stop service
  %{_initrddir}/%{myapp} stop

  # unregister app from services
  systemctl disable %{myapp}.service >/dev/null 2>&1

  # finalize housekeeping
  rm -rf %{myappdir}
  rm -rf %{myapplogdir}
  rm -rf %{myapptempdir}
  rm -rf %{myappworkdir}
fi

%postun
%if 0%{?suse_version} > 1140
%service_del_postun %{myapp}.service
%endif

%files
%defattr(-,root,root)
%attr(0755,%{myappusername},%{myappusername}) %dir %{myapplogdir}
%attr(0755, root,root) %{_initrddir}/%{myapp}
%attr(0644,root,root) %{_systemdir}/%{myapp}.service
%config(noreplace) %{_sysconfdir}/sysconfig/%{myapp}
%config %{_sysconfdir}/logrotate.d/%{myapp}
%config %{_sysconfdir}/security/limits.d/%{myapp}.conf
%{myappdir}/bin
%{myappdir}/conf
%{myappdir}/lib
%attr(-,%{myappusername}, %{myappusername}) %{myappdir}/webapps
%attr(0755,%{myappusername},%{myappusername}) %dir %{myappconflocaldir}
%attr(0755,%{myappusername},%{myappusername}) %dir %{myappdatadir}
%attr(0755,%{myappusername},%{myappusername}) %dir %{myappdatadir}/repos
%attr(0644,%{myappusername},%{myappusername}) %config(noreplace) %{myappdatadir}/conf/users.properties
%attr(0755,%{myappusername},%{myappusername}) %dir %{myapptempdir}
%attr(0755,%{myappusername},%{myappusername}) %dir %{myappworkdir}
%doc %{myappdir}/NOTICE
%doc %{myappdir}/RUNNING.txt
%doc %{myappdir}/LICENSE
%doc %{myappdir}/RELEASE-NOTES

%changelog
* Fri Jan 6 2012 henri.gomez@gmail.com 1.0.0-2
- Create conf/Catalina/localhost with user rights

* Sat Dec 3 2011 henri.gomez@gmail.com 1.0.0-1
- Initial RPM