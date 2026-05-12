import pygame
import math
from simulacion import OsciladorAngular

# Paleta de colores Dark Mode Científico
BG_COLOR = (32, 33, 35)         # Fondo derecho
PANEL_COLOR = (43, 44, 48)      # Fondo izquierdo
TEXT_COLOR = (240, 240, 240)
BLUE_ACCENT = (88, 166, 255)    # Azul estilo neon
GRAY_LINE = (100, 100, 110)
SLIDER_BG = (63, 63, 70)

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, start_val):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.val = start_val
        self.dragging = False

    def draw(self, superficie):
        # Fondo del track
        pygame.draw.rect(superficie, SLIDER_BG, self.rect, border_radius=self.rect.height//2)
        
        # Relleno azul interactivo
        ratio = (self.val - self.min_val) / (self.max_val - self.min_val)
        ancho_relleno = int(ratio * self.rect.width)
        if ancho_relleno > 0:
            rect_relleno = pygame.Rect(self.rect.x, self.rect.y, ancho_relleno, self.rect.height)
            pygame.draw.rect(superficie, BLUE_ACCENT, rect_relleno, border_radius=self.rect.height//2)
        
        # Perilla (Knob)
        knob_x = self.rect.x + ancho_relleno
        pygame.draw.circle(superficie, TEXT_COLOR, (knob_x, self.rect.centery), int(self.rect.height * 0.8))

    def manejar_eventos(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evento.pos):
                self.dragging = True
        elif evento.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif evento.type == pygame.MOUSEMOTION:
            if self.dragging:
                rel_x = max(0, min(evento.pos[0] - self.rect.x, self.rect.width))
                ratio = rel_x / self.rect.width
                self.val = self.min_val + ratio * (self.max_val - self.min_val)

def renderizar():
    pygame.init()
    ancho, alto = 900, 450
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Animación de Velocidad Angular")
    reloj = pygame.time.Clock()
    
    # Fuentes (usamos Segoe UI o Arial para soportar los símbolos ω y θ)
    fuente_math = pygame.font.SysFont("Segoe UI", 48, italic=True)
    fuente_ui = pygame.font.SysFont("Segoe UI", 20)

    sim = OsciladorAngular()
    
    # Slider de Frecuencia (x, y, ancho, alto, min, max, valor_inicial)
    slider_f = Slider(80, 380, 250, 12, 0.1, 5.0, 1.0)

    corriendo = True
    while corriendo:
        dt = reloj.tick(60) / 1000.0
        eventos = pygame.event.get()
        
        for evento in eventos:
            if evento.type == pygame.QUIT:
                corriendo = False
            slider_f.manejar_eventos(evento)

        # Actualizar la simulación con el valor del slider
        sim.frecuencia = slider_f.val
        angulo, y_norm = sim.actualizar(dt)

        # --- DIBUJO ---
        pantalla.fill(BG_COLOR)

        # 1. Panel Izquierdo (Fórmula y Controles)
        pygame.draw.rect(pantalla, PANEL_COLOR, (0, 0, 400, alto))
        pygame.draw.rect(pantalla, (20, 20, 22), (0, 0, 400, alto), 2) # Borde

        # Fórmula matemática centrada
        texto_math = fuente_math.render("ω = dθ / dt", True, TEXT_COLOR)
        pantalla.blit(texto_math, (90, 180))

        # Dibujar Slider
        slider_f.draw(pantalla)
        texto_f = fuente_ui.render(f"f", True, TEXT_COLOR)
        texto_val = fuente_ui.render(f"{slider_f.val:.1f} Hz", True, TEXT_COLOR)
        pantalla.blit(texto_f, (40, 372))
        pantalla.blit(texto_val, (340, 372))

        # 2. Panel Derecho (Gráficos)
        # Configuración del radar/círculo
        centro_x, centro_y = 500, 225
        radio = 45

        # Dibujar círculo base y líneas de eje
        pygame.draw.circle(pantalla, GRAY_LINE, (centro_x, centro_y), radio, 2)
        pygame.draw.circle(pantalla, TEXT_COLOR, (centro_x, centro_y), 3) # Eje central
        pygame.draw.line(pantalla, GRAY_LINE, (centro_x, centro_y), (centro_x + radio, centro_y), 1)

        # Calcular posición del punto que gira
        punto_x = centro_x + math.cos(angulo) * radio
        punto_y = centro_y + math.sin(angulo) * radio

        # Dibujar radio dinámico y punto azul
        pygame.draw.line(pantalla, BLUE_ACCENT, (centro_x, centro_y), (punto_x, punto_y), 3)
        pygame.draw.circle(pantalla, BLUE_ACCENT, (int(punto_x), int(punto_y)), 7)
        # Brillo exterior
        pygame.draw.circle(pantalla, BLUE_ACCENT, (int(punto_x), int(punto_y)), 12, 2)

        # Configuración de la Onda Senoidal
        inicio_onda_x = 600
        ancho_onda = 250
        
        # Línea punteada que conecta el punto con la onda
        for x in range(int(punto_x) + 15, inicio_onda_x, 10):
            pygame.draw.line(pantalla, GRAY_LINE, (x, punto_y), (x + 4, punto_y), 2)

        # Dibujar el eje horizontal del tiempo (0s a 1s)
        pygame.draw.line(pantalla, GRAY_LINE, (inicio_onda_x, centro_y), (inicio_onda_x + ancho_onda + 20, centro_y), 1)
        texto_0s = fuente_ui.render("0 s", True, TEXT_COLOR)
        texto_1s = fuente_ui.render("1 s", True, TEXT_COLOR)
        pantalla.blit(texto_0s, (inicio_onda_x, centro_y + 15))
        pantalla.blit(texto_1s, (inicio_onda_x + ancho_onda, centro_y + 15))

        # Trazar la onda a partir del historial (antialias para que no se vea feo)
        puntos_onda = []
        for i, val_y in enumerate(sim.historial_y):
            # Mapeamos el índice 'i' a una posición 'x' en la pantalla
            x = inicio_onda_x + (i / sim.max_puntos) * ancho_onda
            y = centro_y + val_y * radio
            puntos_onda.append((x, y))

        if len(puntos_onda) > 1:
            pygame.draw.aalines(pantalla, BLUE_ACCENT, False, puntos_onda)
            
            # Punto inicial de la onda (donde conecta la línea punteada)
            pygame.draw.circle(pantalla, BLUE_ACCENT, (int(puntos_onda[0][0]), int(puntos_onda[0][1])), 5)

        pygame.display.flip()

    pygame.quit()