from machine import Pin, SPI, PWM
import framebuf
import time

class LCD_1inch14(framebuf.FrameBuffer):
    def __init__(self, bl_pin=7, dc_pin=8, cs_pin=10, sck_pin=12, mosi_pin=11, rst_pin=9):
        self.width = 240
        self.height = 135
        self.bl = Pin(bl_pin, Pin.OUT)
        self.dc = Pin(dc_pin, Pin.OUT)
        self.cs = Pin(cs_pin, Pin.OUT)
        self.rst = Pin(rst_pin, Pin.OUT)
        self.cs(1)
        self.spi = SPI(1, baudrate=20_000_000, polarity=0, phase=0, 
                       sck=Pin(sck_pin), mosi=Pin(mosi_pin), miso=None)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        self.pwm = PWM(self.bl)
        self.pwm.freq(1000)
        self.set_backlight(100)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()

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
        
        
    def set_backlight(self, brightness):
        duty = int(65535 * brightness / 100)
        self.pwm.duty_u16(duty)

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

    def reorder_rgb565(self, color):
        red = (color >> 11) & 0b11111
        green = (color >> 5) & 0b111111
        blue = color & 0b11111
        reordered_color = (blue << 11) | (red << 5) | green
        return reordered_color

    def _adjust_color(self, color):
        return self.reorder_rgb565(color)

    def fill_color(self, color):
        adjusted_color = self._adjust_color(color)
        self.fill(adjusted_color)
        self.show()

    def draw_pixel(self, x, y, color):
        if 0 <= x < self.width and 0 <= y < self.height:
            adjusted_color = self._adjust_color(color)
            super().pixel(x, y, adjusted_color)

    def draw_line(self, x1, y1, x2, y2, color):
        """
        Dibuja una línea entre dos puntos con el color ajustado.
        """
        # Diferencias en las coordenadas
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        # Dibujar la línea
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
                
                
    def draw_circle(self, x0, y0, radius, color, fill=False):
        """
        Dibuja un círculo.
        Parámetros:
        - x0, y0: Coordenadas del centro del círculo.
        - radius: Radio en píxeles.
        - color: Color en formato RGB565.
        - fill: Si es True, llena el círculo. Por defecto, False.
        """
        if fill:
            # Dibujar un círculo lleno
            for y in range(-radius, radius + 1):
                for x in range(-radius, radius + 1):
                    if x**2 + y**2 <= radius**2:  # Ecuación del círculo
                        self.draw_pixel(x0 + x, y0 + y, color)
        else:
            # Dibujar solo los bordes del círculo
            x = 0
            y = radius
            d = 3 - (2 * radius)
            while x <= y:
                # Dibujar los puntos en los ocho octantes
                self.draw_pixel(x0 + x, y0 + y, color)
                self.draw_pixel(x0 - x, y0 + y, color)
                self.draw_pixel(x0 + x, y0 - y, color)
                self.draw_pixel(x0 - x, y0 - y, color)
                self.draw_pixel(x0 + y, y0 + x, color)
                self.draw_pixel(x0 - y, y0 + x, color)
                self.draw_pixel(x0 + y, y0 - x, color)
                self.draw_pixel(x0 - y, y0 - x, color)

                if d < 0:
                    d += (4 * x) + 6
                else:
                    d += (4 * (x - y)) + 10
                    y -= 1
                x += 1

    def draw_square(self, x0, y0, side, color, fill=False):
        """
        Dibuja un cuadrado.
        Parámetros:
        - x0, y0: Coordenadas de la esquina superior izquierda.
        - side: Tamaño del lado del cuadrado.
        - color: Color en formato RGB565.
        - fill: Si es True, llena el cuadrado. Por defecto, False.
        """
        if fill:
            # Dibujar un cuadrado lleno
            for x in range(x0, x0 + side):
                for y in range(y0, y0 + side):
                    self.draw_pixel(x, y, color)
        else:
            # Dibujar solo los bordes del cuadrado
            for x in range(x0, x0 + side):
                self.draw_pixel(x, y0, color)            # Línea superior
                self.draw_pixel(x, y0 + side - 1, color)  # Línea inferior
            for y in range(y0, y0 + side):
                self.draw_pixel(x0, y, color)            # Línea izquierda
                self.draw_pixel(x0 + side - 1, y, color)  # Línea derecha

    def draw_triangle(self, x1, y1, x2, y2, x3, y3, color, fill=False):
        """
        Dibuja un triángulo.
        Parámetros:
        - x1, y1: Coordenadas del primer vértice.
        - x2, y2: Coordenadas del segundo vértice.
        - x3, y3: Coordenadas del tercer vértice.
        - color: Color en formato RGB565.
        - fill: Si es True, llena el triángulo. Por defecto, False.
        """
        if fill:
            # Ordenar los vértices por coordenada Y (y1 <= y2 <= y3)
            if y1 > y2:
                x1, y1, x2, y2 = x2, y2, x1, y1
            if y2 > y3:
                x2, y2, x3, y3 = x3, y3, x2, y2
            if y1 > y2:
                x1, y1, x2, y2 = x2, y2, x1, y1

            # Dibujar líneas horizontales entre los bordes
            def interpolate(y_start, y_end, x_start, x_end):
                """Interpolar puntos entre dos coordenadas."""
                if y_start == y_end:  # Evitar división por cero
                    return []
                delta_x = x_end - x_start
                delta_y = y_end - y_start
                step = delta_x / delta_y
                x = x_start
                points = []
                for y in range(y_start, y_end + 1):
                    points.append((int(x), y))
                    x += step
                return points

            # Interpolaciones para los bordes del triángulo
            edge1 = interpolate(y1, y2, x1, x2)
            edge2 = interpolate(y2, y3, x2, x3)
            edge3 = interpolate(y1, y3, x1, x3)

            # Combinar los puntos y rellenar las líneas horizontales
            edges = edge1 + edge2 + edge3
            edges.sort(key=lambda point: point[1])  # Ordenar por coordenada Y

            for i in range(len(edges) - 1):
                y = edges[i][1]
                if edges[i][1] == edges[i + 1][1]:  # Mismo Y
                    x_start = min(edges[i][0], edges[i + 1][0])
                    x_end = max(edges[i][0], edges[i + 1][0])
                    for x in range(x_start, x_end + 1):
                        self.draw_pixel(x, y, color)
        else:
            # Dibujar solo los bordes del triángulo
            self.draw_line(x1, y1, x2, y2, color)  # Línea entre (x1, y1) y (x2, y2)
            self.draw_line(x2, y2, x3, y3, color)  # Línea entre (x2, y2) y (x3, y3)
            self.draw_line(x3, y3, x1, y1, color)  # Línea entre (x3, y3) y (x1, y1)
            
            
    def draw_shape(self, points, color, fill=False):
        """
        Dibuja una forma basada en una lista de puntos.
        Parámetros:
        - points: Lista de tuplas [(x1, y1), (x2, y2), ..., (xn, yn)] que representan los vértices.
        - color: Color en formato RGB565.
        - fill: Si es True, llena la forma. Por defecto, False.
        """
        if len(points) < 3:
            raise ValueError("Se necesitan al menos 3 puntos para formar una forma.")

        if fill:
            # Rellenar la forma usando el algoritmo de escaneo
            sorted_points = sorted(points, key=lambda p: p[1])  # Ordenar por coordenada Y
            y_min = sorted_points[0][1]
            y_max = sorted_points[-1][1]

            for y in range(y_min, y_max + 1):
                intersections = []
                for i in range(len(points)):
                    x1, y1 = points[i]
                    x2, y2 = points[(i + 1) % len(points)]  # Conectar el último punto con el primero

                    # Verificar si la línea cruza la línea de escaneo
                    if y1 <= y < y2 or y2 <= y < y1:
                        x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                        intersections.append(int(x))

                intersections.sort()  # Ordenar las intersecciones por X

                # Dibujar líneas horizontales entre pares de intersecciones
                for i in range(0, len(intersections), 2):
                    if i + 1 < len(intersections):
                        x_start = intersections[i]
                        x_end = intersections[i + 1]
                        for x in range(x_start, x_end + 1):
                            self.draw_pixel(x, y, color)
        else:
            # Dibujar los bordes conectando los puntos en orden
            for i in range(len(points)):
                x1, y1 = points[i]
                x2, y2 = points[(i + 1) % len(points)]  # Conectar el último punto con el primero
                self.draw_line(x1, y1, x2, y2, color)

