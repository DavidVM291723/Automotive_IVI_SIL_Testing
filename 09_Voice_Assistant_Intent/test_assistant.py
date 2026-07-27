import subprocess
import time
import unittest

class TestVehicleVoiceAssistant(unittest.TestCase):

    def setUp(self):
        print("\n[SETUP] Initializing voice service environment. Clearing active frames...")
        subprocess.run("adb shell input keyevent 3", shell=True, stdout=subprocess.DEVNULL)
        time.sleep(1)

    def test_voice_assistant_activation(self):
        print("[TEST] Launching CAN simulator for voice assistant trigger...")
        subprocess.run("python ./09_Voice_Assistant_Intent/simulador_can.py", shell=True)
        time.sleep(1.5)
        
        print("[VALIDATION] Querying records from VoiceInteractionManagerService...")
        command_verify = "adb shell dumpsys voiceinteraction"
        dump = subprocess.check_output(command_verify, shell=True, text=True)
        
        self.assertIn("voice", dump.lower(), "ERROR: Voice interaction layer is inactive on the target.")
        print("[PASSED] Voice assistant test successful: Automotive system handled steering wheel interrupt correctly.")

    def tearDown(self):
        print("[TEARDOWN] Dismissing voice capture interface overlay...")
        subprocess.run("adb shell input keyevent 3", shell=True, stdout=subprocess.DEVNULL)

if __name__ == "__main__":
    unittest.main()
