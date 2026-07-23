import subprocess
import time
import can

def enviar_a_vhal(property_id, value):
    """Inyecta el estado en el emulador de Android usando configuración global (Area 0)"""
    comando = f"adb shell dumpsys activity service Car inject-vhal-event {property_id} 0 {value}"
    try:
        subprocess.run(comando, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[ERROR ADB] {e}")

# Inicializar bus virtual
bus = can.interface.Bus(channel='vcan0', interface='virtual')

print("==================================================")
print("SIMULADOR CAN: CONFLICTO DE FRENO DE MANO Y MARCHA")
print("==================================================")

try:
    print("[RIESGO SIMULADO] Conductor intenta avanzar con el Freno de Mano puesto...")
    
    # 1. Poner Freno de Mano Activo (ID: 287310850, Valor: 1)
    enviar_a_vhal("287310850", "1")
    time.sleep(1)
    
    # 2. Cambiar marcha a Drive (ID: 289408000, Valor: 8)
    enviar_a_vhal("289408000", "8")
    
    print(" -> Tx CAN: 0x120 | Freno de Mano: CONFIGURADO EN ACTIVO")
    print(" -> Tx CAN: 0x101 | Marcha Seleccionada: DRIVE")
    time.sleep(2)

finally:
    bus.shutdown()
