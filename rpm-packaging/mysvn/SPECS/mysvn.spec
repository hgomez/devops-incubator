Name: mysvn
Version: 1.0.0
Release: 1
Summary: Subversion setup
Group: Applications/Communications
URL: http://www.mycorp.org/
Vendor: MyCorp
Packager: MyCorp
License: AGPLv1
BuildArch:  noarch

BuildRoot: %{_tmppath}/build-%{name}-%{version}-%{release}

Requires:           apache2
Requires:           subversion-server

Source0: httpd-svn.conf
Source1: access_rules_myrepo
Source2: access_passwords_myrepo

%description
Subversion setup for MyCorp

%prep

%build

%install
# Prep the install location.
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/apache2/vhosts.d
mkdir -p $RPM_BUILD_ROOT%{_var}/lib/mysvn/repos

cp %{SOURCE0}  $RPM_BUILD_ROOT%{_sysconfdir}/apache2/vhosts.d/svn.mycorp.org.conf
cp %{SOURCE1}  $RPM_BUILD_ROOT%{_var}/lib/mysvn/repos
cp %{SOURCE2}  $RPM_BUILD_ROOT%{_var}/lib/mysvn/repos

%post
if [ "$1" == "1" ]; then
  pushd %{_var}/lib/mysvn/repos >>/dev/null
  svnadmin create myrepo
  chown -R wwwrun:www %{_var}/lib/mysvn/repos/myrepo
  popd >>/dev/null

  # Enable Apache modules for SVN
  a2enmod dav 
  a2enmod dav_fs 
  a2enmod dav_svn 
  a2enmod authnz_ldap 
  a2enmod authz_svn 
  a2enmod ldap
  
  service apache2 restart
fi


%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/apache2/vhosts.d/svn.mycorp.org.conf
%{_var}/lib/mysvn/repos
%{_var}/lib/mysvn/repos/access_rules_myrepo
%{_var}/lib/mysvn/repos/access_passwords_myrepo


%changelog
* Wed Mar 23 2009 henri.gomez@gmail.com 1.0.0-1
- Initial RPM