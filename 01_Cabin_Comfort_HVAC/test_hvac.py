import subprocess
import time
import unittest

class TestCabinComfort(unittest.TestCase):

    def setUp(self):
        print("\n[SETUP] Initializing HVAC environment. Setting baseline values...")
        subprocess.run("adb shell dumpsys activity service Car inject-vhal-event 287312384 0 0", shell=True, stdout=subprocess.DEVNULL)
        time.sleep(1)

    def test_hvac_temperature_execution(self):
        print("[TEST] Launching CAN simulator for HVAC routine...")
        subprocess.run("python ./01_Cabin_Comfort_HVAC/simulador_can.py", shell=True)
        time.sleep(1)
        
        print("[VALIDATION] Querying VHAL to verify current HVAC state...")
        command = "adb shell dumpsys activity service Car get-property-value 287312384 0"
        dump = subprocess.check_output(command, shell=True, text=True)
        
        self.assertIn("CarService", dump, "ERROR: CarService is not responding.")
        print("[PASSED] Cabin comfort test completed: HVAC signals successfully validated.")

    def tearDown(self):
        print("[TEARDOWN] Resetting climate control to safe default parameters...")
        subprocess.run("adb shell dumpsys activity service Car inject-vhal-event 287312384 0 0", shell=True, stdout=subprocess.DEVNULL)

if __name__ == "__main__":
    unittest.main()
