from flask import Flask, render_template, jsonify, request
import serial
import threading

app = Flask(__name__)

# Configuración del puerto
PUERTO_COM = "COM5"
BAUDIOS = 115200

# Variables globales para almacenar la última ventana de 64 muestras
latest_data = {"canal1": [0]*64, "canal2": [0]*64}
esp32 = serial.Serial(PUERTO_COM, BAUDIOS, timeout=1)

def leer_puerto_serie():
    global latest_data
    while True:
        try:
            linea = esp32.readline().decode('utf-8', errors='ignore').strip()
            if linea:
                muestras = linea.split('|')
                c1, c2 = [], []
                for m in muestras:
                    valores = m.split(',')
                    if len(valores) == 2 and valores[0].isdigit() and valores[1].isdigit():
                        c1.append(int(valores[0]))
                        c2.append(int(valores[1]))
                
                # Relajamos la condición: si llegan al menos la mitad de las muestras, las graficamos
                if len(c1) > 32 and len(c2) > 32:
                    # Rellenamos hasta 64 repitiendo el último valor si el paquete se cortó
                    while len(c1) < 64: c1.append(c1[-1])
                    while len(c2) < 64: c2.append(c2[-1])
                    
                    latest_data = {"canal1": c1[:64], "canal2": c2[:64]}
                    
                    # Imprime en la terminal lo que está leyendo físicamente el Pin 4
                    print(f"Voltaje Pin 4: {c1[0]} | Voltaje Pin 5: {c2[0]}")
                    
                    esp32.reset_input_buffer() 
        except Exception:
            pass
# Iniciar la lectura serial en segundo plano
threading.Thread(target=leer_puerto_serie, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    return jsonify(latest_data)

@app.route('/api/command', methods=['POST'])
def send_command():
    comando = request.json.get('cmd')
    if comando in ['1', '2', '3']:
        esp32.write(comando.encode())
        return jsonify({"status": "Comando enviado: " + comando})
    return jsonify({"status": "Error"})

if __name__ == '__main__':
    # use_reloader=False evita que el puerto COM se abra dos veces al reiniciar
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)