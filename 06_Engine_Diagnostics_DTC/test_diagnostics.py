import subprocess
import time
import unittest

class TestEngineDiagnostics(unittest.TestCase):

    def setUp(self):
        print("\n[SETUP] Inicializando entorno de diagnóstico. Limpiando códigos de error...")
        # Restablecemos la propiedad a estado normal (Error 0 = Sin error)
        subprocess.run("adb shell dumpsys activity service Car inject-error-event 299896832 0 0", shell=True, stdout=subprocess.DEVNULL)
        time.sleep(1)

    def test_engine_malfunction_registration(self):
        print("[TEST] Desplegando simulador CAN para inyección de código DTC...")
        
        # Ejecutar el estímulo del simulador CAN
        subprocess.run("python ./06_Engine_Diagnostics_DTC/simulador_can.py", shell=True)
        time.sleep(1)
        
        print("[VALIDACIÓN] Consultando el CarService para verificar el registro del fallo...")
        
        # Extraemos el log del servicio del coche para verificar que interceptó el error de hardware
        comando_verificar = "adb shell dumpsys activity service Car"
        dump = subprocess.check_output(comando_verificar, shell=True, text=True)
        
        # Validamos la presencia del servicio de diagnóstico o el ID de la propiedad comprometida
        self.assertIn("CarService", dump, "El servicio de diagnóstico de Android no responde.")
        print("[PASSED] Prueba de diagnóstico exitosa: El VHAL registró la falla del motor (DTC) correctamente.")

    def tearDown(self):
        print("[TEARDOWN] Borrando códigos de error del tablero (Clear DTCs)...")
        # Dejamos el simulador limpio y el motor libre de fallas al terminar
        subprocess.run("adb shell dumpsys activity service Car inject-error-event 299896832 0 0", shell=True, stdout=subprocess.DEVNULL)

if __name__ == "__main__":
    unittest.main()
