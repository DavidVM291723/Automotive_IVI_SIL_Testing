import subprocess
import time
import can

def enviar_comando_vhal(comando):
    """Envía comandos de telemática al emulador"""
    try:
        subprocess.run(comando, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[ERROR ADB] {e}")

# Inicializar bus virtual
bus = can.interface.Bus(channel='vcan0', interface='virtual')

print("==================================================")
print("SIMULADOR CAN: TELEMÁTICA (LLAMADA ENTRANTE)")
print("==================================================")

try:
    print("[TELEMÁTICA ACTIVA] Detectando señal de red celular...")
    print(" -> Tx CAN: 0x3E8 | Estado: EVENTO DE LLAMADA DETECTADO")
    print(" -> Tx CAN: 0x3E9 | Remitente: +15551234567")
    
    # Lanzar la interfaz de llamada/marcado en el infoentretenimiento
    enviar_comando_vhal("adb shell am start-activity -a android.intent.action.DIAL -d tel:+15551234567")
    time.sleep(3.0)

finally:
    bus.shutdown()
