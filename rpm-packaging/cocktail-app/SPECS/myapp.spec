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

%if %{?TOMCAT_REL:1}
%define tomcat_rel        %{TOMCAT_REL}
%else
%define tomcat_rel        7.0.41
%endif

#
# app_ver is application version provided by build script from Maven Artifact version
# ex: 1.0.0, 2.0.1-8, 3.5.0-1
#

%define app_ver    %{APP_VERSION}

# 
# app_rel is application release provided by build script from Maven Artifact version
# 
# 0.20120710.084839-182 for a SNAPSHOT
# 1 for a RELEASE
#
%define app_rel    %{APP_RELEASE}

#
# RPM release, to be updated when app_ver/app_rel don't change but spec file has been updated
#
%define rpm_rel    1

#
# Drop -x from rpm version
%define rpm_ver %(inworkver=`echo %{app_ver}`; echo "${inworkver%%-*}")

%if 0%{?APP_RELEASE:1}
%else
%define app_rel    1
%endif

Name:      cocktail-app
Version:   %{rpm_ver}
Release:   %{app_rel}.%{rpm_rel}%{?dist}
Summary:   Cocktail App %{app_rel} powered by Apache Tomcat %{tomcat_rel}
Group:     Applications/Demos
URL:       https://github.com/jmxtrans/embedded-jmxtrans-samples 
Vendor:    jmxtrans
Packager:  henri.gomez@gmail.com
License:   AGPLv1
BuildArch: noarch

%define myapp             cocktailapp
%define myappusername     cocktapp
%define myappuserid       2234
%define myappgroupid      2234

%define myappdir          /opt/%{myapp}
%define myappdatadir      %{_var}/lib/%{myapp}
%define myapplogdir       %{_var}/log/%{myapp}
%define myappexec         %{myappdir}/bin/catalina.sh
%define myappconfdir      %{myappdir}/conf
%define myappconflocaldir %{myappdir}/conf/Catalina/localhost
%define myappwebappdir    %{myappdir}/webapps
%define myapptempdir      /tmp/%{myapp}
%define myappworkdir      %{_var}/%{myapp}

%define _systemdir        /lib/systemd/system
%define _initrddir        %{_sysconfdir}/init.d

BuildRoot: %{_tmppath}/build-%{name}-%{version}-%{release}

%if 0%{?suse_version} > 1140
BuildRequires: systemd
%{?systemd_requires}
%endif

%if 0%{?suse_version} <= 1140
%define systemd_requires %{nil}
%endif

%if 0%{?suse_version}
Requires:           java >= 1.6.0
%endif

%if 0%{?fedora} || 0%{?rhel} || 0%{?centos}
Requires:           java >= 1:1.6.0
%endif

Requires(pre):      %{_sbindir}/groupadd
Requires(pre):      %{_sbindir}/useradd

Source0: apache-tomcat-%{tomcat_rel}.tar.gz
Source1: %{APP_WAR_FILE}
Source2: initd.skel
Source3: sysconfig.skel
Source4: jmxremote.access.skel
Source5: jmxremote.password.skel
Source6: setenv.sh.skel
Source7: logrotate.skel
Source8: server.xml.skel
Source9: limits.conf.skel
Source10: systemd.skel
Source11: catalina-jmx-remote-%{tomcat_rel}.jar

%description
Coktail App %{rpm_ver}-%{app_rel} powered by Apache Tomcat %{tomcat_rel}.
This Web application demonstrate use of Embedded JmxTrans.

%prep
%setup -q -c

%build

%install
# Prep the install location.
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}%{_sysconfdir}/security/limits.d
mkdir -p %{buildroot}%{_systemdir}

mkdir -p %{buildroot}%{myappdir}
mkdir -p %{buildroot}%{myappdatadir}
mkdir -p %{buildroot}%{myapplogdir}
mkdir -p %{buildroot}%{myapptempdir}
mkdir -p %{buildroot}%{myappworkdir}
mkdir -p %{buildroot}%{myappwebappdir}

# Copy tomcat
mv apache-tomcat-%{tomcat_rel}/* %{buildroot}%{myappdir}

# Create conf/Catalina/localhost
mkdir -p %{buildroot}%{myappconflocaldir}

# remove default webapps
rm -rf %{buildroot}%{myappdir}/webapps/*

# patches to have logs under /var/log/myapp
%{__portsed} 's|\${catalina.base}/logs|%{myapplogdir}|g' %{buildroot}%{myappdir}/conf/logging.properties

# myapp webapp is ROOT.war (will respond to /)
cp %{SOURCE1}  %{buildroot}%{myappwebappdir}/ROOT.war

# init.d
cp  %{SOURCE2} %{buildroot}%{_initrddir}/%{myapp}
%{__portsed} 's|@@MYAPP_APP@@|%{myapp}|g' %{buildroot}%{_initrddir}/%{myapp}
%{__portsed} 's|@@MYAPP_USER@@|%{myappusername}|g' %{buildroot}%{_initrddir}/%{myapp}
%{__portsed} 's|@@MYAPP_VERSION@@|version %{version} release %{release}|g' %{buildroot}%{_initrddir}/%{myapp}
%{__portsed} 's|@@MYAPP_EXEC@@|%{myappexec}|g' %{buildroot}%{_initrddir}/%{myapp}
%{__portsed} 's|@@MYAPP_DATADIR@@|%{myappdatadir}|g' %{buildroot}%{_initrddir}/%{myapp}
%{__portsed} 's|@@MYAPP_LOGDIR@@|%{myapplogdir}|g' %{buildroot}%{_initrddir}/%{myapp}

# sysconfig
cp  %{SOURCE3}  %{buildroot}%{_sysconfdir}/sysconfig/%{myapp}
%{__portsed} 's|@@MYAPP_APP@@|%{myapp}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{myapp}
%{__portsed} 's|@@MYAPP_APPDIR@@|%{myappdir}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{myapp}
%{__portsed} 's|@@MYAPP_DATADIR@@|%{myappdatadir}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{myapp}
%{__portsed} 's|@@MYAPP_LOGDIR@@|%{myapplogdir}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{myapp}
%{__portsed} 's|@@MYAPP_USER@@|%{myappusername}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{myapp}
%{__portsed} 's|@@MYAPP_CONFDIR@@|%{myappconfdir}|g' %{buildroot}%{_sysconfdir}/sysconfig/%{myapp}

# JMX (including JMX Remote)
cp %{SOURCE11} %{buildroot}%{myappdir}/lib
cp %{SOURCE4}  %{buildroot}%{myappconfdir}/jmxremote.access.skel
cp %{SOURCE5}  %{buildroot}%{myappconfdir}/jmxremote.password.skel

# Our custom setenv.sh to get back env variables
cp  %{SOURCE6} %{buildroot}%{myappdir}/bin/setenv.sh
%{__portsed} 's|@@MYAPP_APP@@|%{myapp}|g' %{buildroot}%{myappdir}/bin/setenv.sh

# Install logrotate
cp %{SOURCE7} %{buildroot}%{_sysconfdir}/logrotate.d/%{myapp}
%{__portsed} 's|@@MYAPP_LOGDIR@@|%{myapplogdir}|g' %{buildroot}%{_sysconfdir}/logrotate.d/%{myapp}

# Install server.xml.skel
cp %{SOURCE8} %{buildroot}%{myappconfdir}/server.xml.skel

# Setup user limits
cp %{SOURCE9} %{buildroot}%{_sysconfdir}/security/limits.d/%{myapp}.conf
%{__portsed} 's|@@MYAPP_USER@@|%{myappusername}|g' %{buildroot}%{_sysconfdir}/security/limits.d/%{myapp}.conf

# Setup Systemd
cp %{SOURCE10} %{buildroot}%{_systemdir}/%{myapp}.service
%{__portsed} 's|@@MYAPP_APP@@|%{myapp}|g' %{buildroot}%{_systemdir}/%{myapp}.service
%{__portsed} 's|@@MYAPP_EXEC@@|%{myappexec}|g' %{buildroot}%{_systemdir}/%{myapp}.service

# remove uneeded file in RPM
rm -f %{buildroot}%{myappdir}/*.sh
rm -f %{buildroot}%{myappdir}/*.bat
rm -f %{buildroot}%{myappdir}/bin/*.bat
rm -rf %{buildroot}%{myappdir}/logs
rm -rf %{buildroot}%{myappdir}/temp
rm -rf %{buildroot}%{myappdir}/work

# ensure shell scripts are executable
chmod 755 %{buildroot}%{myappdir}/bin/*.sh

%clean
rm -rf %{buildroot}

%pre
%if 0%{?suse_version} > 1140
%service_add_pre %{myapp}.service
%endif
# First install time, add user and group
if [ "$1" == "1" ]; then
  %{_sbindir}/groupadd -r -g %{myappgroupid} %{myappusername} 2>/dev/null || :
  %{_sbindir}/useradd -s /sbin/nologin -c "%{myapp} user" -g %{myappusername} -r -d %{myappdatadir} -u %{myappuserid} %{myappusername} 2>/dev/null || :
else
# Update time, stop service if running
  if [ "$1" == "2" ]; then
    if [ -f %{_var}/run/%{myapp}.pid ]; then
      %{_initrddir}/%{myapp} stop
      touch %{myapplogdir}/rpm-update-stop
    fi
    # clean up deployed webapp
    rm -rf %{myappwebappdir}/ROOT
  fi
fi

%post
%if 0%{?suse_version} > 1140
%service_add_post %{myapp}.service
%endif
# First install time, register service, generate random passwords and start application
if [ "$1" == "1" ]; then
  # register app as service
  systemctl enable %{myapp}.service >/dev/null 2>&1

  # Generated random password for RO and RW accounts
  RANDOMVAL=`echo $RANDOM | md5sum | sed "s| -||g" | tr -d " "`
  sed -i "s|@@MYAPP_RO_PWD@@|$RANDOMVAL|g" %{_sysconfdir}/sysconfig/%{myapp}
  RANDOMVAL=`echo $RANDOM | md5sum | sed "s| -||g" | tr -d " "`
  sed -i "s|@@MYAPP_RW_PWD@@|$RANDOMVAL|g" %{_sysconfdir}/sysconfig/%{myapp}

  pushd %{myappdir} >/dev/null
  ln -s %{myapplogdir}  logs
  ln -s %{myapptempdir} temp
  ln -s %{myappworkdir} work
  popd >/dev/null

  # start application at first install (uncomment next line this behaviour not expected)
  # %{_initrddir}/%{myapp} start
else
  # Update time, restart application if it was running
  if [ "$1" == "2" ]; then
    if [ -f %{myapplogdir}/rpm-update-stop ]; then
      # restart application after update (comment next line this behaviour not expected)
      %{_initrddir}/%{myapp} start
      rm -f %{myapplogdir}/rpm-update-stop
    fi
  fi
fi

%preun
%if 0%{?suse_version} > 1140
%service_del_preun %{myapp}.service
%endif
if [ "$1" == "0" ]; then
  # Uninstall time, stop service and cleanup

  # stop service
  %{_initrddir}/%{myapp} stop

  # unregister app from services
  systemctl disable %{myapp}.service >/dev/null 2>&1

  # finalize housekeeping
  rm -rf %{myappdir}
  rm -rf %{myapplogdir}
  rm -rf %{myapptempdir}
  rm -rf %{myappworkdir}

fi

%postun
%if 0%{?suse_version} > 1140
%service_del_postun %{myapp}.service
%endif

# Specific actions in relations with others packages
#%triggerin -- otherapp
# Do something if otherapp is installed

#%triggerun -- otherapp
# Do something if otherapp is uninstalled


%files
%defattr(-,root,root)
%attr(0755,%{myappusername},%{myappusername}) %dir %{myapplogdir}
%attr(0755, root,root) %{_initrddir}/%{myapp}
%attr(0644,root,root) %{_systemdir}/%{myapp}.service
%config(noreplace) %{_sysconfdir}/sysconfig/%{myapp}
%config %{_sysconfdir}/logrotate.d/%{myapp}
%config %{_sysconfdir}/security/limits.d/%{myapp}.conf
%{myappdir}/bin
%{myappdir}/conf
%{myappdir}/lib
%attr(-,%{myappusername}, %{myappusername}) %{myappdir}/webapps
%attr(0755,%{myappusername},%{myappusername}) %dir %{myappconflocaldir}
%attr(0755,%{myappusername},%{myappusername}) %dir %{myappdatadir}
%attr(0755,%{myappusername},%{myappusername}) %dir %{myapptempdir}
%attr(0755,%{myappusername},%{myappusername}) %dir %{myappworkdir}
%doc %{myappdir}/NOTICE
%doc %{myappdir}/RUNNING.txt
%doc %{myappdir}/LICENSE
%doc %{myappdir}/RELEASE-NOTES

%changelog
* Wed Jun 12 2013 henri.gomez@gmail.com 1.0.7-1
- Update package to use cocktail-app 1.0.7
- Apache Tomcat 7.0.41 powered

* Sun Apr 21 2013 henri.gomez@gmail.com 1.0.6-1
- Update package to use cocktail-app 1.0.6

* Tue Mar 26 2013 henri.gomez@gmail.com 1.0.4-1
- Initial RPM
