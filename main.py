from GEEK import LCD_1inch14

### codigo para probar lo que hay hasta ahora, descomentar la linea de codigo para probar el funcionamiento



lcd = LCD_1inch14()
#lcd.fill_color(0b1111100000000000)  # Rojo
#lcd.fill_color(0b0000011111100000)  # verde
#lcd.fill_color(0xfff) 

#lcd.draw_line(10, 10, 10, 100, 0b0000011111100000)  # verde

#lcd.draw_line(10, 10, 10, 100, 0b1111100000000000)  # rojo
#lcd.draw_line(10, 10, 10, 100, 0b0000000000011111)  # azul
#lcd.draw_line(10, 10, 10, 100, 0b0000011111100000)  # verde


#lcd.draw_pixel(10, 10, 0b0000011111100000)  # Verde

lcd.draw_circle(120, 70, 30, 0b0000011111100000)  # Dibuja el círculo con centro en (120, 70) y radio 30 píxeles

#lcd.draw_square(50, 30, 40, 0x07E0)  # Cuadrado verde
#lcd.draw_square(50, 30, 40, 0x07E0, fill=True)  # Cuadrado verde lleno
#lcd.draw_circle(120, 67, 50, 0xF800, fill=True)  # Círculo rojo lleno

#lcd.draw_triangle(50, 50, 150, 50, 100, 100, 0x001F, fill=True)  # Azul
lcd.draw_triangle(50, 50, 150, 50, 100, 100, 0b1111100000000000)  # rojo


#lcd.draw_shape([(60, 60), (120, 50), (180, 60), (150, 100), (90, 100)], 0x001F, fill=True)  # Pentágono azul lleno
#lcd.draw_shape([(60, 60), (120, 50), (180, 60), (150, 100), (90, 100)], 0b000011111100000, fill=True)  # Pentágono verde lleno

#lcd.draw_rectangle(50, 50, 100, 60, 0xF800, fill=True)  # Rectángulo rojo lleno
#lcd.draw_oval(120, 67, 50, 30, 0b0000000000011111, fill=True)  # Óvalo azul lleno
#lcd.draw_oval(120, 67, 50, 30, 0b0000000000011111)  # Óvalo azul 

#lcd.draw_trapezoid(50, 50, 150, 50, 120, 100, 80, 100, 0x001F, fill=True)  # Trapecio azul lleno
#lcd.draw_trapezoid(50, 50, 150, 50, 120, 100, 80, 100, 0x001F)  # Trapecio azul solo borde

########## TEXTO ! U.U ######################33

lcd.draw_text(50, 50, "ESTO ES", 0x07E0)  # Texto verde
lcd.draw_text(120, 70, "UNA PORQUERIA", 0x001F)  # Texto azul

lcd.show()




