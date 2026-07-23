import os
import subprocess
import time
import can

def enviar_a_vhal(comando):
    """Ejecuta los comandos de inyección en el emulador de forma segura"""
    try:
        subprocess.run(comando, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[ERROR ADB] {e}")

# Inicializar bus virtual
bus = can.interface.Bus(channel='vcan0', interface='virtual')

print("==================================================")
print("CASO DE PRUEBA 02: DRIVER DISTRACTION & UX RESTRICTIONS")
print("==================================================")

try:
    # ESCENARIO 1: El auto arranca y acelera (Detección de movimiento)
    print("\n[ESCENARIO 1] Vehículo inicia marcha. Activando restricciones...")
    
    # CAN 0x102 -> Fijar Marcha en Drive (ID: 289408000, Valor: 8)
    enviar_a_vhal("adb shell dumpsys activity service Car inject-vhal-event 289408000 8")
    
    # CAN 0x110 -> Aceleración simulada (Fijar velocidad alta)
    enviar_a_vhal("adb shell dumpsys activity service Car inject-vhal-event 291504640 85.0")
    
    # Forzar la restricción por distracción en la interfaz gráfica
    enviar_a_vhal("adb shell dumpsys activity service Car enable-uxr true")
    
    print(" -> [ALERTA] Velocidad: 85 km/h | Marcha: DRIVE")
    print(" -> [VHAL] UX Restrictions ENFORCED (Pantalla bloqueada para apps no seguras)")
    time.sleep(5.0) # Tiempo para observar el bloqueo en el emulador

    # ESCENARIO 2: El auto se detiene por completo (Fin del riesgo)
    print("\n[ESCENARIO 2] Vehículo se detiene en semáforo. Liberando restricciones...")
    
    # CAN 0x110 -> Velocidad a 0 km/h
    enviar_a_vhal("adb shell dumpsys activity service Car inject-vhal-event 291504640 0.0")
    
    # CAN 0x102 -> Cambiar a Parking (ID: 289408000, Valor: 4)
    enviar_a_vhal("adb shell dumpsys activity service Car inject-vhal-event 289408000 4")
    
    # Desactivar la restricción por distracción
    enviar_a_vhal("adb shell dumpsys activity service Car enable-uxr false")
    
    print(" -> [INFO] Velocidad: 0 km/h | Marcha: PARKING")
    print(" -> [VHAL] UX Restrictions DISABLED (Pantalla desbloqueada)")
    time.sleep(2.0)

finally:
    bus.shutdown()
    print("\n[STOP] Caso de prueba de distracción completado.")
