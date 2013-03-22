%ifos darwin
%define __portsed sed -i "" -e
%define __shasum shasum
%else
%define __portsed sed -i
%define __shasum sha1sum
%endif

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

Requires:           mysql-community-server
Requires:           mysql-community-server-client

Source1: sonar-setup-mysql.sh

%description
This package inject MySQL configuration into Sonar package.
It create Sonar MySQL database

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
# install mysql setup for sonar
cp %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
# First install, stop jira, prepare sql db and restart it
if [ "$1" == "1" ]; then

# 
# Ensure MySQL is up
#
%{_initrddir}/mysql start 
chkconfig mysql on

#
# If MySQL env vars are not defined, provide predefined values
#
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_ADMIN_USER=root
SONAR_DB=sonar
SONAR_USER=sonar

if [ -z "$MYSQL_ADMIN_PASSWORD" ]; then
  MYSQL_ADMIN_PASSWORD=
fi

if [ -z "$SONAR_PASSWORD" ]; then
  SONAR_PASSWORD=`echo $RANDOM | %{__shasum} | sed "s| -||g" | tr -d " "`
fi

cat << EOF1 | mysql --host=$MYSQL_HOST --port=$MYSQL_PORT --user=$MYSQL_ADMIN_USER --password=$MYSQL_ADMIN_PASSWORD
CREATE DATABASE $SONAR_DB CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE USER '$SONAR_USER' IDENTIFIED BY '$SONAR_PASSWORD';
GRANT ALL ON $SONAR_DB.* TO '$SONAR_USER'@'%' IDENTIFIED BY '$SONAR_PASSWORD';
GRANT ALL ON $SONAR_DB.* TO '$SONAR_USER'@'localhost' IDENTIFIED BY '$SONAR_PASSWORD';
FLUSH PRIVILEGES;
EOF1

# Inject SQL log/pwd into /etc/sysconfig/cisonar

%{__portsed} "s|SONAR_JDBC_USERNAME=.*|SONAR_JDBC_USERNAME=$SONAR_USER|" %{_sysconfdir}/sysconfig/%{cisonar}
%{__portsed} "s|SONAR_JDBC_PASSWORD=.*|SONAR_JDBC_PASSWORD=$SONAR_PASSWORD|" %{_sysconfdir}/sysconfig/%{cisonar}
%{__portsed} "s|SONAR_JDBC_URL=.*|SONAR_JDBC_URL=\"jdbc:mysql://$MYSQL_HOST:$MYSQL_PORT/$SONAR_DB?useUnicode=true\&characterEncoding=utf8\"|" %{_sysconfdir}/sysconfig/%{cisonar}
%{__portsed} "s|SONAR_JDBC_DRIVERCLASSNAME=.*|SONAR_JDBC_DRIVERCLASSNAME=com.mysql.jdbc.Driver|" %{_sysconfdir}/sysconfig/%{cisonar}

fi

%if 0%{?suse_version}
%triggerin -- mysql-community-server
FILEDATE=`date +%Y%m%d%H%M%S`
cp %{_sysconfdir}/my.cnf %{_sysconfdir}/my.cnf.$FILEDATE

#
# Set max_allowed_packet to 32M (http://codefabulae.blogspot.fr/2012/05/sonar-analysis-and-mysql-max-packet.html)
# Disable mysql replication support (server-id not defined)
# Disable mysql binary logs production (http://www.abluestar.com/blog/what-are-mysql-bin-000001-mysql-bin-000002/) 
#
cat %{_sysconfdir}/my.cnf.$FILEDATE | grep -v "max_allowed_packet" | \
    sed "s|\[mysqld\]|[mysqld]\nmax_allowed_packet = 32M|" | \
    sed "s|\[mysqldump\]|[mysqldump]\nmax_allowed_packet = 32M|" | \
    sed "s|server-id|#server-id|" | \
    sed "s|^log-bin=|# log-bin=|" > %{_sysconfdir}/my.cnf 
%endif

%preun
if [ "$1" == "0" ]; then
#
# If MySQL env vars are not defined, provide predefined values
#
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_ADMIN_USER=root
SONAR_DB=sonar
SONAR_USER=sonar

if [ -z "$MYSQL_ADMIN_PASSWORD" ]; then
  MYSQL_ADMIN_PASSWORD=
fi

cat << EOF1 | mysql --host=$MYSQL_HOST --port=$MYSQL_PORT --user=$MYSQL_ADMIN_USER --password=$MYSQL_ADMIN_PASSWORD
DROP DATABASE $SONAR_DB;
DROP USER '$SONAR_USER';
FLUSH PRIVILEGES;
EOF1

fi

%files
%defattr(-,root,root)
%{_bindir}

%changelog
* Wed Mar 23 2009 henri.gomez@gmail.com 1.0.0-1
- Initial RPM
