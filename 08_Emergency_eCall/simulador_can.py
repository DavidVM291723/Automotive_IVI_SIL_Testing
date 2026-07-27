import subprocess
import time
import can

def trigger_vhal_ecall():
    """Injects a high-priority automatic emergency SOS call action"""
    # Note: For simulation purposes, this triggers an intent, not a real call.
    command = "adb shell am start-activity -a android.intent.action.CALL -d tel:112"
    try:
        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[ADB ERROR] {e}")

bus = can.interface.Bus(channel='vcan0', interface='virtual')

print("==================================================")
print("CAN SIMULATOR: TELEMATICS eCALL SYSTEM (SOS)")
print("==================================================")

try:
    print("[CRITICAL EVENT] Impact sensors detect severe collision...")
    print(" -> Tx CAN: 0x050 | Airbag Status: DEPLOYED")
    print(" -> Tx CAN: 0x051 | eCall Module: Triggering automated SOS emergency call...")
    
    trigger_vhal_ecall()
    time.sleep(3.0)

finally:
    bus.shutdown()
