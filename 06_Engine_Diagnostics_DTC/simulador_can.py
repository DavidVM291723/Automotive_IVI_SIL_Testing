import subprocess
import time
import can

def enviar_error_vhal(property_id, zone, error_code):
    """Inyecta un evento de error de hardware directo en el VHAL de Android"""
    comando = f"adb shell dumpsys activity service Car inject-error-event {property_id} {zone} {error_code}"
    try:
        subprocess.run(comando, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[ERROR ADB] {e}")

# Inicializar bus virtual
bus = can.interface.Bus(channel='vcan0', interface='virtual')

print("==================================================")
print("SIMULADOR CAN: DIAGNÓSTICO DE MOTOR (DTC / OBD2)")
print("==================================================")

try:
    print("[ALERTA CRÍTICA] Sensor del motor reporta falla de presión/temperatura...")
    print(" -> Tx CAN: 0x7DF | Query: UDS Request Diagnostic Trouble Codes")
    print(" -> Tx CAN: 0x7E8 | Response: DTC P0117 - Engine Coolant Temp Circuit Low")
    
    # Inyectamos el error en la propiedad del motor (ID: 299896832, Zona: 0, Código Error: 3 [STATUS_MALFUNCTION])
    enviar_error_vhal("299896832", "0", "3")
    time.sleep(2.0)

finally:
    bus.shutdown()
