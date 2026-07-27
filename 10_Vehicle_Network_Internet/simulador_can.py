import subprocess
import time
import can

def toggle_vehicle_data(state):
    """Controls the cellular telemetry modem data state inside the TCU"""
    command = f"adb shell svc data {state}"
    try:
        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[ADB ERROR] {e}")

bus = can.interface.Bus(channel='vcan0', interface='virtual')

print("==================================================")
print("CAN SIMULATOR: ON-BOARD NETWORK CONNECTIVITY")
print("==================================================")

try:
    print("[SCENARIO 1] Vehicle entering no-coverage area (Tunnel)...")
    print(" -> Tx CAN: 0x450 | TCU Modem State: SIGNAL_LOST (0x00)")
    toggle_vehicle_data("disable")
    time.sleep(3.0)
    
    print("\n[SCENARIO 2] Vehicle exits tunnel. Restoring LTE/5G bandwidth...")
    print(" -> Tx CAN: 0x450 | TCU Modem State: SIGNAL_RESTORED (0x01)")
    toggle_vehicle_data("enable")
    time.sleep(1.5)

finally:
    bus.shutdown()
