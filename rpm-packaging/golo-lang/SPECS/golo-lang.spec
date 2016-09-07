%if ! 0%{?VERSION:1}
%define VERSION        3.2.0-M4
%endif

# Avoid unnecessary debug-information (native code)
%define		debug_package %{nil}

# Avoid jar repack (brp-java-repack-jars)
%define __jar_repack 0

# Avoid CentOS 5/6 extras processes on contents (especially brp-java-repack-jars)
%define __os_install_post %{nil}

%ifos darwin
%define __portsed sed -i "" -e
%else
%define __portsed sed -i
%endif

# Adjust RPM version (- is not allowed, lowercase strings)
%define rpm_version %(version_rel=`echo %{VERSION} | sed "s/-/./g" | tr "[:upper:]" "[:lower:]"`; echo "$version_rel")

Name:      golo-lang
Version:   %{rpm_version}
Release:   0
Summary:   Golo, a lightweight dynamic language for the JVM
Group:     Development/Languages/Other
URL:       http://golo-lang.org/
Packager:  Henri Gomez <henri.gomez@gmail.com>
License:   Apache-2.0
BuildArch: noarch

BuildRequires: unzip

BuildRoot: %{_tmppath}/build-%{name}-%{version}-%{release}

%define golodir          /opt/golo-lang

%if 0%{?suse_version}
Requires:           java >= 1.8.0
%endif

%if 0%{?fedora} || 0%{?rhel} || 0%{?centos}
Requires:           java >= 1:1.8.0
%endif

Source0: golo-%{VERSION}.zip

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

# Set GOLO REPO location
%{__portsed} 's|# resolve links|REPO=%{golodir}/lib\n# resolve links]|g' %{buildroot}%{_bindir}/golo

%clean
rm -rf %{buildroot}

%post
rm -f %{_bindir}/golo
rm -f %{_bindir}/golosh
rm -f %{_bindir}/vanilla-golo
ln -s %{golodir}/bin/golo %{_bindir}/golo
ln -s %{golodir}/bin/golosh %{_bindir}/golosh
ln -s %{golodir}/bin/vanilla-golo %{_bindir}/vanilla-golo

%postun
rm -f %{_bindir}/golo
rm -f %{_bindir}/golosh
rm -f %{_bindir}/vanilla-golo

%files
%defattr(-,root,root)
%doc %{golodir}/CONTRIB*
%doc %{golodir}/README*
%doc %{golodir}/docs
%doc %{golodir}/epl-v10.html
%doc %{golodir}/notice.html
%doc %{golodir}/THIRD-PARTY
%exclude %{golodir}/CONTRIB*
%exclude %{golodir}/README*
%exclude %{golodir}/epl-v10.html
%exclude %{golodir}/notice.html
%exclude %{golodir}/THIRD-PARTY
%exclude %{golodir}/docs
%exclude %{golodir}/samples
%{golodir}
%{_bindir}/golo

%files samples
%defattr(-,root,root)
%{golodir}/samples

%changelog
* Wed Sep 7 2016 henri.gomez@gmail.com 3.2.0-M4-1
- 3.2.0-M4 released
- Symlink at install time, removed at uninstall time

* Tue Nov 10 2015 henri.gomez@gmail.com 3.0.0-incubation-1
- Yoohoo, 3.0.0 released, congrats !

* Mon Sep 07 2015 henri.gomez@gmail.com 3.0.0-incubation-M2-1
- Fix download in source0
- Update doc contents

* Mon Sep 07 2015 romain.lespinasse@gmail.com 3.0.0-incubation-M2-1
- golo 3.0.0-incubation-M2 released

* Mon Jul 27 2015 romain.lespinasse@gmail.com 3.0.0-incubation-M1-1
- golo 3.0.0-incubation-M1 released

* Fri Mar 27 2015 romain.lespinasse@gmail.com 2.1.0-1
- golo 2.1.0 released

* Wed Jan 21 2015 henri.gomez@gmail.com 2.0.0-1
- golo 2.0.0 released

* Mon Sep 22 2014 henri.gomez@gmail.com 1.1.0-1
- golo 1.1.0 released

* Wed Jul 9 2014 henri.gomez@gmail.com 1.0.0-1
- golo 1.0.0 released

* Tue Mar 11 2014 henri.gomez@gmail.com 0.preview11-1
- golo 0-preview11 released

* Wed Dec 18 2013 henri.gomez@gmail.com 0.preview10-1
- golo 0-preview10 released

* Fri Nov 22 2013 henri.gomez@gmail.com 0.preview9-1
- golo 0-preview9 released

* Tue Nov 5 2013 henri.gomez@gmail.com 0.preview8-1
- golo 0-preview8 released

* Tue Aug 20 2013 henri.gomez@gmail.com 0.preview6-1
- golo 0-preview6 released

* Thu Jul 4 2013 henri.gomez@gmail.com 0.preview5-1
- golo 0-preview5 released
- gologolo and goloc removed

* Fri May 17 2013 henri.gomez@gmail.com 0.preview4-1
- golo 0-preview4 released

* Mon Mar 25 2013 henri.gomez@gmail.com 0.preview2-1
- golo 0-preview2 released

* Mon Mar 25 2013 henri.gomez@gmail.com 0.preview1-1
- Initial RPM
