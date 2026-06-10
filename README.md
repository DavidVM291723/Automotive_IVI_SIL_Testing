# Automotive IVI & SiL Testing Sandbox (Android Automotive OS 15)

Este repositorio contiene un laboratorio portátil de **Software-in-the-Loop (SiL)** diseñado para la automatización de pruebas en sistemas de Infoentretenimiento (IVI) basados en **Android Automotive OS (AAOS 15)**, simulación de señales de la capa de vehículo (VHAL) y emulación de tramas cíclicas de red CAN mediante Python y Docker.

## 🛠️ Tecnologías y Estándares Utilizados
*   **Target OS:** Android Automotive OS (AAOS 15 - Vanilla Architecture)
*   **Automation Harness:** Python 3.11 (Subprocess, Object Serialization, Python-CAN)
*   **Virtualización y Portabilidad:** Docker Desktop & Windows Subsystem for Linux (WSL 2)
*   **Protocolos Automotrices:** VHAL Integration, Inyección de Estados de Seguridad (Interlocks), Simulación CAN Bus Cíclica (100ms)
*   **Estándares de Calidad de Software:** Diseño de pruebas alineado a metodologías **ASPICE (SWE.6 / SYS.5)** e **ISO 26262** (Análisis de Fallas Funcionales de Cabina)

## 📂 Estructura del Proyecto
*   `test_vhal.py`: Script avanzado de automatización que gestiona la máquina de estados del coche (Ignición ON -> Cinturón ON -> Freno de mano OFF -> Pedal de Freno ON -> Cambio a DRIVE -> Aceleración). Incorpora mecánicas de **Error Handling** y análisis dinámico de estampas de tiempo (`ElapsedRealtimeNanos`) del Car Service de Android.
*   `simulador_can.py`: Réplica de transmisión cíclica de bus de datos (Frecuencia: 100ms) emulando tramas crudas equivalentes a bases de datos de red automotriz (`.dbc` / CANDB) mediante la abstracción de canales virtuales de SocketCAN en memoria.
*   `Dockerfile`: Entorno contenerizado y agnóstico que empaqueta las dependencias del sistema operativo (ADB client, Python core y librerías de testing) asegurando la reproducibilidad en servidores de Integración Continua (CI/CD).

## 🚀 Instrucciones de Ejecución (Setup Remoto)

### Requisitos Previos
*   Docker Desktop (Configurado con WSL 2)
*   Android Studio con la imagen de sistema `Automotive (1024p landscape)` para Android 15 cargada y en ejecución.

### Paso 1: Configurar el puente de red ADB en el Host
Para permitir que el contenedor aislado de Docker interactúe con el coche virtual, inicie el servidor de ADB en modo global en una terminal de Windows:
```bash
adb kill-server
adb -a nodaemon server start
```

### Paso 2: Compilar el entorno contenerizado
Genere la imagen portátil ejecutando la receta del Dockerfile:
```bash
docker build -t test-vhal-automotive .
```

### Paso 3: Disparar las Pruebas Automatizadas
Ejecute el contenedor redirigiendo los sockets de comunicación al servidor global del Host:
```bash
docker run --rm -e ADB_SERVER_SOCKET=tcp:host.docker.internal:5037 test-vhal-automotive
```

## 📊 Casos de Prueba Automatizados y Lógica de Diseño (ASPICE)
Los scripts ejecutan validaciones funcionales complejas de **Driver Distraction (DD)** y **UX Restrictions (UXR)**. El algoritmo comprueba de manera determinista que el Infoentretenimiento inhabilita o degrada componentes de la interfaz gráfica (como teclados o búsquedas web) solo cuando la combinación lógica de sensores cumple con los criterios de riesgo vial definidos por la norma de seguridad funcional.
