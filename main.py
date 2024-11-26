from GEEK import LCD

lcd = LCD()
lcd.llenar_pantalla(0xFFE0)  # Llenar pantalla con amarillo
lcd.dibujar_circulo(160, 120, 50, 0xF800)  # Dibujar un círculo rojo en el centro
lcd.dibujar_circulo(150, 130, 50, 0xF800)  # Dibujar un círculo rojo en el centro
lcd.dibujar_linea(50, 50, 250, 200, 0x07E0)  # Línea verde
lcd.dibujar_linea(250, 50, 50, 200, 0xF800)  # Línea roja


lcd.llenar_pantalla(0x0000)  # Fondo negro
lcd.dibujar_triangulo(60, 60, 260, 60, 160, 200, 0xFFFF)  # Triángulo blanco
