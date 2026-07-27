import subprocess
import time
import can

def send_coordinates_to_vhal(longitude, latitude):
    """Injects geographical coordinates directly into the Android Location service"""
    command = f"adb shell cmd location set-location-properties gps --location {latitude},{longitude},10.0,1.0"
    try:
        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[ADB ERROR] {e}")

bus = can.interface.Bus(channel='vcan0', interface='virtual')

print("==================================================")
print("CAN SIMULATOR: GPS TELEMETRY & ROUTE TRACKING")
print("==================================================")

try:
    route_coordinates = [
        ("-99.133208", "19.432608"),  
        ("-99.134208", "19.433608"),  
        ("-99.135208", "19.434608")   
    ]
    
    print("[TELEMATICS GPS] Broadcasting satellite positioning tramas...")
    for i, (lon, lat) in enumerate(route_coordinates, 1):
        print(f" -> Tx CAN: 0x410 | Satellites: 8 | Coordinates: Lon {lon}, Lat {lat}")
        send_coordinates_to_vhal(lon, lat)
        time.sleep(1.5)

finally:
    bus.shutdown()
