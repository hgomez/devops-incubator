Name: mygit
Version: 1.0.0
Release: 1
Summary: GIT setup
Group: Company/Development
URL: http://www.mycorp.org/
Vendor: MyCorp
Packager: MyCorp
License: AGPLv1
BuildArch:  noarch

BuildRoot: %{_tmppath}/build-%{name}-%{version}-%{release}

Requires:           apache2
Requires:           subversion
Requires:			git-svn
Requires:			cgit
Requires:           python

Source0: apache2-git.conf
Source1: credentials
Source2: public.conf
Source3: private.conf
Source4: public-readme.html
Source5: private-readme.html
Source6: mycorp.png
Source7: mycorp.ico
Source8: markdownize_cgit.py

%description
GIT setup for MyCorp

%prep

%build

%install
# Prep the install location.
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/apache2/vhosts.d
mkdir -p $RPM_BUILD_ROOT%{_var}/lib/mygit/conf
mkdir -p $RPM_BUILD_ROOT%{_var}/lib/mygit/repos
mkdir -p $RPM_BUILD_ROOT%{_var}/lib/mygit/repos/public
mkdir -p $RPM_BUILD_ROOT%{_var}/lib/mygit/repos/private
mkdir -p $RPM_BUILD_ROOT%{_var}/lib/mygit/cache/cgit/public
mkdir -p $RPM_BUILD_ROOT%{_var}/lib/mygit/cache/cgit/private

mkdir -p $RPM_BUILD_ROOT%{_var}/lib/mygit/www/images
mkdir -p $RPM_BUILD_ROOT%{_bindir}

cp %{SOURCE0}  $RPM_BUILD_ROOT%{_sysconfdir}/apache2/vhosts.d/git.mycorp.org.conf
cp %{SOURCE1}  $RPM_BUILD_ROOT%{_var}/lib/mygit/conf
cp %{SOURCE2}  $RPM_BUILD_ROOT%{_var}/lib/mygit/conf
cp %{SOURCE3}  $RPM_BUILD_ROOT%{_var}/lib/mygit/conf
cp %{SOURCE4}  $RPM_BUILD_ROOT%{_var}/lib/mygit/www/
cp %{SOURCE5}  $RPM_BUILD_ROOT%{_var}/lib/mygit/www/
cp %{SOURCE6}  $RPM_BUILD_ROOT%{_var}/lib/mygit/www/images
cp %{SOURCE7}  $RPM_BUILD_ROOT%{_var}/lib/mygit/www/images
cp %{SOURCE8}  $RPM_BUILD_ROOT%{_bindir}

%post
if [ "$1" == "1" ]; then

  # Enable Apache modules for Git (alias, cgi and env)
  a2enmod alias
  a2enmod cgi
  a2enmod env
  a2enmod rewrite

  service apache2 restart
fi


%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/apache2/vhosts.d/git.mycorp.org.conf
%attr(0755, root, root)  %{_bindir}/markdownize_cgit.py
%{_var}/lib/mygit/conf/credentials
%{_var}/lib/mygit/conf/public.conf
%{_var}/lib/mygit/www/*.html
%{_var}/lib/mygit/www/images/*
%dir %{_var}/lib/mygit/repos/public
%dir %{_var}/lib/mygit/repos/private
%dir %{_var}/lib/mygit/cache/cgit/public
%dir %{_var}/lib/mygit/cache/cgit/private



%changelog
* Wed Mar 23 2009 henri.gomez@gmail.com 1.0.0-1
- Initial RPM