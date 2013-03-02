#
# Due to its Python nature, there could be only a site installation for carbon
# So we just set package name to mywhisper and stick with FHS rules and Graphite suite usage (/var/lib/graphite, /etc/graphite, ...)
#

# Avoid unnecessary debug-information (native code)
%define		debug_package %{nil}

%if 0%{?WHISPER_REL:1}
%define whisper_rel        %{WHISPER_REL}
%else
%define whisper_rel        0.9.10
%endif

# norootforbuild
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%define py_ver %(python -c 'import sys;print(sys.version[0:3])')

Name:           mywhisper
Version:        %{whisper_rel}
Release:        1

License:        Apache-2.0
Group:          Productivity/Networking/Security

Requires:       python >= 2.4

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python-devel >= 2.4

Url:            http://graphite.wikidot.com/
Source:         whisper-%{whisper_rel}.tar.gz

Summary:        Fixed size round-robin style database
%description
Fixed size round-robin style database.

%prep
%setup -n whisper-%{whisper_rel}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}

%if 0%{?rhel} != 5
%{python_sitelib}/whisper-%{version}-py%{py_ver}.egg-info
%endif

%{python_sitelib}/whisper*

%changelog
* Fri Feb 22 2013 henri.gomez@gmail.com 0.9.10-1
- initial package (v0.9.10)
