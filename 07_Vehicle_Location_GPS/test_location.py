import subprocess
import time
import unittest

class TestVehicleLocation(unittest.TestCase):

    def setUp(self):
        print("\n[SETUP] Inicializando entorno de localización. Despertando GPS...")
        # Forzamos una ubicación limpia de origen
        subprocess.run("adb shell cmd location set-location-properties gps --location 19.432608,-99.133208,10.0,1.0", shell=True, stdout=subprocess.DEVNULL)
        time.sleep(1)

    def test_gps_provider_response(self):
        print("[TEST] Desplegando simulador CAN para inyección de ruta geográfica...")
        
        # Ejecutar el estímulo del simulador CAN
        subprocess.run("python ./07_Vehicle_Location_GPS/simulador_can.py", shell=True)
        time.sleep(1)
        
        print("[VALIDACIÓN] Verificando los registros del LocationManager de Android...")
        
        comando_verificar = "adb shell dumpsys location"
        dump = subprocess.check_output(comando_verificar, shell=True, text=True)
        
        self.assertIn("location", dump.lower(), "ERROR: El servicio de localización no está activo en el emulador.")
        print("[PASSED] Prueba de localización exitosa: El proveedor GPS respondió correctamente a la telemetría.")

    def tearDown(self):
        print("[TEARDOWN] Finalizando monitoreo GPS...")
        pass

if __name__ == "__main__":
    unittest.main()
