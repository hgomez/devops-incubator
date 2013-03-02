#
# Due to its Python nature, there could be only a site installation for carbon
# So we just set package name to mycarbon and stick with FHS rules and Graphite suite usage (/var/lib/graphite, /etc/graphite, ...)
#

# Avoid unnecessary debug-information (native code)
%define		debug_package %{nil}

%ifos darwin
%define __portsed sed -i "" -e
%else
%define __portsed sed -i
%endif

%if 0%{?CARBON_REL:1}
%define carbon_rel        %{CARBON_REL}
%else
%define carbon_rel        0.9.10
%endif

%define carbonusername     mycarbon
%define carbonuserid       1300
%define carbongroupid      1300

%define carbonconfdir      %{_sysconfdir}/graphite/carbon
%define carbonlogdir       %{_var}/log/graphite/carbon
%define carbonrundir       %{_var}/run/graphite
%define graphiteroot	   %{_sysconfdir}/graphite
%define storagedir         %{_var}/lib/graphite/storage
%define whisperdir         %{storagedir}/whisper
%define rrddir             %{storagedir}/rrd

%define _systemdir        /lib/systemd/system
%define _initrddir        %{_sysconfdir}/init.d

# norootforbuild
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%define py_ver %(python -c 'import sys;print(sys.version[0:3])')

Name:           mycarbon
Version:        %{carbon_rel}
Release:        1

License:        Apache-2.0
Group:          Productivity/Networking/Security

Requires:       python >= 2.4
Requires:       python-Twisted

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python-devel >= 2.4

Url:            http://graphite.wikidot.com/
Source:         carbon-%{carbon_rel}.tar.gz
Source1:        initd.skel
Source2:        logrotate.skel
Source3:        systemd.skel
Source4:        limits.conf.skel
Source5:        carbon.conf.skel
Source6:        storage-schemas.conf
Source7:        storage-aggregation.conf

Patch:          carbon-%{carbon_rel}.patch

Summary:        Backend data caching and persistence daemon for Graphite
%description
Backend data caching and persistence daemon for Graphite.

%prep
%setup -n carbon-%{carbon_rel}
%patch

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}
install -d -m 0755 %{buildroot}%{_sysconfdir}/graphite/
mv %{buildroot}%{_prefix}/conf/ %{buildroot}%{carbonconfdir}

#
# RPM specifics
# 

install -d -m 0755 %{buildroot}%{carbonlogdir}
install -d -m 0755 %{buildroot}%{rrddir}
install -d -m 0755 %{buildroot}%{whisperdir}

# init.d
install -d -m 0755 %{buildroot}%{_initrddir}
cp  %{SOURCE1} %{buildroot}%{_initrddir}/carbon
%{__portsed} 's|@@SKEL_APP@@|carbon|g' %{buildroot}%{_initrddir}/carbon
%{__portsed} 's|@@SKEL_USER@@|%{carbonusername}|g' %{buildroot}%{_initrddir}/carbon
%{__portsed} 's|@@SKEL_VERSION@@|version %{version} release %{release}|g' %{buildroot}%{_initrddir}/carbon
%{__portsed} 's|@@SKEL_EXEC@@|%{carbonexec}|g' %{buildroot}%{_initrddir}/carbon
%{__portsed} 's|@@SKEL_CONFDIR@@|%{carbonconfdir}|g' %{buildroot}%{_initrddir}/carbon

# Install logrotate
install -d -m 0755 %{buildroot}%{_sysconfdir}/logrotate.d
cp %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/carbon
%{__portsed} 's|@@SKEL_LOGDIR@@|%{carbonlogdir}|g' %{buildroot}%{_sysconfdir}/logrotate.d/carbon

# Setup Systemd
%ifos linux
install -d -m 0755 %{buildroot}%{_systemdir}
cp %{SOURCE3} %{buildroot}%{_systemdir}/carbon.service
%{__portsed} 's|@@SKEL_APP@@|carbon|g' %{buildroot}%{_systemdir}/carbon.service
%{__portsed} 's|@@SKEL_EXEC@@|%{carbonexec}|g' %{buildroot}%{_systemdir}/carbon.service
%endif

# Setup user limits
install -d -m 0755 %{buildroot}%{_sysconfdir}/security/limits.d
cp %{SOURCE4} %{buildroot}%{_sysconfdir}/security/limits.d/carbon.conf
%{__portsed} 's|@@SKEL_USER@@|%{carbonusername}|g' %{buildroot}%{_sysconfdir}/security/limits.d/carbon.conf

# Setup carbon.conf
install -d -m 0755 %{buildroot}%{carbonconfdir}
cp %{SOURCE5} %{buildroot}%{carbonconfdir}/carbon.conf
%{__portsed} 's|@@SKEL_USER@@|%{carbonusername}|g' %{buildroot}%{carbonconfdir}/carbon.conf
%{__portsed} 's|@@SKEL_CONFDIR@@|%{carbonconfdir}|g' %{buildroot}%{carbonconfdir}/carbon.conf
%{__portsed} 's|@@SKEL_WHISPERDIR@@|%{whisperdir}|g' %{buildroot}%{carbonconfdir}/carbon.conf
%{__portsed} 's|@@SKEL_LOGDIR@@|%{carbonlogdir}|g' %{buildroot}%{carbonconfdir}/carbon.conf
%{__portsed} 's|@@SKEL_RUNDIR@@|%{carbonrundir}|g' %{buildroot}%{carbonconfdir}/carbon.conf

# Rundir (PID)
install -d -m 0755 %{buildroot}%{carbonrundir}

# Add default confs
mv %{SOURCE6} %{buildroot}%{carbonconfdir}/storage-schemas.conf
mv %{SOURCE7} %{buildroot}%{carbonconfdir}/storage-aggregation.conf

%clean
%{__rm} -rf %{buildroot}

%pre
%if 0%{?suse_version} > 1140
%service_add_pre carbon.service
%endif
# First install time, add user and group
if [ "$1" == "1" ]; then
  %{_sbindir}/groupadd -r -g %{carbongroupid} %{carbonusername} 2>/dev/null || :
  %{_sbindir}/useradd -s /sbin/nologin -c "carbon user" -g %{carbonusername} -r -d %{whisperdir} -u %{carbonuserid} %{carbonusername} 2>/dev/null || :
else
# Update time, stop service if running
  if [ "$1" == "2" ]; then
    if [ -f %{_var}/run/carbon.pid ]; then
      %{_initrddir}/carbon stop
      touch %{carbonlogdir}/rpm-update-stop
    fi
  fi
fi


%post
%if 0%{?suse_version} > 1140
%service_add_post carbon.service
%endif
# First install time, register service, generate random passwords and start application
if [ "$1" == "1" ]; then
  # register app as service
  systemctl enable carbon.service >/dev/null 2>&1

%if 0%{?fedora} || 0%{?rhel} || 0%{?centos}
  chkconfig carbon on
%endif

  # start application at first install (uncomment next line this behaviour not expected)
  # %{_initrddir}/carbon start
else
  # Update time, restart application if it was running
  if [ "$1" == "2" ]; then
    if [ -f %{carbonlogdir}/rpm-update-stop ]; then
      # restart application after update (comment next line this behaviour not expected)
      %{_initrddir}/carbon start
      rm -f %{carbonlogdir}/rpm-update-stop
    fi
  fi
fi

%preun
%if 0%{?suse_version} > 1140
%service_del_preun carbon.service
%endif
if [ "$1" == "0" ]; then
  # Uninstall time, stop service and cleanup

  # stop service
  %{_initrddir}/carbon stop

  # unregister app from services
  systemctl disable carbon.service >/dev/null 2>&1

%if 0%{?fedora} || 0%{?rhel} || 0%{?centos}
  chkconfig carbon off
%endif

  # finalize housekeeping
  rm -rf %{carbonlogdir}

  # dont remove datadir contents since whisper could use it
  # rm -rf %{whisperdir}
fi

%postun
%if 0%{?suse_version} > 1140
%service_del_postun carbon.service
%endif
 

%files
%defattr(-,root,root,-)
%doc LICENSE
%dir %{_sysconfdir}/graphite/
# example files could be updated but .conf should be conserved
%config %{_sysconfdir}/graphite/carbon/*.example
%config(noreplace) %{_sysconfdir}/graphite/carbon/*.conf
%config %{_sysconfdir}/logrotate.d/carbon
%config %{_sysconfdir}/security/limits.d/carbon.conf

%{_bindir}

%if 0%{?rhel} != 5
%{python_sitelib}/carbon-%{version}-py%{py_ver}.egg-info
%endif

%{python_sitelib}/carbon/
%dir %{python_sitelib}/twisted/
%dir %{python_sitelib}/twisted/plugins/
%{python_sitelib}/twisted/plugins/carbon*

%attr(0777,root,root) %dir %{storagedir}
%attr(0755,%{carbonusername},%{carbonusername}) %dir %{whisperdir}
%attr(0755,%{carbonusername},%{carbonusername}) %dir %{rrddir}
%attr(0755,%{carbonusername},%{carbonusername}) %dir %{carbonlogdir}
%attr(0755,%{carbonusername},%{carbonusername}) %dir %{carbonrundir}

%attr(0755, root,root) %{_initrddir}/carbon
%ifos linux
%attr(0644,root,root) %{_systemdir}/carbon.service
%endif

%changelog
* Fri Feb 22 2013 henri.gomez@gmail.com 0.9.10-1
- initial package (v0.9.10)
