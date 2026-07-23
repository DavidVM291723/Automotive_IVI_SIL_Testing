import subprocess
import time
import can

def enviar_evento_voz_vhal():
    """Inyecta el evento de pulsación del botón de comando de voz del volante"""
    # Usamos el comando nativo del servicio Car para inyectar la tecla KEYCODE_VOICE_ASSIST
    comando = "adb shell dumpsys activity service Car inject-key 231"
    try:
        subprocess.run(comando, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[ERROR ADB] {e}")

# Inicializar bus virtual
bus = can.interface.Bus(channel='vcan0', interface='virtual')

print("==================================================")
print("SIMULADOR CAN: BOTÓN DE COMANDO DE VOZ AL VOLANTE")
print("==================================================")

try:
    print("[MANDOS AL VOLANTE] Conductor presiona el botón de interacción por voz...")
    print(" -> Tx CAN: 0x2B5 | Botón: VOICE_ASSIST_PRESSED (Estado: Activo)")
    print(" -> Tx CAN: 0x2B5 | Enviando interrupción al CarService de Android...")
    
    enviar_evento_voz_vhal()
    time.sleep(2.0)

finally:
    bus.shutdown()
