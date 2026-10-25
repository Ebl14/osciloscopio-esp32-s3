import serial
import time

# Configura tu puerto COM aquí y la velocidad de 2.000.000 baudios
PUERTO_COM = "COM5"  
BAUDIOS = 2000000

try:
    print(f"Intentando conectar al puerto {PUERTO_COM}...")
    esp32 = serial.Serial(PUERTO_COM, BAUDIOS, timeout=1)
    print("¡Conexión exitosa! Leyendo datos...")
    
    while True:
        if esp32.in_waiting > 0:
            # Lee la línea que llega desde el ESP32
            linea = esp32.readline().decode('utf-8').strip()
            if linea:
                print(f"Paquete recibido (64 muestras): {linea[:50]}... (truncado)")
                
except serial.SerialException as e:
    print(f"Error de conexión: {e}")
except KeyboardInterrupt:
    print("\nLectura detenida por el usuario.")
finally:
    if 'esp32' in locals() and esp32.is_open:
        esp32.close()
        print("Puerto cerrado correctamente.")