# Usar imagen base de Python estable
FROM python:3.12-slim

# Evitar que Python genere archivos .pyc y permitir logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el contenido del repositorio dentro de la carpeta 'LIA'
# ADK necesita que el agente esté en un subdirectorio con __init__.py
# para cargarlo como paquete Python (igual que en local con 'adk web .')
COPY . ./LIA

# Exponer el puerto por defecto de ADK (8000)
EXPOSE 8000

# Comando para ejecutar el agente con la interfaz web
# ADK buscará la carpeta 'LIA' como paquete y cargará root_agent
CMD ["adk", "web", "--host", "0.0.0.0", "--port", "8000"]
