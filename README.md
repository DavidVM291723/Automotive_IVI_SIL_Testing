# Automotive Testing - CAN Bus Simulator to Android VHAL Bridge

Este repositorio contiene un entorno de pruebas automatizado para ingeniería de software automotriz. Consiste en un simulador de **Bus CAN virtual** empaquetado en un contenedor aislado de **Docker**, el cual intercepta y traduce señales del vehículo para inyectarlas en tiempo real en la capa **VHAL (Vehicle Hardware Abstraction Layer)** de un emulador de **Android Automotive OS (AAOS)** mediante un puente de depuración **ADB**.

La prueba simula el control de confort de la cabina, manipulando de forma interactiva el sistema de climatización (**HVAC**) y las unidades de medida reflejadas en la pantalla de infoentretenimiento del vehículo.

## 🛠️ Tecnologías y Herramientas
* **Lenguaje:** Python 3.11 (Librería `python-can` para buses virtuales en memoria).
* **Virtualización:** Docker & Docker Compose (Entornos aislados y reproducibles).
* **Automotive:** Android Automotive OS (AAOS) Emulation (API Landscape).
* **Protocolos y Puentes:** Socket/Virtual CAN, ADB (Android Debug Bridge), Win32 Host Bridge.

## 📐 Arquitectura del Flujo de Datos
## 🚀 Guía de Instalación y Ejecución

### 1. Prerrequisitos
* Tener instalado [Docker Desktop](https://docker.com) en Windows.
* Tener instalado [Android Studio](https://android.com) con un emulador de **Android Automotive OS** configurado en formato **Landscape (1024p)**.

### 2. Preparación del Emulador (Android Studio)
Para evitar bloqueos por actividades por defecto en servicios automotrices de segundo plano, configura el entorno de ejecución:
1. Ve a **Edit Configurations...** (junto al botón verde de Run).
2. En **Launch Options**, cambia el parámetro *Launch* de *Default Activity* a **Nothing**.
3. Haz un **Cold Boot** desde el *Device Manager* para inicializar la pantalla del auto limpiamente.

### 3. Configuración del Puente ADB en Windows
Android Studio levanta un servidor local automático. Para permitir que el contenedor Docker aislado se comunique con él, libera y abre el puerto desde PowerShell:
```powershell
# Forzar el cierre de procesos fantasma
Stop-Process -Name "adb" -Force

# Levantar el servidor ADB con el puente de escucha abierto para Docker
adb -a nodaemon server start
```
*Nota: Deja esta terminal abierta. El servidor se quedará en modo de escucha.*

### 4. Construcción y Despliegue con Docker Compose
Abre una segunda terminal en la raíz del proyecto y arranca la simulación con un solo comando:
```powershell
docker compose up --build
```

---

## 📊 Propiedades del VHAL Utilizadas en la Prueba
El script traduce IDs de tramas CAN estándar a las siguientes constantes del ecosistema Android Automotive:
* **`HVAC_POWER_ON`** (`ID: 287312384`): Envía señal de encendido al climatizador de la cabina.
* **`HVAC_TEMPERATURE_SET`** (`ID: 289411585`): Modifica gradualmente los floats de temperatura (`18.0°C` a `26.0°C`) reflejándose visualmente en el infoentretenimiento.
* **`DISTANCE_DISPLAY_UNITS`** (`ID: 289408514`): Alterna el sistema métrico del vehículo entre Kilómetros (`2`) e Imperial/Millas (`3`).

---

## 📝 Resultados del Caso de Prueba
Al ejecutar el contenedor, se valida la comunicación bidireccional exitosa. El sistema responde actualizando dinámicamente la interfaz gráfica (UI) del auto:
* La barra de climatización inferior responde segundo a segundo a los incrementos de temperatura enviados desde Docker.
* La consola confirma la correcta inyección mediante código de retorno limpio, libre de fallos de red tipo `Errno 19` gracias a la migración a buses virtuales controlados.