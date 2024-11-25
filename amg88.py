#esto es una porqueria, estoy trabajando en esto no esta terminado, lo que pasa que el esp32 s3 geek es muy lindo pero no es intuitivo para nada, no es beginer friendly en absoluto entonces no se logra redondear un proyecto ni con ayuda de la IA , en  fin


from machine import Pin, SPI, PWM, I2C
import framebuf
from micropython_amg88xx import AMG88XX
import time

# Pines del LCD
BL = 7
DC = 8
CS = 10
SCK = 12
MOSI = 11
RST = 9

# Configuración del I2C
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)

# Inicializar el sensor
try:
    sensor = AMG88XX(i2c)
    print("Sensor AMG8833 inicializado correctamente.")
except Exception as e:
    print(f"Error al inicializar el sensor: {e}")
    sensor = None

class LCD_1inch14(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 240
        self.height = 135
        
        self.cs = Pin(CS, Pin.OUT)
        self.rst = Pin(RST, Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1, 1000_000)
        self.spi = SPI(1, 50_000_000, polarity=0, phase=0, sck=Pin(SCK), mosi=Pin(MOSI), miso=None)
        self.dc = Pin(DC, Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)

        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
    
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        if isinstance(buf, list):
            for b in buf:
                self.cs(1)
                self.dc(1)
                self.cs(0)
                self.spi.write(bytearray([b]))
                self.cs(1)
        else:
            self.cs(1)
            self.dc(1)
            self.cs(0)
            self.spi.write(bytearray([buf]))
            self.cs(1)

    def init_display(self):
        self.rst(1)
        time.sleep(0.1)
        self.rst(0)
        time.sleep(0.1)
        self.rst(1)
        time.sleep(0.1)
        
        self.write_cmd(0x36)
        self.write_data(0x70)
        self.write_cmd(0x3A)
        self.write_data(0x05)
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
    
    def show(self):
        self.write_cmd(0x2C)
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
    
    def draw_rectangle(self, x, y, w, h, color):
        for i in range(x, x + w):
            for j in range(y, y + h):
                self.pixel(i, j, color)

    def draw_text(self, x, y, text, color):
        self.text(text, x, y, color)

def temperature_to_color(temp, min_temp=20, max_temp=40):
    temp = max(min_temp, min(max_temp, temp))
    scale = (temp - min_temp) / (max_temp - min_temp)
    if scale < 0.5:
        red = int(31 * (scale * 2))
        green = int(63 * scale)
        blue = 31
    else:
        red = 31
        green = int(63 * (1 - scale))
        blue = int(31 * (1 - scale))
    return (red << 11) | (green << 5) | blue

if __name__ == '__main__':
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(65535)

    LCD = LCD_1inch14()
    
    if sensor:
        while True:
            try:
                temperatures = sensor.pixels
                LCD.fill(0x0000)
                pixel_size = 28  # Ajustar para que quepa en el LCD
                for i, row in enumerate(temperatures):
                    for j, temp in enumerate(row):
                        color = temperature_to_color(temp)
                        LCD.draw_rectangle(j * pixel_size, i * pixel_size, pixel_size, pixel_size, color)
                        LCD.draw_text(j * pixel_size + 5, i * pixel_size + 5, str(i * 8 + j), 0x0000)
                LCD.show()
                time.sleep(1)
            except Exception as e:
                print(f"Error: {e}")
