%if 0%{?GRAPHITE_REL:1}
%define graphite_rel        %{GRAPHITE_REL}
%else
%define graphite_rel        0.9.11
%endif

%define logdir             %{_var}/log/graphite/graphite-web

# norootforbuild
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%define py_ver %(python -c 'import sys;print(sys.version[0:3])')

Name:           mygraphite-web
Version:        %{graphite_rel}
Release:        1

License:        Apache-2.0
Group:          Productivity/Networking/Security

Requires:       python >= 2.4

%if 0%{?fedora} || 0%{?rhel} || 0%{?centos}
Requires:       Django >= 1.3
Requires:		django-tagging
%endif

%if 0%{?suse_version}
Requires:       python-django >= 1.3
Requires:       python-django-tagging
%endif

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python-devel >= 2.4

Url:            http://graphite.wikidot.com/
Source:         graphite-web-%{graphite_rel}.tar.gz
Patch:          graphite-web-%{graphite_rel}.patch

Summary:        Enterprise scalable realtime graphing
%description
Enterprise scalable realtime graphing.

%prep
%setup -n graphite-web-%{graphite_rel}
%patch
find webapp -type f -print0 | xargs -r0 chmod -v a-x

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot} --install-data=%{_datadir}/%{name}/
install -d -m 0755 %{buildroot}%{_sysconfdir}/graphite/
install -d -m 0755 %{buildroot}%{logdir}

mv %{buildroot}%{_datadir}/%{name}/conf/ %{buildroot}%{_sysconfdir}/graphite/web/

%clean
%{__rm} -rf %{buildroot}

%postun
rm -rf %{logdir}

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/graphite/

%if 0%{?suse_version}
%attr(0755,wwwrun,www) %dir %{logdir}
%endif

%if 0%{?fedora} || 0%{?rhel} || 0%{?centos}
%attr(0755,apache,apache) %dir %{logdir}
%endif

%config %{_sysconfdir}/graphite/web/
%{_bindir}

%if 0%{?rhel} != 5
%{python_sitelib}/graphite_web-%{version}-py%{py_ver}.egg-info
%endif

%{python_sitelib}/graphite/
%{_datadir}/%{name}/
%dir %{logdir}

%changelog
* Tue Aug 20 2013 henri.gomez@gmail.com 0.9.11-1
- Graphite 0.9.11 released

* Fri Feb 22 2013 henri.gomez@gmail.com 0.9.10-1
- initial package (v0.9.10)
