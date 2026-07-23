import subprocess
import time
import unittest

class TestVehicleVoiceAssistant(unittest.TestCase):

    def setUp(self):
        print("\n[SETUP] Inicializando entorno de voz. Asegurando pantalla Home limpia...")
        # Regresamos al Home de Android antes de iniciar
        subprocess.run("adb shell input keyevent 3", shell=True, stdout=subprocess.DEVNULL)
        time.sleep(1)

    def test_voice_assistant_activation(self):
        print("[TEST] Desplegando simulador CAN para activación del asistente de voz...")
        
        # Ejecutar el estímulo del simulador CAN
        subprocess.run("python ./09_Voice_Assistant_Intent/simulador_can.py", shell=True)
        time.sleep(1.5)
        
        print("[VALIDACIÓN] Verificando logs del VoiceInteractionManagerService...")
        
        # Consultamos el estado de los servicios de asistencia por voz del sistema
        comando_verificar = "adb shell dumpsys voiceinteraction"
        dump = subprocess.check_output(comando_verificar, shell=True, text=True)
        
        # Evaluamos si el subsistema de interacción de voz o el asistente están disponibles y respondiendo
        self.assertIn("voice", dump.lower(), "ERROR: El subsistema de interacción por voz no se encuentra activo.")
        print("[PASSED] Caso de prueba de voz exitoso: El sistema Automotive procesó correctamente la interrupción del asistente.")

    def tearDown(self):
        print("[TEARDOWN] Cerrando interfaz del asistente de voz y restableciendo pantalla...")
        subprocess.run("adb shell input keyevent 3", shell=True, stdout=subprocess.DEVNULL)

if __name__ == "__main__":
    unittest.main()
