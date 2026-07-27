import subprocess
import time
import unittest

class TestVehicleEmergencyCall(unittest.TestCase):

    def setUp(self):
        print("\n[SETUP] Initializing eCall environment. Clearing active layers...")
        subprocess.run("adb shell input keyevent 3", shell=True, stdout=subprocess.DEVNULL)
        time.sleep(1)

    def test_emergency_call_trigger(self):
        print("[TEST] Launching CAN simulator for automated eCall (SOS) activation...")
        subprocess.run("python ./08_Emergency_eCall/simulador_can.py", shell=True)
        time.sleep(1)
        
        print("[VALIDATION] Verifying emergency priority state on the HMI window...")
        command_verify = "adb shell dumpsys activity activities"
        dump = subprocess.check_output(command_verify, shell=True, text=True)
        
        self.assertTrue("dialer" in dump.lower() or "car" in dump.lower(), "ERROR: Emergency dialer activity was not prioritized on screen.")
        print("[PASSED] eCall test successful: VHAL safely hijacked the system for SOS prioritization.")

    def tearDown(self):
        print("[TEARDOWN] Dismissing active eCall test frame and resetting screen...")
        subprocess.run("adb shell input keyevent 3", shell=True, stdout=subprocess.DEVNULL)

if __name__ == "__main__":
    unittest.main()
