import board
import busio
import time

# Configurar los pines UART
uart = busio.UART(board.TX, board.RX, baudrate=115200)

while True:
    if uart.in_waiting > 0:
        data = uart.readline()
        print(data)
        time.sleep(0.1)  # Pequeña pausa para evitar sobrecargar el buffer
