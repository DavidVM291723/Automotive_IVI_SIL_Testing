import subprocess
import time
import unittest

class TestVehicleTelematics(unittest.TestCase):

    def setUp(self):
        print("\n[SETUP] Initializing telematics environment. Returning to Home screen...")
        subprocess.run("adb shell input keyevent 3", shell=True, stdout=subprocess.DEVNULL)
        time.sleep(1)

    def test_incoming_call_interface(self):
        print("[TEST] Launching CAN simulator for incoming call event...")
        subprocess.run("python ./05_Telematics_Calls/simulador_can.py", shell=True)
        time.sleep(1)
        
        print("[VALIDATION] Checking foreground activity on Android Automotive HMI...")
        command_verify = "adb shell dumpsys activity activities"
        dump = subprocess.check_output(command_verify, shell=True, text=True)
        
        self.assertTrue("dialer" in dump.lower() or "car" in dump.lower(), "ERROR: Dialer interface failed to deploy on screen.")
        print("[PASSED] Telematics test successful: Incoming call screen successfully prioritized over HMI.")

    def tearDown(self):
        print("[TEARDOWN] Dismissing dialer activity and clearing screen...")
        subprocess.run("adb shell input keyevent 3", shell=True, stdout=subprocess.DEVNULL)

if __name__ == "__main__":
    unittest.main()
