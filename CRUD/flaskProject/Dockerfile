FROM python:3.12-slim

# Establece el directorio de trabajo en /flaskProject
WORKDIR /flaskProject

# Instala las dependencias del sistema necesarias, incluyendo netcat-openbsd
RUN apt-get update && apt-get install -y \
    unixodbc-dev \
    curl \
    apt-transport-https \
    gnupg \
    netcat-openbsd

# Descarga y agrega el repositorio de Microsoft para el driver ODBC
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Copia los archivos de la aplicación al contenedor
COPY . .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que se ejecutará la aplicación
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python","app.py"]
