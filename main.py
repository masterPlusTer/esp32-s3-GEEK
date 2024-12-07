from GEEK import LCD_1inch14

### codigo para probar lo que hay hasta ahora, descomentar la linea de codigo para probar el funcionamiento

# Inicializar la pantalla
lcd = LCD_1inch14()



#lcd.fill_color(0b1111100000000000)  # rojo
#lcd.fill_color(0b0000011111100000)  # verde
#lcd.fill_color(0b0000000000011111)  # azul



#lcd.fill_color(0b0000000000000000)  # Limpiar pantalla (negro)
#lcd.fill_color(0b1111111111111111)  # Limpiar pantalla (blanco)


#lcd.draw_line(5, 5, 225, 5, 0b0000011111100000)  # Línea horizontal verde
#lcd.draw_line(5, 5, 5, 125, 0b0000000000011111)  # Línea vertical azul
#lcd.draw_line(5, 5, 225, 125, 0b1111100000000000)  # Línea diagonal verde roja

# Dibujar un píxel rojo
lcd.draw_pixel(10, 10, 0b1111100000000000)  # Rojo

# Dibujar un píxel verde
lcd.draw_pixel(20, 20, 0b0000011111100000)  # Verde

# Dibujar un píxel azul
lcd.draw_pixel(30, 30, 0b0000000000011111)  # Azul

# Actualizar la pantalla para reflejar los cambios



#lcd.fill_color(0b1111100000000000)  # Rojo
#lcd.fill_color(0b0000011111100000)  # verde
#lcd.fill_color(0xfff) 

#lcd.draw_line(10, 10, 10, 100, 0b0000011111100000)  # verde

#lcd.draw_line(10, 10, 10, 100, 0b1111100000000000)  # rojo
#lcd.draw_line(10, 10, 10, 100, 0b0000000000011111)  # azul
lcd.draw_line(10, 10, 10, 100, 0b0000011111100000)  # verde


lcd.draw_pixel(10, 10, 0b0000011111100000)  # Verde

lcd.draw_circle(120, 70, 30, 0b0000011111100000)  # Dibuja el círculo con centro en (120, 70) y radio 30 píxeles

lcd.draw_square(50, 30, 40, 0x07E0)  # Cuadrado verde
lcd.draw_square(50, 30, 40, 0x07E0, fill=True)  # Cuadrado verde lleno
lcd.draw_circle(120, 67, 50, 0xF800, fill=True)  # Círculo rojo lleno

#lcd.draw_triangle(50, 50, 150, 50, 100, 100, 0x001F, fill=True)  # Azul
lcd.draw_triangle(50, 50, 150, 50, 100, 100, 0x001F)  # Azul


#lcd.draw_shape([(60, 60), (120, 50), (180, 60), (150, 100), (90, 100)], 0x001F, fill=True)  # Pentágono azul lleno
lcd.draw_shape([(60, 60), (120, 50), (180, 60), (150, 100), (90, 100)], 0b000011111100000, fill=True)  # Pentágono verde lleno







lcd.show()
