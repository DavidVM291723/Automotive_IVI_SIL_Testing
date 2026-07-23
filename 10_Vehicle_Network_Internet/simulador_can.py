import subprocess
import time
import can

def conmutar_datos_vehiculo(estado):
    """Controla el estado del módem de datos interno del auto"""
    comando = f"adb shell svc data {estado}"
    try:
        subprocess.run(comando, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[ERROR ADB] {e}")

# Inicializar bus virtual
bus = can.interface.Bus(channel='vcan0', interface='virtual')

print("==================================================")
print("SIMULADOR CAN: CONECTIVIDAD DE RED DE A BORDO")
print("==================================================")

try:
    print("[ESCENARIO 1] Vehículo ingresa a zona sin cobertura (Túnel)...")
    print(" -> Tx CAN: 0x450 | TCU Módem: SIGNAL_LOST (0x00)")
    conmutar_datos_vehiculo("disable")
    time.sleep(3.0) # Tiempo en modo offline
    
    print("\n[ESCENARIO 2] Vehículo sale del túnel y recupera red LTE/5G...")
    print(" -> Tx CAN: 0x450 | TCU Módem: SIGNAL_RESTORED (0x01)")
    conmutar_datos_vehiculo("enable")
    time.sleep(1.5)

finally:
    bus.shutdown()
