FROM mcr.microsoft.com/mssql/server:2019-latest as build

ARG SA_PASSWORD
ENV ACCEPT_EULA=Y

WORKDIR /tmp

USER mssql

# 1. Launch SQL Server and wait for startup
# 2. Create empty database from script
# 3. Terminate SQL Server
RUN ( /opt/mssql/bin/sqlservr & ) | grep -q "Service Broker manager has started" \
    && /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P $SA_PASSWORD -i /tmp/build.sql \
    && pkill sqlservr

# final image
FROM mcr.microsoft.com/mssql/server:2019-latest

COPY --from=build /var/opt/mssql/data /var/opt/mssql/data