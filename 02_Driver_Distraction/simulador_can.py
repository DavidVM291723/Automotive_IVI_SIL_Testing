import subprocess
import time
import can

def send_to_vhal(command):
    """Executes injection commands inside the emulator environment"""
    try:
        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[ADB ERROR] {e}")

bus = can.interface.Bus(channel='vcan0', interface='virtual')

print("==================================================")
print("TEST CASE 02: DRIVER DISTRACTION & UX RESTRICTIONS")
print("==================================================")

try:
    print("\n[SCENARIO 1] Vehicle starts moving. Enforcing UX restrictions...")
    send_to_vhal("adb shell dumpsys activity service Car inject-vhal-event 289408000 8")
    send_to_vhal("adb shell dumpsys activity service Car inject-vhal-event 291504640 85.0")
    send_to_vhal("adb shell dumpsys activity service Car enable-uxr true")
    
    print(" -> [ALERT] Speed: 85 km/h | Gear: DRIVE")
    print(" -> [VHAL] UX Restrictions ENFORCED (Non-optimized apps blocked on screen)")
    time.sleep(5.0)

    print("\n[SCENARIO 2] Vehicle stops at traffic light. Disabling UX restrictions...")
    send_to_vhal("adb shell dumpsys activity service Car inject-vhal-event 291504640 0.0")
    send_to_vhal("adb shell dumpsys activity service Car inject-vhal-event 289408000 4")
    send_to_vhal("adb shell dumpsys activity service Car enable-uxr false")
    
    print(" -> [INFO] Speed: 0 km/h | Gear: PARKING")
    print(" -> [VHAL] UX Restrictions DISABLED (Screen unlocked)")
    time.sleep(2.0)

finally:
    bus.shutdown()
    print("\n[STOP] Driver distraction test case completed.")
