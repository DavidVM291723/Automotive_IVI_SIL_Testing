import subprocess
import time
import can

def send_to_vhal(property_id, value):
    """Injects state into the Android emulator using global configuration (Area 0)"""
    command = f"adb shell dumpsys activity service Car inject-vhal-event {property_id} 0 {value}"
    try:
        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[ERROR ADB] {e}")

bus = can.interface.Bus(channel='vcan0', interface='virtual')

print("==================================================")
print("CAN SIMULATOR: PARKING BRAKE & GEAR CONFLICT")
print("==================================================")

try:
    print("[SIMULATED RISK] Driver attempts to drive away with Parking Brake engaged...")
    send_to_vhal("287310850", "1")
    time.sleep(1)
    send_to_vhal("289408000", "8")
    
    print(" -> Tx CAN: 0x120 | Parking Brake: ENGAGED")
    print(" -> Tx CAN: 0x101 | Selected Gear: DRIVE")
    time.sleep(2)

finally:
    bus.shutdown()
