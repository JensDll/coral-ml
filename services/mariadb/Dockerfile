FROM mariadb:10.6

COPY mariadb.cnf /etc/mysql/conf.d
COPY build.sql /docker-entrypoint-initdb.d
