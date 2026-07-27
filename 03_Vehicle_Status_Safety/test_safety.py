import subprocess
import time
import unittest

class TestVehicleSafety(unittest.TestCase):

    def setUp(self):
        print("\n[SETUP] Initializing safety environment. Releasing brake...")
        subprocess.run("adb shell dumpsys activity service Car inject-vhal-event 287310850 0 0", shell=True, stdout=subprocess.DEVNULL)
        time.sleep(1)

    def test_parking_brake_conflict(self):
        print("[TEST] Launching CAN simulator for brake conflict event...")
        subprocess.run("python ./03_Vehicle_Status_Safety/simulador_can.py", shell=True)
        time.sleep(1)
        
        print("[VALIDATION] Fetching VHAL telemetry to verify state...")
        command_verify = "adb shell dumpsys activity service Car get-property-value 287310850 0"
        dump = subprocess.check_output(command_verify, shell=True, text=True)
        
        self.assertIn("value: true", dump.lower(), "ERROR: VHAL did not register active parking brake.")
        print("[PASSED] Safety validation successful: VHAL correctly flags engaged brake under drive conditions.")

    def tearDown(self):
        print("[TEARDOWN] Resetting vehicle to safe default state (Parking & Brake Released)...")
        subprocess.run("adb shell dumpsys activity service Car inject-vhal-event 287310850 0 0", shell=True, stdout=subprocess.DEVNULL)
        subprocess.run("adb shell dumpsys activity service Car inject-vhal-event 289408000 0 4", shell=True, stdout=subprocess.DEVNULL)

if __name__ == "__main__":
    unittest.main()
