import subprocess
import time
import can

def enviar_sos_vhal():
    """Inyecta el comando de disparo de llamada de emergencia (eCall)"""
    # En entornos automotrices, las llamadas de emergencia usan la acción CALL_PRIVILEGED o el marcado SOS directo
    comando = "adb shell am start-activity -a android.intent.action.CALL -d tel:911"
    try:
        subprocess.run(comando, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[ERROR ADB] {e}")

# Inicializar bus virtual
bus = can.interface.Bus(channel='vcan0', interface='virtual')

print("==================================================")
print("SIMULADOR CAN: SISTEMA DE TELEMÁTICA eCALL (SOS)")
print("==================================================")

try:
    print("[EVENTO CRÍTICO] Colisión detectada por sensores de impacto...")
    print(" -> Tx CAN: 0x050 | Airbag Status: DEPLOYED (Desplegado)")
    print(" -> Tx CAN: 0x051 | eCall Module: Iniciando llamada de emergencia automatizada...")
    
    enviar_sos_vhal()
    time.sleep(3.0)

finally:
    bus.shutdown()
