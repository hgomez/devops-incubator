Name: jstatd-daemon
Version: %{VERSION}
Release: 3
Summary: A configurable rc.d daemon for jstatd.
Group: Development/Tools
URL: http://docs.oracle.com/javase/6/docs/technotes/tools/share/jstatd.html
Packager: Julien Nicoulaud <julien.nicoulaud@gmail.com>
License: BSD
BuildArch:  noarch

%define service_name jstatd

BuildRoot: %{_tmppath}/build-%{name}-%{version}-%{release}

%if 0%{?suse_version}
Requires:           java = 1.6.0
%endif

%if 0%{?fedora} || 0%{?rhel} || 0%{?centos}
Requires:           java = 1:1.6.0
%endif

Source0: initd.skel
Source1: sysconfig.skel
Source2: jstatd.all.policy

%description
A configurable rc.d daemon for jstatd.

%prep
%setup -q -c -T

%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/init.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/jstatd

cp  %{SOURCE0} $RPM_BUILD_ROOT%{_sysconfdir}/init.d/%{service_name}
sed -i 's|@@SKEL_APP@@|%{service_name}|g' $RPM_BUILD_ROOT%{_sysconfdir}/init.d/%{service_name}

cp  %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{service_name}
sed -i 's|@@SKEL_APP@@|%{service_name}|g' $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{service_name}

cp  %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/%{service_name}/all.policy

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%if 0%{?suse_version} > 1140
%service_add_pre %{service_name}.service
%endif

%post
%if 0%{?suse_version} > 1140
%service_add_post %{service_name}.service
%endif
# First install time, register service, generate random passwords and start application
if [ "$1" == "1" ]; then
  # register app as service
  systemctl enable %{service_name}.service >/dev/null 2>&1
fi

%preun
%if 0%{?suse_version} > 1140
%service_del_preun %{service_name}.service
%endif
if [ "$1" == "0" ]; then
  # Uninstall time, stop service and cleanup

  # stop service
  %{_initrddir}/%{service_name} stop

  # unregister app from services
  systemctl disable %{service_name}.service >/dev/null 2>&1
fi

%postun
%if 0%{?suse_version} > 1140
%service_del_postun %{service_name}.service
%endif

%files
%defattr(-,root,root)
%attr(0755,root,root) %{_sysconfdir}/init.d/%{service_name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{service_name}
%attr(0644,root,root) %{_sysconfdir}/%{service_name}/all.policy

%changelog
* Wed Mar 7 2012 henri.gomez@gmail.com 1.0.0-3
- Distribution dependant Requires for Java

* Tue Mar 6 2012 henri.gomez@gmail.com 1.0.0-2
- Rework for Suse/OpenSuse compatiblity

* Sun Mar 4 2012 julien.nicoulaud@gmail.com 1.0.0-1
- Initial RPM

