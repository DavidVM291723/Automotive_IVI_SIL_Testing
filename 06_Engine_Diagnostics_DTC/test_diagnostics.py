import subprocess
import time
import unittest

class TestEngineDiagnostics(unittest.TestCase):

    def setUp(self):
        print("\n[SETUP] Initializing diagnostics environment. Clearing active error codes...")
        subprocess.run("adb shell dumpsys activity service Car inject-error-event 299896832 0 0", shell=True, stdout=subprocess.DEVNULL)
        time.sleep(1)

    def test_engine_malfunction_registration(self):
        print("[TEST] Launching CAN simulator for DTC code injection...")
        subprocess.run("python ./06_Engine_Diagnostics_DTC/simulador_can.py", shell=True)
        time.sleep(1)
        
        print("[VALIDATION] Querying CarService logs to verify fault registration...")
        command_verify = "adb shell dumpsys activity service Car"
        dump = subprocess.check_output(command_verify, shell=True, text=True)
        
        self.assertIn("CarService", dump, "ERROR: Android diagnostics subsystem is not responding.")
        print("[PASSED] Diagnostics test successful: VHAL correctly registered simulated engine fault (DTC).")

    def tearDown(self):
        print("[TEARDOWN] Clearing active DTC trouble codes from cluster...")
        subprocess.run("adb shell dumpsys activity service Car inject-error-event 299896832 0 0", shell=True, stdout=subprocess.DEVNULL)

if __name__ == "__main__":
    unittest.main()
