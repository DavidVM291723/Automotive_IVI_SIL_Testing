# Automotive Testing - CAN Bus Simulator to Android VHAL Bridge

This repository hosts an enterprise-grade automated testing framework tailored for **Automotive Software Engineering**. It leverages an isolated **CAN Bus simulator** containerized within **Docker**, which intercepts, translates, and injects real-time vehicle telematics into the **Vehicle Hardware Abstraction Layer (VHAL)** of an **Android Automotive OS (AAOS)** emulator via an **ADB server pipeline**.

The framework validates critical automotive systems, ranging from cabin climate constraints to complex telematics handovers and road safety safety policies.

## 🛠️ Tech Stack & Ecosystem
* **Core Runtime:** Python 3.11 (`python-can` abstract virtual memory-mapped architecture).
* **Virtualization:** Docker & Docker Compose (Hermetic, reproducible infrastructure).
* **Automotive Platform:** Android Automotive OS (AAOS) Emulator (Landscape HMI layout).
* **Transport Bridges:** Virtual CAN Sockets, Android Debug Bridge (ADB), Win32 Network Tunneling.

# 🚘 Automotive Testing - Containerized CAN Bus Simulator to Android VHAL Bridge

[![Build Status](https://shields.io)](https://github.com)
[![QA Methodology](https://shields.io_|_BDD-blue)](https://github.com)
[![Framework Target](https://shields.io)](https://android.com)

This repository hosts an enterprise-grade automated testing framework tailored for **Automotive Software Engineering**. It leverages an isolated **CAN Bus simulator** containerized within **Docker**, which intercepts, translates, and injects real-time vehicle telematics into the **Vehicle Hardware Abstraction Layer (VHAL)** of an **Android Automotive OS (AAOS)** emulator via an **ADB server pipeline**.

The framework architecture supports a **hybrid execution ecosystem**, coupling low-level isolated unit testing (`unittest`) with enterprise **Behavior-Driven Development (BDD)** specifications (`Gherkin/Behave`), validating 10 critical in-vehicle domains.

## 📐 Data Pipeline & Architecture
[ Python Simulator / Behave Engine ] ──(Virtual CAN)──> [ Docker Container ]│ (ADB Network Tunnel)[ Infotainment UI / Dashboard HMI ] <───────(VHAL)────── [ Windows Host Bridge ]
* **Core Runtime:** Python 3.11 (`python-can` abstract virtual memory-mapped architecture).
* **Virtualization:** Docker & Docker Compose (Hermetic, reproducible infrastructure).
* **Automotive Platform:** Android Automotive OS (AAOS) Emulator (Landscape HMI layout).
* **Transport Bridges:** Virtual CAN Sockets, Android Debug Bridge (ADB), Win32 Network Tunneling.

---

## 📂 Test Suites Portfolio Structure

The test infrastructure is modularized into 10 distinct, self-contained vehicle domains, each containing dual implementations (**Natve Unittest** and **BDD Gherkin Feature Specifications**):

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

## 🚀 Installation & Environment Setup

### 1. Host Machine Prerequisites
* [Docker Desktop](https://docker.com) configured and running on Windows 11.
* [Android Studio](https://android.com) installed with an **Android Automotive OS** virtual device (Landscape layout).

### 2. IDE Workspace Configuration (VS Code)
To enable full auto-complete syntax parsing for the business scenarios:
1. Install the **Cucumber (Gherkin) Full Support** extension in Visual Studio Code.
2. Append the following constraints to your global `settings.json` file:
   ```json
   "cucumberautocomplete.steps": ["features/steps/*.py"],
   "cucumberautocomplete.strictGherkinValidation": true
   ```

### 3. Emulator Pre-Flight Configuration
To prevent Android configuration mismatches during service verification:
1. Open **Edit Configurations...** next to the target Run button in Android Studio.
2. Under **Launch Options**, change the *Launch* parameter from *Default Activity* to **Nothing**.
3. Wipe data or perform a **Cold Boot** via the *Device Manager* to initialize a pristine layout.

### 4. Establish the Host ADB Bridge Listener
Release and open the local transport layer socket from your host PowerShell console:
```powershell
# Kill potential zombie processes
Stop-Process -Name "adb" -Force

# Launch the ADB server binding to all network interfaces
adb -a nodaemon server start
```
*Note: Keep this terminal window open; it acts as the primary network bridge.*

---

## ⚡ Automated Execution (Global Test Runner)

To execute the verification layers sequentially without manual script hacking, a global interactive PowerShell orchestrator script is provided. 

Open a new shell path pointing to the project root directory and run the runner script using the bypass security sequence:

```powershell
powershell -ExecutionPolicy Bypass -File .\Run_All_Tests.ps1
```

### Interactive Menu Selection:
Upon execution, the terminal will present an automated deployment menu:
* **Option 1:** Runs the Traditional isolated low-level `unittest` pipeline across the 10 domains sequentially.
* **Option 2:** Deploys the advanced **BDD Gherkin Suite** via the `Behave` regression engine.
* **Option 3:** Executes a **Full Comprehensive Regression Suite** (Unittest + BDD) back-to-back.

---

## 💡 Manual/Isolated Test Execution

If you wish to isolate a single test vector manually outside the orchestrator script:

### Executing BDD Features Locally
Ensure `behave` is installed on your execution layer (`pip install behave`) and run targeted specs:
```powershell
# Run all BDD features at once
behave

# Run an isolated business case
behave features/01_cabin_comfort.feature
```

### Executing Unittest Modules via Docker
Modify the **`command`** property inside the **`docker-compose.yml`** file to point to the target asset before running `docker compose up --build`:
```yaml
# Example entry configuration inside docker-compose.yml
command: python -m unittest 01_Cabin_Comfort_HVAC/test_hvac.py
```

---

## 📝 Engineering Project Ownership

```text
================================================================================
   AUTHORSHIP & FRAMEWORK COPYRIGHT NOTICES
================================================================================
   Designed, Engineered, and Maintained by:
   👉 Eliseo David Vargas Medina | Automotive QA Automation Specialist - HIL Senior Engineer - Specialist

   Core IP: Software-in-the-Loop (SIL) VHAL Core Integration Lab
   Year: 2026 | All Rights Reserved.
================================================================================
```
*This framework represents an independent intellectual asset simulating production-grade HIL/SIL pipeline verification boundaries for In-Vehicle Infotainment architectures.*