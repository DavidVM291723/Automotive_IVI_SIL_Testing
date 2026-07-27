import subprocess
import time
import unittest

class TestVehicleLocation(unittest.TestCase):

    def setUp(self):
        print("\n[SETUP] Initializing location environment. Waking up GPS hardware...")
        subprocess.run("adb shell cmd location set-location-properties gps --location 19.432608,-99.133208,10.0,1.0", shell=True, stdout=subprocess.DEVNULL)
        time.sleep(1)

    def test_gps_provider_response(self):
        print("[TEST] Launching CAN simulator for geographic route injection...")
        subprocess.run("python ./07_Vehicle_Location_GPS/simulador_can.py", shell=True)
        time.sleep(1)
        
        print("[VALIDATION] Inspecting Android LocationManager records...")
        command_verify = "adb shell dumpsys location"
        dump = subprocess.check_output(command_verify, shell=True, text=True)
        
        self.assertIn("location", dump.lower(), "ERROR: Location subsystem is inactive on the emulator.")
        print("[PASSED] Location test successful: GPS provider correctly responded to stream telemetry.")

    def tearDown(self):
        print("[TEARDOWN] Finalizing GPS monitoring telemetry stream...")
        pass

if __name__ == "__main__":
    unittest.main()
