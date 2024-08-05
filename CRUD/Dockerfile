FROM mcr.microsoft.com/mssql/server:latest

COPY init.sql /usr/src/app/init.sql

ENV SA_PASSWORD=1@pOrf4vorD10$
ENV ACCEPT_EULA=Y

CMD /opt/mssql/bin/sqlservr & /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "$SA_PASSWORD" -i /usr/src/app/init.sql
