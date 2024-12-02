from GEEK import LCD_1inch14

# Inicializar la pantalla
lcd = LCD_1inch14()

# Llenar la pantalla con color blanco
lcd.fill_color(0xFFFF)

# Dibujar líneas en la pantalla
lcd.draw_line(10, 10, 100, 10, 0xF800)  # Línea horizontal roja
lcd.draw_line(10, 10, 10, 100, 0x07E0)  # Línea vertical verde
lcd.draw_line(10, 10, 100, 100, 0x001F)  # Línea diagonal azul

# Mostrar los cambios
lcd.show()
