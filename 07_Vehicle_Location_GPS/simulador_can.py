import subprocess
import time
import can

def enviar_coordenadas_vhal(longitud, latitud):
    """Inyecta coordenadas utilizando el servicio nativo de localización de Android"""
    # Formato nativo: cmd location set-location-properties gps --location lat,lon,alt,precision
    # Usaremos altitud 10.0 y precisión 1.0 como datos estándar de telemetría CAN
    comando = f"adb shell cmd location set-location-properties gps --location {latitud},{longitud},10.0,1.0"
    try:
        subprocess.run(comando, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[ERROR ADB] {e}")

# Inicializar bus virtual
bus = can.interface.Bus(channel='vcan0', interface='virtual')

print("==================================================")
print("SIMULADOR CAN: RECEPCIÓN DE TELEMETRÍA GPS / RUTA")
print("==================================================")

try:
    coordenadas_ruta = [
        ("-99.133208", "19.432608"),  
        ("-99.134208", "19.433608"),  
        ("-99.135208", "19.434608")   
    ]
    
    print("[TELEMÁTICA GPS] Transmitiendo tramas de posicionamiento satelital...")
    for i, (lon, lat) in enumerate(coordenadas_ruta, 1):
        print(f" -> Tx CAN: 0x410 | Satélites: 8 | Coordenadas: Lon {lon}, Lat {lat}")
        enviar_coordenadas_vhal(lon, lat)
        time.sleep(1.5)

finally:
    bus.shutdown()
