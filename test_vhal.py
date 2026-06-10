import subprocess
import time

def ejecutar_adb(comando):
    return subprocess.check_output(f"adb shell {comando}", shell=True).decode("utf-8").strip()

def test_ultimate_set():
    print("\n" + "="*60)
    print("TEST DE INYECCIÓN DIRECTA - SINTAXIS SET-PROPERTY")
    print("="*60)

    # 1. Intentar el cambio usando 'set-property-value' (Nueva sintaxis A15)
    # Sintaxis: set-property-value <ID> <Area> <Valor>
    print("[ACTION] Forzando GEAR_DRIVE (8) con SET...")
    ejecutar_adb("cmd car_service set-property-value 0x11400400 0 8")
    
    print("[ACTION] Forzando SPEED (100.0) con SET...")
    ejecutar_adb("cmd car_service set-property-value 0x11600207 0 100.0")
    
    time.sleep(2)

    # 2. Verificación
    res_gear = ejecutar_adb("cmd car_service get-property-value 0x11400400 0")
    print(f"\nResultado en VHAL: {res_gear}")

    if "8" in res_gear or "DRIVE" in res_gear:
        print("\nRESULTADO: [ PASS ] - ¡La sintaxis SET funcionó!")
    else:
        print("\nRESULTADO: [ FAIL ] - El VHAL de esta imagen es Read-Only.")
        print("Tip: Intenta ejecutar 'adb root' en tu terminal antes de correr el script.")

if __name__ == "__main__":
    test_ultimate_set()
