Name: mysonar-mysql
Version: 1.0.0
Release: 1
Summary: MySQL configuration for Sonar
Group: Applications/Communications
URL: http://www.mycorp.org/
Vendor: MyCorp
Packager: MyCorp
License: AGPLv1
BuildArch:  noarch

BuildRoot: %{_tmppath}/build-%{name}-%{version}-%{release}

%description
MySQL configuration for Sonar

Requires:           mysql-community-server
Requires:           mysql-community-server-client

Source1: sonar-setup-mysql.sh

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
# install mysql setup for sonar
cp %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%pre

%post

%preun

%postun

%files
%defattr(-,root,root)
%{_bindir}

%changelog
* Wed Mar 23 2009 henri.gomez@gmail.com 1.0.0-1
- Initial RPM