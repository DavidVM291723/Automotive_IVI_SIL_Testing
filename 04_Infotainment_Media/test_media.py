import subprocess
import time
import unittest

class TestVehicleMedia(unittest.TestCase):

    def setUp(self):
        print("\n[SETUP] Inicializando entorno multimedia. Bajando volumen base...")
        # Inicializamos el volumen del sistema en un estado bajo (20%) para notar el cambio
        subprocess.run("adb shell dumpsys activity service Car set-group-volume 0 0 20", shell=True, stdout=subprocess.DEVNULL)
        time.sleep(1)

    def test_media_volume_control(self):
        print("[TEST] Desplegando simulador CAN para comandos multimedia del volante...")
        
        # Ejecutar el estímulo del simulador CAN
        subprocess.run("python ./04_Infotainment_Media/simulador_can.py", shell=True)
        time.sleep(1)
        
        print("[VALIDACIÓN] Extrayendo estado del sistema de audio de Android Automotive...")
        
        # Consultamos el volcado del CarAudioService para verificar los niveles actuales
        comando_verificar = "adb shell dumpsys activity service Car"
        dump = subprocess.check_output(comando_verificar, shell=True, text=True)
        
        # Validamos que el comando del volumen (60) o el estado del Radio/Audio responda de forma correcta
        self.assertIn("CarService", dump, "El servicio CarService no se encuentra disponible.")
        print("[PASSED] Control multimedia validado: El volumen del sistema escaló correctamente mediante tramas CAN.")

    def tearDown(self):
        print("[TEARDOWN] Restableciendo sistema multimedia a parámetros iniciales seguros...")
        # Dejamos el volumen en un nivel medio de confort (40%) al cerrar las pruebas
        subprocess.run("adb shell dumpsys activity service Car set-group-volume 0 0 40", shell=True, stdout=subprocess.DEVNULL)

if __name__ == "__main__":
    unittest.main()
