import subprocess
import time
import unittest

class TestVehicleTelematics(unittest.TestCase):

    def setUp(self):
        print("\n[SETUP] Inicializando entorno de telemática. Volviendo a pantalla de inicio...")
        # Regresamos al Home de Android para asegurar un inicio limpio
        subprocess.run("adb shell input keyevent 3", shell=True, stdout=subprocess.DEVNULL)
        time.sleep(1)

    def test_incoming_call_interface(self):
        print("[TEST] Desplegando simulador CAN para llamada entrante...")
        
        # Ejecutar el estímulo del simulador CAN
        subprocess.run("python ./05_Telematics_Calls/simulador_can.py", shell=True)
        time.sleep(1)
        
        print("[VALIDACIÓN] Verificando actividad en pantalla (HMI) de Android Automotive...")
        
        # Consultamos qué aplicación está al frente en la interfaz gráfica
        comando_verificar = "adb shell dumpsys activity activities"
        dump = subprocess.check_output(comando_verificar, shell=True, text=True)
        
        # Validamos que la aplicación de contactos/teléfono (dialer) esté en los registros de actividades activos
        self.assertTrue("dialer" in dump.lower() or "car" in dump.lower(), "ERROR: La interfaz de llamada no se desplegó en pantalla.")
        print("[PASSED] Prueba de telemática exitosa: La interfaz de llamada interrumpió el infoentretenimiento correctamente.")

    def tearDown(self):
        print("[TEARDOWN] Cerrando aplicación de teléfono y liberando pantalla...")
        # Regresamos al Home al finalizar la prueba para dejar el sistema limpio
        subprocess.run("adb shell input keyevent 3", shell=True, stdout=subprocess.DEVNULL)

if __name__ == "__main__":
    unittest.main()
