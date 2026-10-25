# Osciloscopio Híbrido ESP32-S3

Este repositorio contiene el código fuente, la configuración y la documentación para la implementación de un sistema de adquisición de señales analógicas (osciloscopio híbrido) de dos canales, utilizando un ESP32-S3 y un servidor local.

## 1. Descripción Detallada del Proyecto
El proyecto consiste en un sistema de instrumentación que captura ventanas de 64 muestras de dos señales analógicas a través de los pines 4 y 5 del ESP32-S3. Los datos son enviados mediante comunicación Serial (UART) a un ordenador que actúa como servidor backend (Flask/Python). Finalmente, una interfaz web reactiva (HTML/Chart.js) consume estos datos y grafica las formas de onda en tiempo real, con una tasa de refresco de 1 Hz. 

El sistema cuenta con tres presets de frecuencia de muestreo: 100 Sa/s, 1.000 Sa/s y 10.000 Sa/s.

### Diagramas
- **Diagrama de Bloques:** 
  ![Diagrama de Bloques](Diagrama%20de%20bloques%20(1).png)

- **Diagrama de Flujo:** 
  ![Diagrama de Flujo](Diagrama%20de%20flujo.png)

## 2. Requerimientos y Restricciones (Justificación Técnica)
* **Requerimiento original:** Uso de SBC (Raspberry Pi) y comunicación SPI.
* **Restricción y adaptación:** Debido a la falta de disponibilidad de hardware SBC dedicado, se empleó un computador personal con Windows operando como host (SBC lógico). En consecuencia, al carecer de pines SPI físicos directos entre el ESP32 y el PC, la capa de transporte se adaptó para utilizar UART sobre USB (115,200 baudios), garantizando la estabilidad de la transmisión de las ventanas de 64 muestras requeridas.

## 3. Análisis Teórico de Transferencia
Aunque se implementó comunicación UART, se realizó el análisis teórico exigido para SPI según el Datasheet del ESP32-S3:
* **SPI (Teórico):** El ESP32-S3 soporta frecuencias de reloj SPI de hasta 80 MHz. En modo estándar (1 bit por ciclo), la tasa teórica máxima es de 80 Mbps (10 MB/s). 
* **UART (Implementado):** Se configuró a 115,200 bps. Enviando paquetes de 64 muestras (~150 bytes por trama), la red soporta sobradamente la actualización del dashboard a 1 Hz, requiriendo apenas una fracción del ancho de banda disponible (aprox. 1,200 bps de uso real).

## 4. Instrucciones de Configuración e Instalación

### Hardware (Firmware ESP32-S3)
1. Abrir el entorno Arduino IDE.
2. Seleccionar la placa **ESP32S3 Dev Module**.
3. **Paso crítico:** En el menú "Herramientas", configurar *Flash Mode* en **QIO 80MHz**.
4. Cargar el código `.ino` al microcontrolador.

### Software (Servidor Flask y Dashboard)
1. Instalar Python 3.x.
2. Instalar las dependencias en la terminal: `pip install flask pyserial`
3. Conectar el ESP32-S3 al PC y verificar el puerto asignado (ej. `COM5`).
4. Actualizar el puerto COM en el script de Python si es necesario.
5. Ejecutar el servidor: `python servidor.py`
6. Abrir un navegador web en `http://localhost:5000` (o la ruta correspondiente al archivo HTML local).

## 5. Matriz de Verificación
Los resultados detallados de las pruebas (Línea base a 0V, saturación a 3.3V, acoplamiento capacitivo y atenuación) se encuentran documentados en el informe técnico en formato IEEE adjunto en este repositorio (`Informe_IEEE.pdf`).

## 6. Roles y Declaración de Participación
* **Esteban Becerra Loaiza:** Desarrollo del firmware del ESP32, codificación del servidor Flask, diseño de la interfaz web en Chart.js, ejecución de pruebas de integración, redacción del documento en Typst y control de versiones en Git.
* *(Si tienes compañeros, añade sus nombres y qué hicieron. Si estuviste solo, deja solo tu nombre)*.

## 7. Declaración de Uso de Inteligencia Artificial
* **Modelo utilizado:** Gemini 1.5 Pro.
* **Tareas específicas:** 
  1. Depuración del error de reinicio constante del ESP32 (diagnóstico y corrección del modo de memoria a QIO 80MHz).
  2. Estructuración y formato del código Typst para generar el informe bajo el estándar IEEE a doble columna.
  3. Soporte en comandos de terminal para inicializar y sincronizar el repositorio local con GitHub.
* **Verificación:** Todos los códigos y configuraciones sugeridas fueron verificados experimentalmente cargándolos en el microcontrolador y visualizando el dashboard. Se verificó que el documento compilado en Typst cumpliera con la rúbrica visual IEEE.
