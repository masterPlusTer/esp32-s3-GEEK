from machine import Pin, SPI, PWM
import framebuf
import time


class LCD_1inch14(framebuf.FrameBuffer):
    def __init__(self, bl_pin=7, dc_pin=8, cs_pin=10, sck_pin=12, mosi_pin=11, rst_pin=9):
        self.width = 240
        self.height = 135

        # Pines del LCD
        self.bl = Pin(bl_pin, Pin.OUT)
        self.dc = Pin(dc_pin, Pin.OUT)
        self.cs = Pin(cs_pin, Pin.OUT)
        self.rst = Pin(rst_pin, Pin.OUT)

        # Configuración SPI
        self.cs(1)
        self.spi = SPI(1, baudrate=20_000_000, polarity=0, phase=0, sck=Pin(sck_pin), mosi=Pin(mosi_pin), miso=None)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)

        # Inicialización de la retroiluminación
        self.pwm = PWM(self.bl)
        self.pwm.freq(1000)
        self.set_backlight(100)  # Brillo máximo por defecto

        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()

    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, data):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        if isinstance(data, int):
            self.spi.write(bytearray([data]))
        else:
            self.spi.write(bytearray(data))
        self.cs(1)

    def init_display(self):
        """Inicialización de la pantalla"""
        self.rst(1)
        time.sleep(0.1)
        self.rst(0)
        time.sleep(0.1)
        self.rst(1)
        time.sleep(0.1)

        # Comandos de inicialización
        self.write_cmd(0x36)
        self.write_data(0x70)  # Configuración de orientación

        self.write_cmd(0x3A)
        self.write_data(0x05)  # Formato de píxeles: 16 bits/pixel

        self.write_cmd(0xB2)
        self.write_data([0x0C, 0x0C, 0x00, 0x33, 0x33])

        self.write_cmd(0xB7)
        self.write_data(0x35)

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F)

        self.write_cmd(0xD0)
        self.write_data([0xA4, 0xA1])

        self.write_cmd(0xE0)
        self.write_data([0xD0, 0x04, 0x0D, 0x11, 0x13, 0x2B, 0x3F, 0x54, 0x4C, 0x18, 0x0D, 0x0B, 0x1F, 0x23])

        self.write_cmd(0xE1)
        self.write_data([0xD0, 0x04, 0x0C, 0x11, 0x13, 0x2C, 0x3F, 0x44, 0x51, 0x2F, 0x1F, 0x1F, 0x20, 0x23])

        self.write_cmd(0x21)
        self.write_cmd(0x11)
        time.sleep(0.1)
        self.write_cmd(0x29)

    def set_backlight(self, brightness):
        """Configurar el brillo de la retroiluminación (0 a 100)"""
        duty = int(65535 * brightness / 100)
        self.pwm.duty_u16(duty)

    def show(self):
        """Actualizar la pantalla"""
        self.write_cmd(0x2A)
        self.write_data([0x00, 0x28, 0x01, 0x17])  # Rango de columnas

        self.write_cmd(0x2B)
        self.write_data([0x00, 0x35, 0x00, 0xBB])  # Rango de filas

        self.write_cmd(0x2C)
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)

    def fill_color(self, color):
        """Llenar la pantalla con un color sólido"""
        self.fill(color)
        self.show()

    def draw_pixel(self, x, y, color):
        """Dibujar un píxel en una posición específica"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixel(x, y, color)
        else:
            raise ValueError("Coordenadas fuera del rango (0-239, 0-134)")

    def draw_line(self, x1, y1, x2, y2, color):
        """Dibujar una línea desde (x1, y1) hasta (x2, y2)"""
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            self.draw_pixel(x1, y1, color)
            if x1 == x2 and y1 == y2:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

