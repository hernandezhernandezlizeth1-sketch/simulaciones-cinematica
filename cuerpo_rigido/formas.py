import pygame
import math

def dibujar_rueda(superficie, x, y, radio, angulo, color=(100, 200, 255)):
    # Dibuja el borde de la rueda
    pygame.draw.circle(superficie, color, (x, y), radio, 4)
    # Dibuja un radio como línea de referencia para observar la rotación
    fin_x = x + radio * math.cos(angulo)
    fin_y = y + radio * math.sin(angulo)
    pygame.draw.line(superficie, color, (x, y), (fin_x, fin_y), 4)