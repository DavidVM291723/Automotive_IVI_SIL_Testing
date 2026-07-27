import subprocess
import time
import can

def send_voice_event_to_vhal():
    """Injects a steering wheel voice command button hardware event"""
    command = "adb shell dumpsys activity service Car inject-key 231"
    try:
        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[ADB ERROR] {e}")

bus = can.interface.Bus(channel='vcan0', interface='virtual')

print("==================================================")
print("CAN SIMULATOR: STEERING WHEEL VOICE COMMAND BUTTON")
print("==================================================")

try:
    print("[STEERING CONTROLS] Driver presses the voice interaction button...")
    print(" -> Tx CAN: 0x2B5 | Button State: VOICE_ASSIST_PRESSED")
    print(" -> Tx CAN: 0x2B5 | Sending interrupt trigger to Android CarService...")
    
    send_voice_event_to_vhal()
    time.sleep(2.0)

finally:
    bus.shutdown()
