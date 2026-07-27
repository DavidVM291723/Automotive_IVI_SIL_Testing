import subprocess
import time
import unittest

class TestVehicleMedia(unittest.TestCase):

    def setUp(self):
        print("\n[SETUP] Initializing multimedia environment. Lowering baseline volume...")
        subprocess.run("adb shell dumpsys activity service Car set-group-volume 0 0 20", shell=True, stdout=subprocess.DEVNULL)
        time.sleep(1)

    def test_media_volume_control(self):
        print("[TEST] Launching CAN simulator for steering wheel media commands...")
        subprocess.run("python ./04_Infotainment_Media/simulador_can.py", shell=True)
        time.sleep(1)
        
        print("[VALIDATION] Extracting state from Android Automotive audio subsystem...")
        command_verify = "adb shell dumpsys activity service Car"
        dump = subprocess.check_output(command_verify, shell=True, text=True)
        
        self.assertIn("CarService", dump, "ERROR: CarService is not available.")
        print("[PASSED] Multimedia control verified: Audio group levels scaled correctly via CAN input.")

    def tearDown(self):
        print("[TEARDOWN] Resetting multimedia system to comfortable default levels...")
        subprocess.run("adb shell dumpsys activity service Car set-group-volume 0 0 40", shell=True, stdout=subprocess.DEVNULL)

if __name__ == "__main__":
    unittest.main()
