import subprocess
import time
import can

def enviar_comando_vhal(comando):
    """Envía comandos de control de infoentretenimiento al emulador"""
    try:
        subprocess.run(comando, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[ERROR ADB] {e}")

# Inicializar bus virtual
bus = can.interface.Bus(channel='vcan0', interface='virtual')

print("==================================================")
print("SIMULADOR CAN: MANDOS AL VOLANTE (INFOTAINMENT)")
print("==================================================")

try:
    print("[MANDOS ACTIVER] Conductor interactúa con los botones del volante...")
    
    # 1. Simular subida de volumen mediante comando de zona de audio (Zona 0, Grupo de volumen 0, fijar en 60%)
    print(" -> Tx CAN: 0x2A0 | Comando: SUBIR VOLUMEN (Fijar en 60%)")
    enviar_comando_vhal("adb shell dumpsys activity service Car set-group-volume 0 0 60")
    time.sleep(1.5)
    
    # 2. Simular pulsación física del botón 'Siguiente Canción' (KeyEvent 87)
    print(" -> Tx CAN: 0x2A1 | Comando: BOTÓN PISTA SIGUIENTE (Key 87)")
    enviar_comando_vhal("adb shell dumpsys activity service Car inject-key 87")
    time.sleep(1.5)

finally:
    bus.shutdown()
