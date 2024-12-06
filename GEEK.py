from machine import Pin, SPI, PWM  # Para manejo de pines GPIO, comunicación SPI y señales PWM
import framebuf  # Biblioteca para manipular buffers gráficos
import time  # Biblioteca para manejar pausas y tiempos






# Definición de la clase LCD_1inch14 que extiende FrameBuffer
class LCD_1inch14(framebuf.FrameBuffer):
    def __init__(self, bl_pin=7, dc_pin=8, cs_pin=10, sck_pin=12, mosi_pin=11, rst_pin=9):
        """
        Constructor para inicializar el display LCD de 1.14 pulgadas.
        Parámetros:
        - bl_pin: Pin GPIO para controlar la retroiluminación.
        - dc_pin: Pin GPIO para diferenciar comandos de datos.
        - cs_pin: Pin GPIO para la selección del chip en el bus SPI.
        - sck_pin: Pin GPIO para la señal de reloj del bus SPI.
        - mosi_pin: Pin GPIO para la señal de datos del bus SPI.
        - rst_pin: Pin GPIO para reiniciar el display.
        """
        self.width = 240  # Ancho en píxeles del display
        self.height = 135  # Alto en píxeles del display

        # Configuración de pines del LCD
        self.bl = Pin(bl_pin, Pin.OUT)  # Retroiluminación como salida
        self.dc = Pin(dc_pin, Pin.OUT)  # Pin de datos/comandos como salida
        self.cs = Pin(cs_pin, Pin.OUT)  # Selección del chip como salida
        self.rst = Pin(rst_pin, Pin.OUT)  # Reset como salida

        # Configuración de comunicación SPI
        self.cs(1)  # Inicialmente desactiva el chip seleccionando nivel alto
        self.spi = SPI(1, baudrate=20_000_000, polarity=0, phase=0, 
                       sck=Pin(sck_pin), mosi=Pin(mosi_pin), miso=None)  # Inicialización del bus SPI
        self.dc(1)  # Inicializa el pin DC en modo datos
        self.buffer = bytearray(self.height * self.width * 2)  # Buffer de memoria para el contenido del display

        # Configuración de la retroiluminación mediante PWM
        self.pwm = PWM(self.bl)  # Activa el PWM en el pin de retroiluminación
        self.pwm.freq(1000)  # Configura la frecuencia del PWM en 1 kHz
        self.set_backlight(100)  # Establece el brillo máximo por defecto

        # Inicialización de la clase base FrameBuffer con el buffer definido
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)

        # Llama a la inicialización del hardware del display
        self.init_display()

    def write_cmd(self, cmd):
        """
        Envía un comando al controlador del display.
        Parámetro:
        - cmd: Byte de comando a enviar.
        """
        self.cs(1)  # Desactiva el chip momentáneamente
        self.dc(0)  # Configura el pin DC en modo comando
        self.cs(0)  # Activa el chip seleccionando nivel bajo
        self.spi.write(bytearray([cmd]))  # Envía el comando por SPI
        self.cs(1)  # Desactiva el chip tras completar la operación

    def write_data(self, data):
        """
        Envía datos al controlador del display.
        Parámetro:
        - data: Puede ser un byte o una lista de bytes.
        """
        self.cs(1)  # Desactiva el chip momentáneamente
        self.dc(1)  # Configura el pin DC en modo datos
        self.cs(0)  # Activa el chip seleccionando nivel bajo
        if isinstance(data, int):  # Si es un solo byte
            self.spi.write(bytearray([data]))  # Envía el byte como dato
        else:  # Si es una lista de bytes
            self.spi.write(bytearray(data))  # Envía todos los bytes como datos
        self.cs(1)  # Desactiva el chip tras completar la operación



    def init_display(self):
       
        
        """
        Inicialización del display mediante comandos específicos.
        Configura parámetros como orientación, formato de píxeles, etc.
        """
        self.rst(1)  # Activa el reset
        time.sleep(0.1)  # Espera 100 ms
        self.rst(0)  # Desactiva el reset
        time.sleep(0.1)  # Espera 100 ms
        self.rst(1)  # Activa el reset nuevamente
        time.sleep(0.1)  # Espera 100 ms

        # Secuencia de comandos para inicialización del controlador
        self.write_cmd(0x36)
        self.write_data(0x70)  # Configura la orientación de la memoria gráfica

        self.write_cmd(0x3A)
        self.write_data(0x05)  # Formato de píxeles: 16 bits por píxel (RGB565)

        # Configuración de tiempos, voltajes y otros parámetros
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

        self.write_cmd(0x21)  # Activa modo inverso de color
        self.write_cmd(0x11)  # Salida del modo sleep
        time.sleep(0.1)  # Espera para asegurar la estabilidad
        self.write_cmd(0x29)  # Encender el display
        
       
    def set_backlight(self, brightness):
        """
        Configura el brillo de la retroiluminación.
        Parámetro:
        - brightness: Valor de 0 a 100 que representa el porcentaje de brillo.
        """
        duty = int(65535 * brightness / 100)  # Convierte porcentaje a duty cycle
        self.pwm.duty_u16(duty)  # Ajusta el PWM según el duty cycle calculado

    def show(self):
        """
        Actualiza la pantalla enviando el contenido del buffer al display.
        """
        self.write_cmd(0x2A)
        self.write_data([0x00, 0x28, 0x01, 0x17])  # Define el rango de columnas

        self.write_cmd(0x2B)
        self.write_data([0x00, 0x35, 0x00, 0xBB])  # Define el rango de filas

        self.write_cmd(0x2C)  # Indica que se comenzará a enviar datos de la memoria
        self.cs(1)  # Desactiva el chip temporalmente
        self.dc(1)  # Configura DC para datos
        self.cs(0)  # Activa el chip para enviar los datos
        self.spi.write(self.buffer)  # Envía todo el buffer al display
        self.cs(1)  # Desactiva el chip
    
    def reorder_rgb565(self, color):
        """
        Reordena los bits RGB565 para mover los últimos 6 bits (verde y azul) al centro y ajusta los colores.
        """
        # Extraer los bits individuales
        red = (color >> 11) & 0b11111       # Bits 15-11: Rojo
        green = (color >> 5) & 0b111111     # Bits 10-5: Verde
        blue = color & 0b11111              # Bits 4-0: Azul

        # Reorganizar los componentes:
        # Rojo y azul están invertidos en tu caso, los reordenamos adecuadamente
        reordered_color = (blue << 11) | (red << 5) | green
        return reordered_color



    def fill_color(self, color):
        """Llenar pantalla con un color."""
        adjusted_color = self.reorder_rgb565(color)  # Reorganiza el color
        #self.fill(color)
        self.fill(adjusted_color)
        self.show()

    def draw_pixel(self, x, y, color):
        """
        Dibuja un píxel en una posición específica con el color corregido.
        """
        if 0 <= x < self.width and 0 <= y < self.height:  # Verifica que las coordenadas sean válidas
            adjusted_color = self.reorder_rgb565(color)  # Corrige el color
            super().pixel(x, y, adjusted_color)  # Llama al método pixel de framebuf con el color corregido
        else:
            raise ValueError("Coordenadas fuera del rango (0-239, 0-134)")

    
    def draw_line(self, x1, y1, x2, y2, color):
        """
        Dibuja una línea entre dos puntos con el color corregido.
        """
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            self.draw_pixel(x1, y1, color)  # Usa draw_pixel para garantizar el ajuste de color
            if x1 == x2 and y1 == y2:  # Si llega al final, termina
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
