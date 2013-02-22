%ifos darwin
%define __portsed sed -i "" -e
%else
%define __portsed sed -i
%endif

# norootforbuild
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%define py_ver %(python -c 'import sys;print(sys.version[0:3])')

%define carbonconfdir      %{_sysconfdir}/graphite/carbon
%define carbondatadir      %{_var}/lib/graphite/carbon
%define carbonlogdir       %{_var}/log/graphite/carbon
%define carbonrundir       %{_var}/run/graphite
%define webappdir		   %{_datadir}/mygraphite-web/webapp
%define contentdir		   %{webappdir}/content
%define graphiteroot	   %{_sysconfdir}/graphite
%define graphiteconfdir    %{_sysconfdir}/graphite/web
%define storagedir         %{_var}/lib/graphite/storage
%define whisperdir         %{storagedir}/whisper
%define rrddir             %{storagedir}/rrd
%define logdir             %{_var}/log/graphite/graphite-web

Name:      mygraphite-suite
Version:   1.0.0
Release:   1%{?dist}
Summary:   Graphite suite setup using Apache HTTPd in Named VirtualHost mode
Group:     Productivity/Networking/Security
Url:       http://graphite.wikidot.com/

License:   Apache-2.0
BuildArch: noarch

Requires: apache2-worker
Requires: apache2
Requires: apache2-mod_wsgi
Requires: mycarbon
Requires: mywhisper
Requires: mygraphite-web
Requires: sqlite3
Requires: python-cairo
Requires: python-ldap
Requires: python-django-ldapbackend

Source0:         local_settings.py.skel
Source1:         mygraphite.conf.skel
Source2:         graphite.wsgi.skel
Source3:         dashboard.conf
Source4:         graphTemplates.conf

BuildRoot: %{_tmppath}/build-%{name}-%{version}-%{release}

%description
Graphite suite setup using Apache HTTPd in Named VirtualHost mode.
Designed for openSUSE 12.1/12.2 and SUSE SLES 11 and higher

%prep

%build

%install
install -d -m 0755 %{buildroot}%{python_sitelib}/graphite
cp %{SOURCE0} %{buildroot}%{python_sitelib}/graphite/local_settings.py

# Graphite local-settings (django/db)
%{__portsed} 's|@@SKEL_GRAPHITEROOT@@|%{graphiteroot}|g' %{buildroot}%{python_sitelib}/graphite/local_settings.py
%{__portsed} 's|@@SKEL_CONFDIR@@|%{graphiteroot}|g' %{buildroot}%{python_sitelib}/graphite/local_settings.py
%{__portsed} 's|@@SKEL_CONTENTDIR@@|%{contentdir}|g' %{buildroot}%{python_sitelib}/graphite/local_settings.py
%{__portsed} 's|@@SKEL_STORAGEDIR@@|%{storagedir}|g' %{buildroot}%{python_sitelib}/graphite/local_settings.py
%{__portsed} 's|@@SKEL_RRDDIR@@|%{rrddir}|g' %{buildroot}%{python_sitelib}/graphite/local_settings.py
%{__portsed} 's|@@SKEL_WHISPERDIR@@|%{whisperdir}|g' %{buildroot}%{python_sitelib}/graphite/local_settings.py
%{__portsed} 's|@@SKEL_LOGDIR@@|%{logdir}|g' %{buildroot}%{python_sitelib}/graphite/local_settings.py

# Graphite VHost conf
install -d -m 0755 %{buildroot}%{_sysconfdir}/apache2/vhosts.d
cp %{SOURCE1} %{buildroot}%{_sysconfdir}/apache2/vhosts.d/mygraphite.conf
%{__portsed} 's|@@SKEL_WEBCONFDIR@@|%{graphiteconfdir}|g' %{buildroot}%{_sysconfdir}/apache2/vhosts.d/mygraphite.conf

# Graphite wsgi
install -d -m 0755 %{buildroot}%{graphiteconfdir}
cp %{SOURCE2} %{buildroot}%{graphiteconfdir}/graphite.wsgi
%{__portsed} 's|@@SKEL_WEBCONFDIR@@|%{graphiteconfdir}|g' %{buildroot}%{graphiteconfdir}/graphite.wsgi
%{__portsed} 's|@@SKEL_WEBAPPDIR@@|%{webappdir}|g' %{buildroot}%{graphiteconfdir}/graphite.wsgi

cp  %{SOURCE3} %{buildroot}%{_sysconfdir}/graphite/web
cp  %{SOURCE4} %{buildroot}%{_sysconfdir}/graphite/web

%post

if [ ! -f %{storagedir}/graphite.db ]; then
  echo "no" | python %{python_sitelib}/graphite/manage.py syncdb
  chown wwwrun:www %{storagedir}/graphite.db
  touch %{storagedir}/index
  chown wwwrun:www %{storagedir}/index
fi

# Enable Apache module (silently avoid duplicates)
a2enmod deflate >>/dev/null
a2enmod jk >>/dev/null
a2enmod wsgi >>/dev/null

# Ensure Named Virtual host mode is used
sed -i 's|#NameVirtualHost \*:80|NameVirtualHost \*:80|g' %{_sysconfdir}/apache2/listen.conf

# Ensure worker mode is used (etc/sysconf/apache2)
sed -i 's|APACHE_MPM=""|APACHE_MPM="worker"|g' %{_sysconfdir}/sysconfig/apache2

chkconfig apache2 on
service apache2 restart

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{python_sitelib}/graphite/local_settings.py
%{_sysconfdir}/apache2/vhosts.d/mygraphite.conf
%config %{_sysconfdir}/graphite/web/dashboard.conf
%config %{_sysconfdir}/graphite/web/graphTemplates.conf
%{graphiteconfdir}/graphite.wsgi

%changelog
* Fri Feb 22 2013 henri.gomez@gmail.com 1.0.0-1
- Initial package, using Graphite Web Suite 0.9.10 and Apache HTTpd in Named VirtualHost mode
- This RPM is designed to works with openSUSE 12.1/12.2 and SUSE 11 and higher