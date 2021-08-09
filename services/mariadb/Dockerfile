FROM mariadb:10.6

COPY mariadb.cnf /etc/mysql/conf.d
WORKDIR /docker-entrypoint-initdb.d
RUN apt update && apt install unzip wget -y && \
    wget https://github.com/JensDll/coral-ml/releases/download/1.0.13/backup.zip && \
    unzip backup.zip && rm backup.zip