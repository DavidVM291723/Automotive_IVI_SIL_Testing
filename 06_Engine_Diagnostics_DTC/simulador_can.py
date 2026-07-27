import subprocess
import time
import can

def inject_vhal_error(property_id, zone, error_code):
    """Injects a hardware error event directly into the Android VHAL"""
    command = f"adb shell dumpsys activity service Car inject-error-event {property_id} {zone} {error_code}"
    try:
        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[ADB ERROR] {e}")

bus = can.interface.Bus(channel='vcan0', interface='virtual')

print("==================================================")
print("CAN SIMULATOR: ENGINE DIAGNOSTICS (DTC / OBD2)")
print("==================================================")

try:
    print("[CRITICAL ALERT] Powertrain sensor reports temperature/pressure malfunction...")
    print(" -> Tx CAN: 0x7DF | Query: UDS Request Diagnostic Trouble Codes")
    print(" -> Tx CAN: 0x7E8 | Response: DTC P0117 - Engine Coolant Temp Circuit Low")
    
    # Inject malfunction state into OBD2 Live Frame property (ID: 299896832, Error Code: 3)
    inject_vhal_error("299896832", "0", "3")
    time.sleep(2.0)

finally:
    bus.shutdown()
