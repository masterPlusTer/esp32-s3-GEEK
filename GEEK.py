from machine import Pin, SPI
import time

class LCD:
    def __init__(self):
        # Configuración de pines del LCD
        self.BL = 7     # Luz de fondo
        self.DC = 8     # Dato o comando
        self.CS = 10    # Selección del chip
        self.SCK = 12   # Reloj SPI
        self.MOSI = 11  # Datos SPI
        self.RST = 9    # Reset del LCD

        # Configuración de dimensiones
        self.ancho = 320
        self.alto = 240

        # Inicialización del SPI
        self.spi = SPI(1, baudrate=10_000_000, polarity=0, phase=0, sck=Pin(self.SCK), mosi=Pin(self.MOSI))

        # Pines de control
        self.cs = Pin(self.CS, Pin.OUT)
        self.dc = Pin(self.DC, Pin.OUT)
        self.rst = Pin(self.RST, Pin.OUT)
        self.bl = Pin(self.BL, Pin.OUT)
        self.bl.value(1)  # Encender backlight

        # Inicializar el LCD
        self.inicializar()

    def escribir_comando(self, cmd):
        self.cs(1)
        self.dc(0)  # Modo comando
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def escribir_datos(self, data):
        self.cs(1)
        self.dc(1)  # Modo datos
        self.cs(0)
        self.spi.write(bytearray([data]) if isinstance(data, int) else bytearray(data))
        self.cs(1)

    def inicializar(self):
        self.rst(1)
        time.sleep(0.1)
        self.rst(0)
        time.sleep(0.1)
        self.rst(1)
        time.sleep(0.1)

        # Comandos de inicialización del LCD
        self.escribir_comando(0x36)  # Dirección de memoria
        self.escribir_datos(0x70)
        self.escribir_comando(0x3A)  # Formato de píxeles
        self.escribir_datos(0x05)
        self.escribir_comando(0xB2)  # Timing
        self.escribir_datos([0x0C, 0x0C, 0x00, 0x33, 0x33])
        self.escribir_comando(0xB7)  # Voltaje de entrada
        self.escribir_datos(0x35)
        self.escribir_comando(0xBB)
        self.escribir_datos(0x19)
        self.escribir_comando(0xC0)  # Fuente de alimentación
        self.escribir_datos(0x2C)
        self.escribir_comando(0xC2)
        self.escribir_datos(0x01)
        self.escribir_comando(0xC3)
        self.escribir_datos(0x12)
        self.escribir_comando(0xC4)
        self.escribir_datos(0x20)
        self.escribir_comando(0xC6)  # Ajuste de gama
        self.escribir_datos(0x0F)
        self.escribir_comando(0xD0)
        self.escribir_datos([0xA4, 0xA1])
        self.escribir_comando(0xE0)  # Gama positiva
        self.escribir_datos([0xD0, 0x04, 0x0D, 0x11, 0x13, 0x2B, 0x3F, 0x54, 0x4C, 0x18, 0x0D, 0x0B, 0x1F, 0x23])
        self.escribir_comando(0xE1)  # Gama negativa
        self.escribir_datos([0xD0, 0x04, 0x0C, 0x11, 0x13, 0x2C, 0x3F, 0x44, 0x51, 0x2F, 0x1F, 0x1F, 0x20, 0x23])
        self.escribir_comando(0x21)  # Modo de visualización
        self.escribir_comando(0x11)  # Salir de sleep
        time.sleep(0.1)
        self.escribir_comando(0x29)  # Encender el display

    def llenar_pantalla(self, color):
        self.escribir_comando(0x2A)  # Rango de columna
        self.escribir_datos([0x00, 0x00, 0x01, 0x3F])  # 320 píxeles de ancho
        self.escribir_comando(0x2B)  # Rango de fila
        self.escribir_datos([0x00, 0x00, 0x00, 0xEF])  # 240 píxeles de alto
        self.escribir_comando(0x2C)  # Escribir memoria
        for _ in range(320 * 240):  # Llenar cada píxel con el color dado
            self.escribir_datos([color >> 8, color & 0xFF])

    def dibujar_pixel(self, x, y, color):
        self.escribir_comando(0x2A)
        self.escribir_datos([x >> 8, x & 0xFF, x >> 8, x & 0xFF])
        self.escribir_comando(0x2B)
        self.escribir_datos([y >> 8, y & 0xFF, y >> 8, y & 0xFF])
        self.escribir_comando(0x2C)
        self.escribir_datos([color >> 8, color & 0xFF])

    def dibujar_circulo(self, xc, yc, r, color):
        x = 0
        y = r
        d = 3 - 2 * r  # Decisión inicial en el algoritmo de Bresenham
        self._dibujar_puntos_circulo(xc, yc, x, y, color)
        
        while y >= x:
            x += 1
            if d > 0:
                y -= 1
                d += 4 * (x - y) + 10
            else:
                d += 4 * x + 6
            self._dibujar_puntos_circulo(xc, yc, x, y, color)

    def _dibujar_puntos_circulo(self, xc, yc, x, y, color):
        # Dibujar los ocho puntos simétricos del círculo
        self.dibujar_pixel(xc + x, yc + y, color)
        self.dibujar_pixel(xc - x, yc + y, color)
        self.dibujar_pixel(xc + x, yc - y, color)
        self.dibujar_pixel(xc - x, yc - y, color)
        self.dibujar_pixel(xc + y, yc + x, color)
        self.dibujar_pixel(xc - y, yc + x, color)
        self.dibujar_pixel(xc + y, yc - x, color)
        self.dibujar_pixel(xc - y, yc - x, color)

    def dibujar_linea(self, x1, y1, x2, y2, color):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            self.dibujar_pixel(x1, y1, color)  # Dibujar el píxel actual
            if x1 == x2 and y1 == y2:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def dibujar_triangulo(self, x1, y1, x2, y2, x3, y3, color):
        # Dibujar las tres líneas que forman el triángulo
        self.dibujar_linea(x1, y1, x2, y2, color)
        self.dibujar_linea(x2, y2, x3, y3, color)
        self.dibujar_linea(x3, y3, x1, y1, color)
