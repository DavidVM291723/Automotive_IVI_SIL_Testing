import os
import subprocess
import time
import can

def send_to_vhal(property_id, value, area_id="0"):
    """Sends the translated CAN value to the Android Emulator VHAL via ADB"""
    command = f"adb shell dumpsys activity service Car inject-vhal-event {property_id} {area_id} {value}"
    try:
        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[ADB ERROR] Failed to send to VHAL: {e}")

# Initialize virtual memory CAN bus
bus = can.interface.Bus(channel='vcan0', interface='virtual')

print("==================================================")
print("AUTOMOTIVE SIMULATOR: HVAC & UNITS CONTROL")
print("==================================================")

try:
    # 1. TURN ON HVAC (ID: 287312384)
    print("[CONFIG] Sending CAN signal to power ON Climate Control...")
    send_to_vhal("287312384", "1")
    time.sleep(1.5)

    # 2. INCREASE TEMPERATURE GRADUALLY (ID: 289411585)
    target_temperatures = ["18.0", "20.5", "22.0", "24.5", "26.0"]
    
    for i, temp in enumerate(target_temperatures, 1):
        print(f"[{i:02d}] Tx CAN: 0x201 -> VHAL Adjusting cabin temperature to {temp}°C")
        send_to_vhal("289411585", temp)
        time.sleep(1.5)

    # 3. CHANGE DISTANCE UNITS (ID: 289408514)
    print("\n[CONFIG] Sending CAN signal to toggle display measurement units...")
    
    print(" -> Tx CAN: 0x301 -> VHAL Changing display units to IMPERIAL (MPH / Miles)")
    send_to_vhal("289408514", "3")
    time.sleep(3.0)
    
    print(" -> Tx CAN: 0x301 -> VHAL Restoring display units to METRIC (KM/H)")
    send_to_vhal("289408514", "2")
    time.sleep(1.5)

finally:
    bus.shutdown()
    print("\n[STOP] Interactive comfort simulation completed successfully.")
