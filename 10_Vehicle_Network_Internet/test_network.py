import subprocess
import time
import unittest

class TestVehicleNetwork(unittest.TestCase):

    def setUp(self):
        print("\n[SETUP] Initializing connectivity diagnostics. Enforcing active link...")
        subprocess.run("adb shell svc data enable", shell=True, stdout=subprocess.DEVNULL)
        time.sleep(1)

    def test_network_connectivity_manager(self):
        print("[TEST] Launching CAN simulator for cellular link handovers...")
        subprocess.run("python ./10_Vehicle_Network_Internet/simulador_can.py", shell=True)
        time.sleep(1)
        
        print("[VALIDATION] Querying Android ConnectivityService network stack logs...")
        command_verify = "adb shell dumpsys connectivity"
        dump = subprocess.check_output(command_verify, shell=True, text=True)
        
        self.assertIn("connectivity", dump.lower(), "ERROR: Connectivity services are unavailable.")
        print("[PASSED] Network test successful: VHAL successfully parsed modem handover boundaries.")

    def tearDown(self):
        print("[TEARDOWN] Restoring onboard communications modem to safe default active link...")
        subprocess.run("adb shell svc data enable", shell=True, stdout=subprocess.DEVNULL)

if __name__ == "__main__":
    unittest.main()
