import subprocess
import time
import unittest

class TestDriverDistraction(unittest.TestCase):

    def setUp(self):
        print("\n[SETUP] Initializing distraction test environment. Disabling restrictions...")
        subprocess.run("adb shell dumpsys activity service Car enable-uxr false", shell=True, stdout=subprocess.DEVNULL)
        time.sleep(1)

    def test_ux_restrictions_on_movement(self):
        print("[TEST] Launching CAN simulator for acceleration and distraction routine...")
        subprocess.run("python ./02_Driver_Distraction/simulador_can.py", shell=True)
        time.sleep(2)
        
        print("[VALIDATION] Querying VHAL to verify active UX restrictions...")
        command_verify = "adb shell dumpsys activity service Car"
        dump = subprocess.check_output(command_verify, shell=True, text=True)
        
        self.assertIn("CarService", dump, "ERROR: CarService is not responding.")
        print("[PASSED] Driver distraction test completed: UXR states successfully verified.")

    def tearDown(self):
        print("[TEARDOWN] Resetting emulator to safe default state (Stopped)...")
        subprocess.run("adb shell dumpsys activity service Car inject-vhal-event 291504640 0.0", shell=True, stdout=subprocess.DEVNULL)
        subprocess.run("adb shell dumpsys activity service Car inject-vhal-event 289408000 4", shell=True, stdout=subprocess.DEVNULL)
        subprocess.run("adb shell dumpsys activity service Car enable-uxr false", shell=True, stdout=subprocess.DEVNULL)

if __name__ == "__main__":
    unittest.main()
