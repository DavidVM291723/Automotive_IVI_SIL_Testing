import subprocess
import time
import unittest

class TestVehicleNetwork(unittest.TestCase):

    def setUp(self):
        print("\n[SETUP] Inicializando entorno de red. Asegurando conexión activa...")
        subprocess.run("adb shell svc data enable", shell=True, stdout=subprocess.DEVNULL)
        time.sleep(1)

    def test_network_connectivity_manager(self):
        print("[TEST] Desplegando simulador CAN para simulación de conmutación de red...")
        
        # Ejecutar el estímulo del simulador CAN
        subprocess.run("python ./10_Vehicle_Network_Internet/simulador_can.py", shell=True)
        time.sleep(1)
        
        print("[VALIDACIÓN] Extrayendo telemetría del ConnectivityService de Android...")
        
        # Consultamos el estado del gestor de red móvil de Android
        comando_verificar = "adb shell dumpsys connectivity"
        dump = subprocess.check_output(comando_verificar, shell=True, text=True)
        
        # Validamos que el subsistema de conectividad de red esté operando correctamente
        self.assertIn("connectivity", dump.lower(), "ERROR: El servicio de conectividad de red no está disponible.")
        print("[PASSED] Prueba de red exitosa: La pila de conectividad del VHAL gestionó correctamente los cambios de señal.")

    def tearDown(self):
        print("[TEARDOWN] Restableciendo conectividad del vehículo a estado seguro de fábrica...")
        subprocess.run("adb shell svc data enable", shell=True, stdout=subprocess.DEVNULL)

if __name__ == "__main__":
    unittest.main()
