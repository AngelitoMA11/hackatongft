# Usar una imagen ligera
FROM python:3.9-slim

# Definir directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar solo los requisitos primero (para optimizar la cache)
COPY requirements.txt .

# Instalar dependencias de manera eficiente
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Exponer el puerto 8080 para Cloud Run
EXPOSE 8080

CMD ["python", "api.py"]