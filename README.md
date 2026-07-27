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


---

## 📂 Test Suites Portfolio Structure

The test infrastructure is modularized into 10 distinct, self-contained domain suites:

1. **`01_Cabin_Comfort_HVAC`**: Simulates CAN comfort frames. Drives linear cabin temperature scaling and validates metric/imperial display units toggling across the central HMI.
2. **`02_Driver_Distraction`**: Validates safety constraints via UX Restrictions (UXR). Enforces interface lockdown protocols the moment mock vehicle speeds indicate active motion.
3. **`03_Vehicle_Status_Safety`**: Asserts interlock states, flagging critical driver conflicts such as attempts to engage `Drive` gears while keeping the electronic `PARKING_BRAKE_ON`.
4. **`04_Infotainment_Media`**: Intercepts steering wheel accessory buttons. Remotely orchestrates the target audio app layout, validating volume scaling and media tracking via CAN interrupts.
5. **`05_Telematics_Calls`**: Validates cellular baseband signaling. Injects mock incoming call payloads to verify HMI preemption logic and dialer application deployment priorities.
6. **`06_Engine_Diagnostics_DTC`**: Simulates powertrain diagnostics (OBD2/UDS). Injects powertrain trouble code frames (DTCs) to monitor how the VHAL logs hardware malfunctions.
7. **`07_Vehicle_Location_GPS`**: Injects real-time satellite positioning telemetry. Streams coordinate sequences to mock cross-city route tracking over the central navigation layout.
8. **`08_Emergency_eCall`**: Validates regulatory eCall SOS emergency automated response. Simulates passive crash sensor triggering (Airbag deployment) to verify dialer preemption rules.
9. **`09_Voice_Assistant_Intent`**: Integrates speech recognition layers. Processes steering wheel push-to-talk (PTT) CAN signals to wake up the native voice capture window overlay.
10. **`10_Vehicle_Network_Internet`**: Evaluates TCU cellular modem resilience. Simulates connection dropouts and handovers (e.g., subterranean tunnel transitions) across the network stack.

---

## 🚀 Installation & Execution Guide

### 1. Prerequisites
* [Docker Desktop](https://docker.com) installed on Windows.
* [Android Studio](https://android.com) configured with an **Android Automotive OS** virtual device (Landscape layout).

### 2. Emulator Pre-Flight Configuration
To prevent Android configuration mismatches during service verification:
1. Open **Edit Configurations...** next to the target Run button in Android Studio.
2. Under **Launch Options**, change the *Launch* parameter from *Default Activity* to **Nothing**.
3. Wipe data or perform a **Cold Boot** via the *Device Manager* to initialize a pristine layout.

### 3. Establish the Host ADB Bridge Listener
Release and open the local transport layer socket from your host PowerShell console:
```powershell
# Kill potential zombie processes
Stop-Process -Name "adb" -Force

# Launch the ADB server binding to all network interfaces
adb -a nodaemon server start
```
*Note: Keep this terminal window open; it acts as the bridge listener.*

---

## ⚡ Automated Full Suite Execution (Test Runner)

To execute all 10 test cases sequentially without any manual intervention, a global PowerShell orchestrator script is provided. This automation dynamically mutates the Docker orchester, deploys the isolation layers, aggregates results, and ensures clean environment transitions.

Open your local terminal at the root of the project folder and run the runner script using the execution policy bypass sequence:

```powershell
powershell -ExecutionPolicy Bypass -File .\Run_All_Tests.ps1
```

The orchestrator will take complete control of your workspace, validating every single domain automatically and printing out a finalized regression report.

---

## 💡 Manual Step-by-Step Execution

If you wish to target and manually isolate a single test case instead of running the automated sequence, you must modify the **`command`** property inside the **`docker-compose.yml`** file. 

Open `docker-compose.yml` and substitute the last line with the command corresponding to the domain you wish to validate before running `docker compose up --build`:

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