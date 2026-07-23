import os
import subprocess
import time
import can

def enviar_a_vhal(property_id, value, area_id="0"):
    """Envía el valor al VHAL. Agregamos area_id porque HVAC lo requiere (0 es global/conductor)"""
    # Usamos la sintaxis nativa de tu emulador: inject-vhal-event ID [area_id] data
    comando = f"adb shell dumpsys activity service Car inject-vhal-event {property_id} {area_id} {value}"
    
    try:
        subprocess.run(comando, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[ERROR ADB] No se pudo enviar al VHAL: {e}")

# Inicializar bus virtual
bus = can.interface.Bus(channel='vcan0', interface='virtual')

print("==================================================")
print("SIMULADOR AUTOMOTRIZ: CONTROL DE HVAC Y UNIDADES")
print("==================================================")

try:
    # 1. ENCENDER EL HVAC (ID: 287312384)
    print("[CONFIG] Enviando señal CAN para encender el Climatizador...")
    enviar_a_vhal("287312384", "1")
    time.sleep(1.5)

    # 2. SUBIR LA TEMPERATURA GRADUALMENTE (ID: 289411585)
    # Area ID suele ser 1 (Asiento conductor) o 0 (Global) según el emulador. Usaremos 0 por defecto.
    temperaturas_prueba = ["18.0", "20.5", "22.0", "24.5", "26.0"]
    
    for i, temp in enumerate(temperaturas_prueba, 1):
        print(f"[{i:02d}] Tx CAN: 0x201 -> VHAL Ajustando temperatura a {temp}°C")
        enviar_a_vhal("289411585", temp)
        time.sleep(1.5) # Pausa para que aprecies el cambio visual en pantalla

    # 3. CAMBIAR UNIDADES DE DISTANCIA (ID: 289408514)
    print("\n[CONFIG] Enviando señal CAN para alternar unidades de medida...")
    
    print("[06] Tx CAN: 0x301 -> VHAL Cambiando a MILLAS (MPH / Miles)")
    enviar_a_vhal("289408514", "3") # 3 = Imperial (Millas)
    time.sleep(3.0)
    
    print("[07] Tx CAN: 0x301 -> VHAL Restableciendo a KILÓMETROS (KM/H)")
    enviar_a_vhal("289408514", "2") # 2 = Métrico (Kilómetros)
    time.sleep(1.5)

finally:
    bus.shutdown()
    print("\n[STOP] Simulación interactiva de confort completada con éxito.")
