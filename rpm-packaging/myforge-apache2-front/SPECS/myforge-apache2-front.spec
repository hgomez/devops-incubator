Name: mysonar-apache2-front
Version: 1.0.0
Release: 1
Summary: Apache2 Front configuration for Sonar
Group: Applications/Communications
URL: http://www.mycorp.org/
Vendor: MyCorp
Packager: MyCorp
License: AGPLv1
BuildArch:  noarch

BuildRoot: %{_tmppath}/build-%{name}-%{version}-%{release}

Requires: apache2-mod_jk

Provides: mysonar-http-front

Source0: workers.properties
Source1: jk.conf
Source2: ci.mycorp.org.conf
Source3: repository.mycorp.org.conf
Source4: sonar.mycorp.org.conf

%description
Apache2 Front configuration for Sonar

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/apache2/conf.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/apache2/vhosts.d

# install vhost and jk settings
cp %{SOURCE0} $RPM_BUILD_ROOT%{_sysconfdir}/apache2/conf.d
cp %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache2/conf.d
cp %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/apache2/vhosts.d
cp %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/apache2/vhosts.d
cp %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/apache2/vhosts.d

%clean
rm -rf $RPM_BUILD_ROOT

%pre

%post
if [ "$1" == "1" ]; then

  # Enable Apache module
  a2enmod deflate
  a2enmod jk
  service apache2 restart

fi


%preun

%postun

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/apache2/vhosts.d/
%config(noreplace) %{_sysconfdir}/apache2/conf.d/

%changelog
* Wed Mar 23 2009 henri.gomez@gmail.com 1.0.0-1
- Initial RPM