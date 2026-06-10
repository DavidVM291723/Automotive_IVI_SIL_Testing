import can
import time
import struct

def simular_mensaje_ciclico_velocidad():
    print("\n" + "="*50)
    print("SIMULADOR CAN OPEN-SOURCE (REPLICA DE CANalyzer)")
    print("="*50)

    try:
        # Configurar canal virtual (vcan0) usando el driver nativo de Linux
        bus = can.interface.Bus(channel='vcan0', interface='socketcan')
        print("[CONFIG] Canal vcan0 inicializado con éxito.")
    except Exception as e:
        print(f"[FALLO] No se pudo abrir vcan0: {e}")
        print("[INFO] Usando canal virtual en memoria para la prueba...")
        bus = can.interface.Bus(channel='test_loopback', interface='virtual')

    # Configuración del mensaje (ID 0x101 - Frecuencia: 100ms)
    # Imaginemos que los primeros 2 bytes representan la velocidad multiplicada por 100 (Factor 0.01)
    id_mensaje = 0x101
    velocidad_objetivo = 100.0 # km/h
    valor_crudo = int(velocidad_objetivo / 0.01) # 10000 en decimal

    # Empaquetamos el valor en 2 bytes (Big Endian '>') y llenamos los otros 6 bytes con ceros (DLC = 8)
    data_bytes = struct.pack('>H', valor_crudo) + b'\x00\x00\x00\x00\x00\x00'

    print(f"\n[START] Transmitiendo Mensaje Cíclico cada 100ms...")
    print(f"-> ID: 0x{id_mensaje:X} | DLC: 8 | Data Cruda: {data_bytes.hex().upper()}")
    print("Presiona Ctrl + C para detener la transmisión.\n")

    try:
        ciclos = 0
        while ciclos < 20:  # Transmitirá durante 2 segundos (20 ciclos de 100ms)
            # Creamos la trama CAN cruda
            msg = can.Message(
                arbitration_id=id_mensaje,
                data=data_bytes,
                is_extended_id=False
            )
            
            bus.send(msg)
            ciclos += 1
            print(f"[{ciclos:02d}] Tx: ID 0x{id_mensaje:X} Data: {data_bytes.hex().upper()}")
            
            time.sleep(0.1) # 100ms (Frecuencia estándar automotriz)
            
        print("\n[STOP] Simulación completada con éxito.")
        
    except KeyboardInterrupt:
        print("\n[STOP] Transmisión detenida por el usuario.")

if __name__ == "__main__":
    simular_mensaje_ciclico_velocidad()
