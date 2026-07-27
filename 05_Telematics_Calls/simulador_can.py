import subprocess
import time
import can

def send_vhal_command(command):
    """Sends telematics commands to the emulator"""
    try:
        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[ADB ERROR] {e}")

bus = can.interface.Bus(channel='vcan0', interface='virtual')

print("==================================================")
print("CAN SIMULATOR: TELEMATICS (INCOMING CALL)")
print("==================================================")

try:
    print("[TELEMATICS ACTIVE] Detecting cellular network signal...")
    print(" -> Tx CAN: 0x3E8 | State: CALL EVENT DETECTED")
    print(" -> Tx CAN: 0x3E9 | Caller ID: +15551234567")
    
    send_vhal_command("adb shell am start-activity -a android.intent.action.DIAL -d tel:+15551234567")
    time.sleep(3.0)

finally:
    bus.shutdown()
