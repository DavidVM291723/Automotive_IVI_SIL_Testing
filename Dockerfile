# Paso 1: Usar una imagen oficial de Python ligera como base
FROM python:3.11-slim

# Paso 2: Instalar dependencias del sistema operativo
RUN apt-get update && apt-get install -y \
    adb \
    && rm -rf /var/lib/apt/lists/*

# Paso 3: Definir el directorio de trabajo
WORKDIR /app

# Paso 4: Copiar e instalar requerimientos de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Paso 5: ¡AQUÍ ESTÁ EL CAMBIO! Copiar TODO el contenido de la carpeta actual
COPY . .

# Paso 6: Comando por defecto al arrancar
CMD ["python", "simulador_can.py"]
