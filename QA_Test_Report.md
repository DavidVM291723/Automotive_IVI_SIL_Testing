# 📊 Test Execution & Performance Metrics Report
**Proyecto:** Framework de Automatización VHAL - Android Automotive OS (AAOS)  
**Entorno de Prueba:** Docker Container (Debian/Python 3.11) x Host Windows 11 (WSL2/ADB Bridge)  
**Fecha de Ejecución:** Julio 2026  
**Estatus Global:** 🟩 PASSED (10/10)

Este informe técnico consolida las métricas de rendimiento, tiempos de respuesta y estabilidad de la suite automatizada de pruebas para la Capa de Abstracción de Hardware del Vehículo (VHAL).

---

## 📈 Resumen Ejecutivo de Tiempos de Ejecución

A continuación se detallan los tiempos reales medidos por la terminal de Docker (utilizando el test runner nativo de `unittest`) durante la inyección de señales CAN y la validación en el HMI del emulador.

| ID | Suite de Prueba | Evento / Estímulo CAN | Tiempo (s) | Estatus |
|:---|:---|:---|:---:|:---:|
| 01 | `01_Cabin_Comfort_HVAC` | Control interactivo de clima y cambio de unidades | ~9.50 | 🟩 PASS |
| 02 | `02_Driver_Distraction` | Activación de UX Restrictions (UXR) en marcha | 29.71 | 🟩 PASS |
| 03 | `03_Vehicle_Status_Safety` | Conflicto de Freno de Mano activo vs. marcha Drive | 15.88 | 🟩 PASS |
| 04 | `04_Infotainment_Media` | Mandos al volante (Volumen + Cambio de pista) | 16.80 | 🟩 PASS |
| 05 | `05_Telematics_Calls` | Despliegue de marcador telefónico por llamada entrante | 7.69 | 🟩 PASS |
| 06 | `06_Engine_Diagnostics_DTC` | Registro de códigos de error de motor (OBD2/UDS) | 11.68 | 🟩 PASS |
| 07 | `07_Vehicle_Location_GPS` | Inyección de coordenadas y telemetría de ruta | 7.29 | 🟩 PASS |
| 08 | `08_Emergency_eCall` | Priorización HMI para llamada automática de emergencia | 6.94 | 🟩 PASS |
| 09 | `09_Voice_Assistant_Intent` | Invocación de Google Assistant por botón del volante | 10.15 | 🟩 PASS |
| 10 | `10_Vehicle_Network_Internet` | Conmutación de red celular (Modo Offline en Túnel) | 7.30 | 🟩 PASS |

**Tiempo Total de Ejecución de_la Suite:** ~122.94 segundos (~2.04 minutos)

---

## 🧠 Análisis Técnico de Latencias

1. **Casos de Alta Duración (`02`, `03`, `04`):**
   * El caso `02_Driver_Distraction` presenta el mayor tiempo de ejecución (29.71s) debido a que incluye retardos programados (`time.sleep`) para garantizar que el `CarService` asiente las restricciones visuales y permita la inspección visual en la pantalla táctil antes del desmantelamiento (`tearDown`).
2. **Optimización de Pruebas Telemáticas y Críticas (`05`, `07`, `08`, `10`):**
   * Los subsistemas de GPS, eCall y Red de Datos se validaron en rangos óptimos de **6.9 a 7.6 segundos**. Esto demuestra la eficiencia de los comandos directos de la shell de Android (`cmd location`, `svc data`) frente a las consultas masivas de dumpsys.

---

## 🛠️ Lecciones Aprendidas de Ingeniería y Debugging

Durante el ciclo de desarrollo del framework, se identificaron y solucionaron los siguientes cuellos de botella de integración:
* **Manejo de Bloqueos en Host (Socket Errors):** Se resolvió el error de socket `10048` mediante la automatización de la limpieza de procesos fantasmas de ADB (`adb kill-server` / `Stop-Process`) antes de abrir el puente de Docker.
* **Compatibilidad de Red (Kernel WSL2):** Ante la falta del módulo nativo de Linux `vcan` en el kernel básico de Docker Desktop en Windows, la arquitectura se migró exitosamente al driver de memoria `virtual` de `python-can`, garantizando la portabilidad del portafolio.
* **Normalización de Strings en Aserciones:** Se corrigieron falsos negativos en el test runner (como en la suite `03`) implementando métodos de sanitización de texto (`dump.lower()`) para alinear las respuestas asíncronas de Android con los `assertIn` de Python.

---
*Reporte autogenerado por el Framework de Automatización de Pruebas.*
