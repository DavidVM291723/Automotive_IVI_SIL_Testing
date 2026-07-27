# Automotive Testing - CAN Bus Simulator to Android VHAL Bridge

This repository hosts an enterprise-grade automated testing framework tailored for **Automotive Software Engineering**. It leverages an isolated **CAN Bus simulator** containerized within **Docker**, which intercepts, translates, and injects real-time vehicle telematics into the **Vehicle Hardware Abstraction Layer (VHAL)** of an **Android Automotive OS (AAOS)** emulator via an **ADB server pipeline**.

The framework validates critical automotive systems, ranging from cabin climate constraints to complex telematics handovers and road safety safety policies.

## 🛠️ Tech Stack & Ecosystem
* **Core Runtime:** Python 3.11 (`python-can` abstract virtual memory-mapped architecture).
* **Virtualization:** Docker & Docker Compose (Hermetic, reproducible infrastructure).
* **Automotive Platform:** Android Automotive OS (AAOS) Emulator (Landscape HMI layout).
* **Transport Bridges:** Virtual CAN Sockets, Android Debug Bridge (ADB), Win32 Network Tunneling.

## 📐 Data Pipeline & Architecture
[ Python Simulator ] ──(Virtual CAN)──> [ Docker Container ]│ (ADB Server Tunnel)[ Infotainment UI / HMI ] <───(VHAL)──── [ Windows Host ]


## 💡 How to Switch Between Test Cases

To target and execute a specific test case, you must modify the **`command`** property inside the **`docker-compose.yml`** file before running `docker compose up --build`. 

Open `docker-compose.yml` and replace the last line with the command corresponding to the domain you wish to validate:

*   **Test Case 01: Cabin Comfort & HVAC**
    ```yaml
    command: python -m unittest 01_Cabin_Comfort_HVAC/test_hvac.py
    ```
*   **Test Case 02: Driver Distraction & UX Restrictions**
    ```yaml
    command: python -m unittest 02_Driver_Distraction/test_distraction.py
    ```
*   **Test Case 03: Vehicle Status & Safety (Brake Conflict)**
    ```yaml
    command: python -m unittest 03_Vehicle_Status_Safety/test_safety.py
    ```
*   **Test Case 04: Infotainment & Media Controls**
    ```yaml
    command: python -m unittest 04_Infotainment_Media/test_media.py
    ```
*   **Test Case 05: Telematics & Incoming Calls**
    ```yaml
    command: python -m unittest 05_Telematics_Calls/test_calls.py
    ```
*   **Test Case 06: Engine Diagnostics & DTC Codes**
    ```yaml
    command: python -m unittest 06_Engine_Diagnostics_DTC/test_diagnostics.py
    ```
*   **Test Case 07: Vehicle Location & GPS Tracking**
    ```yaml
    command: python -m unittest 07_Vehicle_Location_GPS/test_location.py
    ```
*   **Test Case 08: Emergency eCall (SOS Simulation)**
    ```yaml
    command: python -m unittest 08_Emergency_eCall/test_ecall.py
    ```
*   **Test Case 09: Voice Assistant Intent**
    ```yaml
    command: python -m unittest 09_Voice_Assistant_Intent/test_assistant.py
    ```
*   **Test Case 10: Vehicle Network & Internet Handover**
    ```yaml
    command: python -m unittest 10_Vehicle_Network_Internet/test_network.py
    ```