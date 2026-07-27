import subprocess
import time
import can

def send_vhal_command(command):
    """Sends infotainment control commands to the emulator"""
    try:
        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[ADB ERROR] {e}")

bus = can.interface.Bus(channel='vcan0', interface='virtual')

print("==================================================")
print("CAN SIMULATOR: STEERING WHEEL CONTROLS (INFOTAINMENT)")
print("==================================================")

try:
    print("[STEERING CONTROLS] Driver interacts with steering wheel buttons...")
    print(" -> Tx CAN: 0x2A0 | Command: INCREASE VOLUME (Set to 60%)")
    send_vhal_command("adb shell dumpsys activity service Car set-group-volume 0 0 60")
    time.sleep(1.5)
    
    print(" -> Tx CAN: 0x2A1 | Command: NEXT TRACK BUTTON (Key 87)")
    send_vhal_command("adb shell dumpsys activity service Car inject-key 87")
    time.sleep(1.5)

finally:
    bus.shutdown()
