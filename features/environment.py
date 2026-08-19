import subprocess
import time

def before_all(context):
    """Executes once before any test feature runs"""
    print("\n[BDD ORCHESTRATOR] Initializing global automotive validation network...")
    # Verify host ADB status
    try:
        subprocess.run("adb devices", shell=True, check=True, stdout=subprocess.DEVNULL)
    except Exception:
        print("[CRITICAL] ADB server is not running on the host. Please start the listener.")

def before_scenario(context, scenario):
    """Executes before EVERY individual scenario to ensure a clean baseline"""
    print(f"\n[SETUP] Preparing vehicle state for Scenario: '{scenario.name}'...")
    # Safe defaults: Release brake, turn off HVAC, set speed to 0, gear to Parking
    subprocess.run("adb shell dumpsys activity service Car inject-vhal-event 287312384 0 0", shell=True, stdout=subprocess.DEVNULL)
    subprocess.run("adb shell dumpsys activity service Car inject-vhal-event 291504640 0.0", shell=True, stdout=subprocess.DEVNULL)
    subprocess.run("adb shell dumpsys activity service Car inject-vhal-event 289408000 4", shell=True, stdout=subprocess.DEVNULL)
    subprocess.run("adb shell dumpsys activity service Car enable-uxr false", shell=True, stdout=subprocess.DEVNULL)
    time.sleep(1)

def after_scenario(context, scenario):
    """Executes after EVERY individual scenario to clean up the environment"""
    print(f"[TEARDOWN] Scenario '{scenario.name}' completed. Resetting systems to safe defaults...")
    subprocess.run("adb shell dumpsys activity service Car enable-uxr false", shell=True, stdout=subprocess.DEVNULL)
    subprocess.run("adb shell input keyevent 3", shell=True, stdout=subprocess.DEVNULL) # Go to Home screen
    time.sleep(1)

def after_all(context):
    """Executes once after the entire BDD suite finishes execution"""
    print("\n[BDD ORCHESTRATOR] Global automotive suite execution finished cleanly.")
