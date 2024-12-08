intentando incluir en una unica libreria ( GEEK.py) todo lo necesario para poder controlar el esp32-s3-geek. 
Hasta ahora solo tengo hecho la parte del display, quizas los colores al momento de mostrar el bmp no son perfectos pero al menos ya hay una interface mas o menos amigable para empezar a dibujar formas , figuras y escribir texto.

TO DO LIST:
mi intencion es agregar clases para trabajar con la conectividad wifi y bluetooth y quizas tambien integrar una clase para trabajar con la tarjeta SD aunque no prometo nada porque ya he estado intentandolo por todos los medios y no hay con que darle...

este dispositivo es muy vistoso pero programarlo es una pesadilla, y lo que funciona en micropython no funciona en circuitpython y se hace imposible integrar en un unico programa todo lo que el esp32s3-geek tiene para ofrecer.

por ahora esto es lo que hay. 
me voy a poner a adaptar esto mismo para circuit python ya que alli quizas si sea posible mostrar en el display datos de la sd ... en fin...

esto esta en construccion, sepan disculpar el desorden

################################################################################################################################################################

# Documentación de la librería LCD_1inch14 para MicroPython

## Introducción
Esta librería permite controlar una pantalla LCD de 1.14 pulgadas utilizando MicroPython. Ofrece funciones para inicializar el dispositivo, manejar el brillo, dibujar figuras geométricas, mostrar texto e imágenes, y realizar tareas de visualización. Es ideal para usuarios que deseen implementar interfaces gráficas en proyectos embebidos.

---

## Inicialización del dispositivo

### Clase: `LCD_1inch14`

#### Parámetros del constructor
```python
LCD_1inch14(bl_pin=7, dc_pin=8, cs_pin=10, sck_pin=12, mosi_pin=11, rst_pin=9)
```
- **bl_pin**: Pin para el control de retroiluminación.
- **dc_pin**: Pin para datos/comandos.
- **cs_pin**: Pin para selección de chip.
- **sck_pin**: Pin del reloj SPI.
- **mosi_pin**: Pin para datos SPI.
- **rst_pin**: Pin para reiniciar la pantalla.

#### Ejemplo
```python
from LCD_1inch14 import LCD_1inch14
lcd = LCD_1inch14()
```

---

## Funciones principales

### 1. Configuración del brillo
```python
lcd.set_backlight(brightness)
```
- **Parámetro**:
  - `brightness`: Nivel de brillo en porcentaje (0-100).

#### Ejemplo
```python
lcd.set_backlight(50)  # Configura el brillo al 50%
```

---

### 2. Mostrar el contenido del buffer
```python
lcd.show()
```
Actualiza la pantalla con el contenido actual del buffer de memoria.

#### Ejemplo
```python
lcd.show()
```

---

### 3. Dibujar en la pantalla

#### Dibujar un píxel
```python
lcd.draw_pixel(x, y, color)
```
- **Parámetros**:
  - `x`, `y`: Coordenadas del píxel.
  - `color`: Color en formato RGB565.

#### Ejemplo
```python
lcd.draw_pixel(10, 10, 0xFFFF)  # Píxel blanco en (10, 10)
```

#### Dibujar una línea
```python
lcd.draw_line(x1, y1, x2, y2, color)
```
- **Parámetros**:
  - `x1`, `y1`: Coordenadas iniciales.
  - `x2`, `y2`: Coordenadas finales.
  - `color`: Color en formato RGB565.

#### Ejemplo
```python
lcd.draw_line(0, 0, 100, 100, 0xF800)  # Línea roja diagonal
```

#### Dibujar figuras geométricas

- **Cuadrado**:
  ```python
  lcd.draw_square(x0, y0, side, color, fill=False)
  ```
  - `x0, y0`: Coordenadas superiores izquierdas.
  - `side`: Tamaño del lado.
  - `color`: Color en RGB565.
  - `fill`: Relleno opcional (True o False).

- **Rectángulo**:
  ```python
  lcd.draw_rectangle(x0, y0, width, height, color, fill=False)
  ```

- **Círculo**:
  ```python
  lcd.draw_circle(x0, y0, radius, color, fill=False)
  ```

- **Triángulo**:
  ```python
  lcd.draw_triangle(x1, y1, x2, y2, x3, y3, color, fill=False)
  ```

#### Ejemplo
```python
lcd.draw_square(10, 10, 50, 0x07E0, fill=True)  # Cuadrado verde relleno
```

---

### 4.  Texto
```python
lcd.draw_text(x, y, text, color)
```
- **Parámetros**:
  - `x`, `y`: Coordenadas superiores izquierdas.
  - `text`: Cadena de texto a mostrar.
  - `color`: Color en formato RGB565.

#### Ejemplo
```python
lcd.draw_text(10, 20, "Hola Mundo", 0xFFFF)  # Texto blanco
```

---

### 5. Mostrar imágenes BMP
```python
lcd.draw_bmp(file_path, x, y)
```
- **Parámetros**:
  - `file_path`: Ruta del archivo BMP.
  - `x`, `y`: Coordenadas superiores izquierdas.

#### Ejemplo
```python
lcd.draw_bmp("imagen.bmp", 0, 0)
```

---

### 6. Rellenar con un color
```python
lcd.fill_color(color)
```
- **Parámetro**:
  - `color`: Color en formato RGB565.

#### Ejemplo
```python
lcd.fill_color(0x0000)  # Pantalla completamente negra
```

---

## Código de ejemplo completo

```python
from GEEK import LCD_1inch14
lcd = LCD_1inch14()

# Configurar brillo
lcd.set_backlight(80)

# Dibujar figuras
lcd.fill_color(0x0000)  # Fondo negro
lcd.draw_circle(120, 67, 30, 0xF800, fill=True)  # Círculo rojo
lcd.draw_text(50, 100, "Hola!", 0x07E0)  # Texto verde
lcd.show()
```

---

## Notas adicionales
1. El formato de color RGB565 utiliza 16 bits:
   - 5 bits para rojo.
   - 6 bits para verde.
   - 5 bits para azul.

2.  La biblioteca está diseñada para pantallas basadas en controladores ST7789.

