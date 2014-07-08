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

%define appname      myjmxtrans
%define appusername  myjmxtra
%define appuserid    1356
%define appgroupid   1356

%define appdir       /opt/%{appname}
%define appconfdir   %{appdir}/conf
%define appdatadir   %{_var}/lib/%{appname}
%define applogdir    %{_var}/log/%{appname}
%define appexec      %{appdir}/jmxtrans.sh
%define apptempdir   %{_var}/run/%{appname}
%define appworkdir   %{_var}/spool/%{appname}

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

BuildRequires:  ant >= 1.7
BuildRequires:  java-devel

%if 0%{?suse_version} > 1010
BuildRequires:  java-devel >= 1.6.0
else
BuildRequires:  java-devel >= 1.5.0
%endif

BuildRequires: unzip

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

mkdir -p %{buildroot}%{appdir}
mkdir -p %{buildroot}%{appdatadir}
mkdir -p %{buildroot}%{applogdir}
mkdir -p %{buildroot}%{apptempdir}
mkdir -p %{buildroot}%{appworkdir}

# remove source (unneeded here)
unzip target/jmxtrans-%{jmxtrans_rel}.zip
pushd jmxtrans-%{jmxtrans_rel}

rm -rf src
rm -rf javadoc
cp -rf * %{buildroot}%{appdir}

# copy yaml2jmxtrans.py to bin
cp tools/yaml2jmxtrans.py %{buildroot}%{_bindir}
chmod 755 %{buildroot}%{_bindir}/yaml2jmxtrans.py

# copy doc
if [ -d doc ]; then
  cp -rf doc %{buildroot}%{appdir}
else
  mkdir -p %{buildroot}%{appdir}/doc
fi

popd

# ensure shell scripts are executable
chmod 755 %{buildroot}%{appdir}/*.sh
chmod 755 %{buildroot}%{appdir}/tools/yaml2jmxtrans.py
chmod 755 %{buildroot}%{appdir}/tools/setup-vm.sh

# init.d
cp  %{SOURCE1} %{buildroot}%{_initrddir}/%{appname}
%{__portsed} 's|@@SKEL_APP@@|%{appname}|g' %{buildroot}%{_initrddir}/%{appname}
%{__portsed} 's|@@SKEL_USER@@|%{appusername}|g' %{buildroot}%{_initrddir}/%{appname}
%{__portsed} 's|@@SKEL_VERSION@@|version %{version} release %{release}|g' %{buildroot}%{_initrddir}/%{appname}
%{__portsed} 's|@@SKEL_EXEC@@|%{appexec}|g' %{buildroot}%{_initrddir}/%{appname}
%{__portsed} 's|@@SKEL_DATADIR@@|%{appdatadir}|g' %{buildroot}%{_initrddir}/%{appname}
%{__portsed} 's|@@SKEL_LOGDIR@@|%{applogdir}|g' %{buildroot}%{_initrddir}/%{appname}
%{__portsed} 's|@@SKEL_TMPDIR@@|%{apptempdir}|g' %{buildroot}%{_initrddir}/%{appname}

# sysconfig
cp  %{SOURCE2}  %{buildroot}%{_sysconfdir}/sysconfig/%{appname}
%{__portsed} 's|@@SKEL_APP@@|%{appname}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{appname}
%{__portsed} 's|@@SKEL_APPDIR@@|%{appdir}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{appname}
%{__portsed} 's|@@SKEL_DATADIR@@|%{appdatadir}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{appname}
%{__portsed} 's|@@SKEL_LOGDIR@@|%{applogdir}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{appname}
%{__portsed} 's|@@SKEL_USER@@|%{appusername}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{appname}
%{__portsed} 's|@@SKEL_CONFDIR@@|%{appconfdir}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{appname}

%if 0%{?suse_version} > 1000
mkdir -p %{buildroot}%{_var}/adm/fillup-templates
mv %{buildroot}%{_sysconfdir}/sysconfig/%{appname} %{buildroot}%{_var}/adm/fillup-templates/sysconfig.%{appname}
%endif

# Setup Systemd
mkdir -p %{buildroot}%{_systemdir}
cp %{SOURCE3} %{buildroot}%{_systemdir}/%{appname}.service
%{__portsed} 's|@@SKEL_APP@@|%{appname}|g' %{buildroot}%{_systemdir}/%{appname}.service
%{__portsed} 's|@@SKEL_EXEC@@|%{appexec}|g' %{buildroot}%{_systemdir}/%{appname}.service

# Use correct sysconfig file in control script
%{__portsed} 's|/etc/sysconfig/jmxtrans|%{_sysconfdir}/sysconfig/%{appname}|g' %{buildroot}%{appexec}

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
  fi
fi

%post
%if 0%{?suse_version} > 1140
%service_add_post %{appname}.service
%endif
%if 0%{?suse_version} > 1000
%fillup_only -n %{appname}
%endif

if [ $1 = 1 ]; then

  # register app as service
  systemctl enable %{appname}.service >/dev/null 2>&1

%if 0%{?fedora} || 0%{?rhel} || 0%{?centos}
  chkconfig %{appname} on
%endif

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
  # remove datadir contents (full housekeeping so)
  rm -rf %{appdatadir}

fi

%postun
%if 0%{?suse_version} > 1140
%service_del_postun %{appname}.service
%endif

%files
%defattr(-,root,root)
%dir %{appdir}
%{appdir}/lib
%{appdir}/tools
%{appdir}/*.jar
%{appdir}/*.json
%{appdir}/*.sh
%{appdir}/*.xml

%{_bindir}
%exclude                                       %{appdir}/README.html
%exclude                                       %{appdir}/doc
%attr(0755,root,root)                          %{_initrddir}/%{appname}
%attr(0644,root,root)                          %{_systemdir}/%{appname}.service
%if 0%{?suse_version} > 1000
%{_var}/adm/fillup-templates/sysconfig.%{appname}
%else
%dir %{_sysconfdir}/sysconfig
%config(noreplace) %{_sysconfdir}/sysconfig/%{appname}
%endif
%attr(0755,%{appusername},%{appusername}) %dir %{appdatadir}
%attr(0755,%{appusername},%{appusername}) %dir %{applogdir}
%ghost %{apptempdir}
%attr(0755,%{appusername},%{appusername}) %dir %{appworkdir}
%doc %{appdir}/README.html
%doc %{appdir}/doc


%changelog
* Tue Jul 8 2014 Henri Gomez <henri.gomez@gmail.com> - 243-1
- Update to latest changes, including Librato Writer

* Fri Mar 29 2013 Henri Gomez <henri.gomez@gmail.com> - 242-1
- Initial RPM
