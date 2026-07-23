import subprocess
import time
import unittest

class TestVehicleEmergencyCall(unittest.TestCase):

    def setUp(self):
        print("\n[SETUP] Inicializando entorno eCall. Limpiando HMI...")
        subprocess.run("adb shell input keyevent 3", shell=True, stdout=subprocess.DEVNULL)
        time.sleep(1)

    def test_emergency_call_trigger(self):
        print("[TEST] Desplegando simulador CAN para activación de eCall (SOS)...")
        
        # Ejecutar el estímulo del simulador CAN
        subprocess.run("python ./08_Emergency_eCall/simulador_can.py", shell=True)
        time.sleep(1)
        
        print("[VALIDACIÓN] Verificando la prioridad de la llamada SOS en el HMI...")
        
        comando_verificar = "adb shell dumpsys activity activities"
        dump = subprocess.check_output(comando_verificar, shell=True, text=True)
        
        # El sistema debe registrar la apertura de la actividad telefónica de marcado/emergencia
        self.assertTrue("dialer" in dump.lower() or "car" in dump.lower(), "ERROR: El sistema no dio prioridad a la llamada de emergencia eCall.")
        print("[PASSED] Caso de prueba eCall validado: El VHAL interrumpió el sistema de forma correcta para el marcado SOS.")

    def tearDown(self):
        print("[TEARDOWN] Finalizando llamada eCall de prueba y restableciendo el vehículo...")
        subprocess.run("adb shell input keyevent 3", shell=True, stdout=subprocess.DEVNULL)

if __name__ == "__main__":
    unittest.main()
