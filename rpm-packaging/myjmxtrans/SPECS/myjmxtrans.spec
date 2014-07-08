# Avoid unnecessary debug-information (native code)
%define		debug_package %{nil}

# Avoid CentOS 5/6 extras processes on contents (especially brp-java-repack-jars)
%define __os_install_post %{nil}

%ifos darwin
%define __portsed sed -i "" -e
%else
%define __portsed sed -i
%endif

%if 0%{?JMXTRANS_REL:1}
%define jmxtrans_rel        %{JMXTRANS_REL}
%else
%define jmxtrans_rel        243
%endif

%define myjmxtrans             myjmxtrans
%define myjmxtransusername     cijmxtra
%define myjmxtransuserid       1356
%define myjmxtransgroupid      1356

%define myjmxtransdir       /opt/%{myjmxtrans}
%define myjmxtransconfdir   %{myjmxtransdir}/conf
%define myjmxtransdatadir   %{_var}/lib/%{myjmxtrans}
%define myjmxtranslogdir    %{_var}/log/%{myjmxtrans}
%define myjmxtransexec      %{myjmxtransdir}/jmxtrans.sh
%define myjmxtranstempdir   %{_var}/run/%{myjmxtrans}
%define myjmxtransworkdir   %{_var}/spool/%{myjmxtrans}

%define _initrddir          %{_sysconfdir}/init.d
%define _systemdir          /lib/systemd/system

Name: myjmxtrans
Version: %{jmxtrans_rel}
Release: 1
Summary: JMX Transformer - more than meets the eye
Group: Applications/Communications
URL: https://github.com/jmxtrans/jmxtrans/
Vendor: Jon Stevens
Packager: Henri Gomez <henri.gomez@gmail.com>
License: OpenSource Software by Jon Stevens
BuildArch:  noarch

Source0: jmxtrans-v%{jmxtrans_rel}.tar.gz
Source1: initd.skel
Source2: sysconfig.skel
Source3: systemd.skel

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

Requires(pre):   /usr/sbin/groupadd
Requires(pre):   /usr/sbin/useradd

BuildRequires:  ant
BuildRequires:  java-devel

%if 0%{?suse_version} > 1000
BuildRequires:  java-devel >= 1.6.0
%endif

%if 0%{?fedora} || 0%{?rhel} || 0%{?centos}
BuildRequires:           java-devel >= 1:1.6.0
%endif

%define xuser       jmxtrans

%define _systemdir        /lib/systemd/system
%define _initrddir        %{_sysconfdir}/init.d

%description
jmxtrans is very powerful tool which reads json configuration files of servers/ports and jmx domains - attributes - types.
Then outputs the data in whatever format you want via special 'Writer' objects which you can code up yourself.
It does this with a very efficient engine design that will scale to querying thousands of machines.

%prep
%setup -q -n jmxtrans-%{jmxtrans_rel}

%build
ant clean dist -Dversion=%{jmxtrans_rel}

%install
# Prep the install location.
# Prep the install location.
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}%{_sysconfdir}/security/limits.d
mkdir -p %{buildroot}%{_systemdir}

mkdir -p %{buildroot}%{myjmxtransdir}
mkdir -p %{buildroot}%{myjmxtransdatadir}
mkdir -p %{buildroot}%{myjmxtranslogdir}
mkdir -p %{buildroot}%{myjmxtranstempdir}
mkdir -p %{buildroot}%{myjmxtransworkdir}

# remove source (unneeded here)
unzip target/jmxtrans-%{jmxtrans_rel}.zip
pushd jmxtrans-%{jmxtrans_rel}

rm -rf src/com
cp -rf * %{buildroot}%{myjmxtransdir}

# copy yaml2jmxtrans.py to bin
cp tools/yaml2jmxtrans.py %{buildroot}%{_bindir}
chmod 755 %{buildroot}%{_bindir}/yaml2jmxtrans.py

# copy doc
if [ -d doc ]; then
  cp -rf doc %{buildroot}%{myjmxtransdir}
else
  mkdir -p %{buildroot}%{myjmxtransdir}/doc
fi

popd

# ensure shell scripts are executable
chmod 755 %{buildroot}%{myjmxtransdir}/*.sh

# init.d
cp  %{SOURCE1} %{buildroot}%{_initrddir}/%{myjmxtrans}
%{__portsed} 's|@@SKEL_APP@@|%{myjmxtrans}|g' %{buildroot}%{_initrddir}/%{myjmxtrans}
%{__portsed} 's|@@SKEL_USER@@|%{myjmxtransusername}|g' %{buildroot}%{_initrddir}/%{myjmxtrans}
%{__portsed} 's|@@SKEL_VERSION@@|version %{version} release %{release}|g' %{buildroot}%{_initrddir}/%{myjmxtrans}
%{__portsed} 's|@@SKEL_EXEC@@|%{myjmxtransexec}|g' %{buildroot}%{_initrddir}/%{myjmxtrans}
%{__portsed} 's|@@SKEL_DATADIR@@|%{myjmxtransdatadir}|g' %{buildroot}%{_initrddir}/%{myjmxtrans}
%{__portsed} 's|@@SKEL_LOGDIR@@|%{myjmxtranslogdir}|g' %{buildroot}%{_initrddir}/%{myjmxtrans}
%{__portsed} 's|@@SKEL_TMPDIR@@|%{myjmxtranstempdir}|g' %{buildroot}%{_initrddir}/%{myjmxtrans}

# sysconfig
cp  %{SOURCE2}  %{buildroot}%{_sysconfdir}/sysconfig/%{myjmxtrans}
%{__portsed} 's|@@SKEL_APP@@|%{myjmxtrans}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{myjmxtrans}
%{__portsed} 's|@@SKEL_APPDIR@@|%{myjmxtransdir}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{myjmxtrans}
%{__portsed} 's|@@SKEL_DATADIR@@|%{myjmxtransdatadir}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{myjmxtrans}
%{__portsed} 's|@@SKEL_LOGDIR@@|%{myjmxtranslogdir}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{myjmxtrans}
%{__portsed} 's|@@SKEL_USER@@|%{myjmxtransusername}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{myjmxtrans}
%{__portsed} 's|@@SKEL_CONFDIR@@|%{myjmxtransconfdir}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{myjmxtrans}

# Setup Systemd
mkdir -p %{buildroot}%{_systemdir}
cp %{SOURCE3} %{buildroot}%{_systemdir}/%{myjmxtrans}.service
%{__portsed} 's|@@SKEL_APP@@|%{myjmxtrans}|g' %{buildroot}%{_systemdir}/%{myjmxtrans}.service
%{__portsed} 's|@@SKEL_EXEC@@|%{myjmxtransexec}|g' %{buildroot}%{_systemdir}/%{myjmxtrans}.service

# Use correct sysconfig file in control script
%{__portsed} 's|/etc/sysconfig/jmxtrans|%{_sysconfdir}/sysconfig/%{myjmxtrans}|g' %{buildroot}%{myjmxtransexec}

%clean
rm -rf %{buildroot}

%pre
%if 0%{?suse_version} > 1140
%service_add_pre %{myjmxtrans}.service
%endif
# First install time, add user and group
if [ "$1" == "1" ]; then
  %{_sbindir}/groupadd -r -g %{myjmxtransgroupid} %{myjmxtransusername} 2>/dev/null || :
  %{_sbindir}/useradd -s /sbin/nologin -c "%{myjmxtrans} user" -g %{myjmxtransusername} -r -d %{myjmxtransdatadir} -u %{myjmxtransuserid} %{myjmxtransusername} 2>/dev/null || :
fi

%post
%if 0%{?suse_version} > 1140
%service_add_post %{myjmxtrans}.service
%endif
%if 0%{?suse_version} > 1000
%fillup_only -n %{appname}
%endif

if [ $1 = 1 ]; then

  # register app as service
  systemctl enable %{myjmxtrans}.service >/dev/null 2>&1

%if 0%{?fedora} || 0%{?rhel} || 0%{?centos}
  chkconfig %{myjmxtrans} on
%endif

fi

%preun
%if 0%{?suse_version} > 1140
%service_del_preun %{myjmxtrans}.service
%endif
if [ "$1" == "0" ]; then
  # Uninstall time, stop service and cleanup

  # stop service
  %{_initrddir}/%{myjmxtrans} stop

  # unregister app from services
  systemctl disable %{myjmxtrans}.service >/dev/null 2>&1

%if 0%{?fedora} || 0%{?rhel} || 0%{?centos}
  chkconfig %{myjmxtrans} off
%endif

  # finalize housekeeping
  rm -rf %{myjmxtransdir}
  rm -rf %{myjmxtranslogdir}
  rm -rf %{myjmxtranstempdir}
  rm -rf %{myjmxtransworkdir}
  # remove datadir contents (full housekeeping so)
  rm -rf %{myjmxtransdatadir}

fi

%postun
%if 0%{?suse_version} > 1140
%service_del_postun %{myjmxtrans}.service
%endif

%files
%defattr(-,root,root)
%{_bindir}
%{myjmxtransdir}
%exclude                                                     %{myjmxtransdir}/README.html
%exclude                                                     %{myjmxtransdir}/doc
%attr(0755,root,root)                                        %{_initrddir}/%{myjmxtrans}
%attr(0644,root,root)                                        %{_systemdir}/%{myjmxtrans}.service
%config(noreplace)                                           %{_sysconfdir}/sysconfig/%{myjmxtrans}
%attr(0755,%{myjmxtransusername},%{myjmxtransusername}) %dir %{myjmxtransdatadir}
%attr(0755,%{myjmxtransusername},%{myjmxtransusername}) %dir %{myjmxtranslogdir}
%attr(0755,%{myjmxtransusername},%{myjmxtransusername}) %dir %{myjmxtranstempdir}
%attr(0755,%{myjmxtransusername},%{myjmxtransusername}) %dir %{myjmxtransworkdir}
%doc %{myjmxtransdir}/README.html
%doc %{myjmxtransdir}/doc


%changelog
* Tue Jul 8 2014 Henri Gomez <henri.gomez@gmail.com> - 243-1
- Update to latest changes, including Librato Writer

* Fri Mar 29 2013 Henri Gomez <henri.gomez@gmail.com> - 242-1
- Initial RPM
