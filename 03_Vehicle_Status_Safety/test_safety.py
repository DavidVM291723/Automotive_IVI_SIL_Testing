import subprocess
import time
import unittest

class TestVehicleSafety(unittest.TestCase):

    def setUp(self):
        print("\n[SETUP] Inicializando entorno de seguridad. Liberando freno...")
        # Forzar estado limpio al inicio (Freno de mano quitado = 0)
        subprocess.run("adb shell dumpsys activity service Car inject-vhal-event 287310850 0 0", shell=True, stdout=subprocess.DEVNULL)
        time.sleep(1)

    def test_parking_brake_conflict(self):
        print("[TEST] Desplegando simulador CAN para evento de freno activo...")
        
        # Ejecutar el estímulo CAN
        subprocess.run("python ./03_Vehicle_Status_Safety/simulador_can.py", shell=True)
        time.sleep(1)
        
        print("[VALIDACIÓN] Extrayendo telemetría del VHAL para verificar el estado...")
        
        # Consultamos el valor actual del Freno de Mano (Area ID: 0) en Android
        comando_verificar = "adb shell dumpsys activity service Car get-property-value 287310850 0"
        dump = subprocess.check_output(comando_verificar, shell=True, text=True)
        
        # Evaluamos si la propiedad se encuentra en 1 (True / Activo)
                # Evaluamos si el texto en minúsculas contiene el estado correcto
        self.assertIn("value: true", dump.lower(), "ERROR: El VHAL no registró el freno de mano activo.")
        print("[PASSED] Validación de seguridad exitosa: El VHAL reportó el estado de freno activo bajo marcha.")

    def tearDown(self):
        print("[TEARDOWN] Restableciendo vehículo a estado seguro (Parking y Freno Liberado)...")
        subprocess.run("adb shell dumpsys activity service Car inject-vhal-event 287310850 0 0", shell=True, stdout=subprocess.DEVNULL)
        subprocess.run("adb shell dumpsys activity service Car inject-vhal-event 289408000 0 4", shell=True, stdout=subprocess.DEVNULL)

if __name__ == "__main__":
    unittest.main()
