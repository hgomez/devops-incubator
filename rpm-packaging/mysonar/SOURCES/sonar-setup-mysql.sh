#!/bin/sh

SONAR_USER=sonar
SONAR_PASSWORD=sonar
SONAR_DATABASE=sonar
SONAR_HOST=localhost
SONAR_PORT=3306

ADMIN_USER=root
ADMIN_PASSWORD=

#
# help / usage about program
#
usage()
{
cat << EOF
usage: $0 options

This script setup Sonar for MySQL.

OPTIONS:
   -h   Show this message
   -u   Sonar user (default: $SONAR_USER)
   -p   Sonar password (default: $SONAR_PASSWORD)
   -U   MySQL admin user (default: $ADMIN_USER)
   -P   MySQL admin password (default: $ADMIN_PASSWORD)
   -d   Sonar database (default: $SONAR_DATABASE)
   -o   MySQL server host (default: $SONAR_HOST)
   -r   MySQL server port (default: $SONAR_PORT)

EOF
}

#
# without parameters, provide help
#
if [ $# = 0 ]; then
  usage
  exit 1;
fi

while getopts "hu:p:U:P:d:o:r:" OPTION
do
     case $OPTION in
         h)
             usage
             exit 1
             ;;
         u)
             SONAR_USER=$OPTARG
             ;;
         p)
             SONAR_PASSWORD=$OPTARG
             ;;
         U)
             ADMIN_USER=$OPTARG
             ;;
         P)
             ADMIN_PASSWORD=$OPTARG
             ;;
         d)
             SONAR_DATABASE=$OPTARG
             ;;
         o)
             SONAR_HOST=$OPTARG
             ;;
         r)
             SONAR_PORT=$OPTARG
             ;;
         ?)
             usage
             exit
             ;;
     esac
done

cat << EOF1 | mysql --host=$SONAR_HOST --port=$SONAR_PORT --user=$ADMIN_USER --password=$ADMIN_PASSWORD
CREATE DATABASE $SONAR_DATABASE CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE USER '$SONAR_USER' IDENTIFIED BY '$SONAR_PASSWORD';
GRANT ALL ON $SONAR_DATABASE.* TO '$SONAR_USER'@'%' IDENTIFIED BY '$SONAR_PASSWORD';
GRANT ALL ON $SONAR_DATABASE.* TO '$SONAR_USER'@'localhost' IDENTIFIED BY '$SONAR_PASSWORD';
FLUSH PRIVILEGES;
EOF1

if [ ! -f /etc/sysconfig/mysonar.orig ]; then
  mv /etc/sysconfig/mysonar /etc/sysconfig/mysonar.orig
fi

cat /etc/sysconfig/mysonar | sed "s|SONAR_JDBC_USERNAME=.*|SONAR_JDBC_USERNAME=$SONAR_USER|" | \
sed "s|SONAR_JDBC_USERNAME=.*|SONAR_JDBC_USERNAME=$SONAR_USER|" | \
sed "s|SONAR_JDBC_PASSWORD=.*|SONAR_JDBC_PASSWORD=$SONAR_PASSWORD|" | \
sed "s|SONAR_JDBC_URL=.*|SONAR_JDBC_URL=jdbc:mysql://$SONAR_HOST:$SONAR_PORT/$SONAR_DATABASE?useUnicode=true&characterEncoding=utf8|" | \
sed "s|SONAR_JDBC_DRIVERCLASSNAME=.*|SONAR_JDBC_DRIVERCLASSNAME=com.mysql.jdbc.Driver|" > /etc/sysconfig/mysonar
