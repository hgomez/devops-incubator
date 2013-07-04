# Avoid unnecessary debug-information (native code)
%define		debug_package %{nil}

# Avoid jar repack (brp-java-repack-jars)
#%define __jar_repack 0

# Avoid CentOS 5/6 extras processes on contents (especially brp-java-repack-jars)
%define __os_install_post %{nil}

%ifos darwin
%define __portsed sed -i "" -e
%else
%define __portsed sed -i
%endif

# Adjust RPM version (- is not allowed, lowercase strings)
%define rpm_version %(version_rel=`echo %{VERSION} | sed "s/-/./g" | tr "[:upper:]" "[:lower:]"`; echo "$version_rel")

Name:     golo-lang
Version:  %{rpm_version}
Release:  1
Summary:   Golo, a lightweight dynamic language for the JVM
Group:     Development/Languages
URL:       http://golo-lang.org/
Packager:  Henri Gomez <henri.gomez@gmail.com>
License:   ASL 2.0
BuildArch: noarch

BuildRoot: %{_tmppath}/build-%{name}-%{version}-%{release}

%define golodir          /opt/golo-lang

%if 0%{?suse_version}
Requires:           java >= 1.7.0
%endif

%if 0%{?fedora} || 0%{?rhel} || 0%{?centos}
Requires:           java >= 1:1.7.0
%endif

Source0: golo-%{VERSION}-distribution.tar.gz

%description
Golo, a lightweight dynamic language for the JVM.
Golo is a simple dynamic, weakly-typed language that favours explicit over implicit. You should become a Golo programmer within hours, not days

%package samples
Summary:        Golo Samples
Group:          Development/Languages
Requires:       %{name} 

%description samples
Samples for golo-lang

%prep
%setup -n golo-%{VERSION}

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{golodir}
mkdir -p %{buildroot}%{_bindir}

# no need for bat
rm -f bin/*.bat
cp -rf * %{buildroot}%{golodir}
cp %{buildroot}%{golodir}/bin/* %{buildroot}%{_bindir}

# Set GOLO REPO location
%{__portsed} 's|# resolve links|REPO=%{golodir}/lib\n# resolve links]|g' %{buildroot}%{_bindir}/golo

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(0755,root,root) %{golodir}
%attr(0755,root,root) %{_bindir}
%exclude %{golodir}/doc
%exclude %{golodir}/samples
%doc %{golodir}/CONTRIB*
%doc %{golodir}/LICENSE*
%doc %{golodir}/NOTICE*
%doc %{golodir}/README*
%doc %{golodir}/doc

%files samples
%defattr(-,root,root)
%{golodir}/samples

%changelog
* Thu Jul 4 2013 henri.gomez@gmail.com 0.preview5-1
- golo 0-preview5 released
- gologolo and goloc removed

* Fri May 17 2013 henri.gomez@gmail.com 0.preview4-1
- golo 0-preview4 released

* Mon Mar 25 2013 henri.gomez@gmail.com 0.preview2-1
- golo 0-preview2 released

* Mon Mar 25 2013 henri.gomez@gmail.com 0.preview1-1
- Initial RPM
