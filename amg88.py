import time
import board
import busio
from adafruit_amg88xx import AMG88XX

# Configuración del bus I2C
print("Iniciando bus I2C...")
i2c = busio.I2C(board.SCL, board.SDA)
time.sleep(1)

# Escaneo I2C con manejo de bloqueos
print("Escaneando dispositivos I2C...")
while not i2c.try_lock():
    pass

try:
    devices = i2c.scan()
    print("Dispositivos detectados:", [hex(device) for device in devices])
finally:
    i2c.unlock()

# Inicializar el sensor AMG88
try:
    amg88 = AMG88XX(i2c)
    print("Sensor AMG88 conectado correctamente.")
except ValueError as e:
    print("Error al inicializar el AMG88:", e)
    print("Verifica las conexiones del sensor.")
    raise

# Mostrar datos del sensor en el LCD
print("\n*** Visualización en el LCD ***\n")
try:
    while True:
        # Limpiar pantalla con líneas vacías
        print("\033c", end="")  # Esto limpia el LCD (ANSI escape para "limpiar pantalla")

        # Título decorativo
        print("=== Temperaturas del AMG88 ===")
        print("-----------------------------")

        # Leer y mostrar la matriz de temperaturas
        for row in amg88.pixels:
            print(" ".join(["{:5.1f}".format(temp) for temp in row]))  # Formatear filas
        print("\nActualizando en 1s...\n")
        time.sleep(1)
except KeyboardInterrupt:
    print("Interrumpido por el usuario.")
except Exception as e:
    print("Error al leer datos del AMG88:", e)

