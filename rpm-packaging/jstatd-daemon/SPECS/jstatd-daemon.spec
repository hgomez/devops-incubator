Name: jstatd-daemon
Version: %{VERSION}
Release: 1
Summary: A configurable rc.d daemon for jstatd.
Group: Development/Tools 
URL: http://docs.oracle.com/javase/6/docs/technotes/tools/share/jstatd.html
Packager: Julien Nicoulaud <julien.nicoulaud@gmail.com>
License: BSD
BuildArch:  noarch

BuildRoot: %{_tmppath}/build-%{name}-%{version}-%{release}

Requires: jdk

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

%files
%defattr(-,root,root)
%attr(0755,root,root) %{_sysconfdir}/init.d/jstatd
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/jstatd
%attr(0644,root,root) %{_sysconfdir}/jstatd/all.policy 

%changelog
* Sun Mar 4 2012 julien.nicoulaud@gmail.com 1.0.0-1
- Initial RPM

