Name: jstatd
Version: %{VERSION}
Release: 1
Summary: A configurable rc.d daemon for jstatd.
Group: Development/Tools
URL: http://docs.oracle.com/javase/6/docs/technotes/tools/share/jstatd.html
Packager: Julien Nicoulaud <julien.nicoulaud@gmail.com>
License: BSD
BuildArch:  noarch

BuildRoot: %{_tmppath}/build-%{name}-%{version}-%{release}

#Requires: jdk
Requires:           java = 1.6.0

Source0: jstatd.initd
Source1: jstatd.sysconfig
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

cp  %{SOURCE0} $RPM_BUILD_ROOT%{_sysconfdir}/init.d/jstatd
cp  %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/jstatd
cp  %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/jstatd/all.policy

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%if 0%{?suse_version} > 1140
%service_add_pre %{name}.service
%endif

%post
%if 0%{?suse_version} > 1140
%service_add_post %{name}.service
%endif
# First install time, register service, generate random passwords and start application
if [ "$1" == "1" ]; then
  # register app as service
  systemctl enable %{name}.service >/dev/null 2>&1
fi

%preun
%if 0%{?suse_version} > 1140
%service_del_preun %{name}.service
%endif
if [ "$1" == "0" ]; then
  # Uninstall time, stop service and cleanup

  # stop service
  %{_initrddir}/%{name} stop

  # unregister app from services
  systemctl disable %{name}.service >/dev/null 2>&1
fi

%postun
%if 0%{?suse_version} > 1140
%service_del_postun %{name}.service
%endif

%files
%defattr(-,root,root)
%attr(0755,root,root) %{_sysconfdir}/init.d/jstatd
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/jstatd
%attr(0644,root,root) %{_sysconfdir}/jstatd/all.policy

%changelog
* Sun Mar 4 2012 julien.nicoulaud@gmail.com 1.0.0-1
- Initial RPM

