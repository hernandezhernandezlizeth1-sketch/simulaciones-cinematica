import pygame
import math
from simulacion import Proyectil

# Paleta Dark Mode Científico
BG_COLOR = (32, 33, 35)         
PANEL_COLOR = (43, 44, 48)      
TEXT_COLOR = (240, 240, 240)
GREEN_NEON = (57, 255, 20)
BLUE_ACCENT = (88, 166, 255)    
ORANGE_ACCENT = (255, 158, 59)
GRAY_LINE = (70, 70, 80)
SLIDER_BG = (63, 63, 70)

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, start_val):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.val = start_val
        self.dragging = False

    def draw(self, superficie):
        pygame.draw.rect(superficie, SLIDER_BG, self.rect, border_radius=self.rect.height//2)
        ratio = (self.val - self.min_val) / (self.max_val - self.min_val)
        ancho_relleno = int(ratio * self.rect.width)
        if ancho_relleno > 0:
            rect_relleno = pygame.Rect(self.rect.x, self.rect.y, ancho_relleno, self.rect.height)
            pygame.draw.rect(superficie, BLUE_ACCENT, rect_relleno, border_radius=self.rect.height//2)
        knob_x = self.rect.x + ancho_relleno
        pygame.draw.circle(superficie, TEXT_COLOR, (knob_x, self.rect.centery), int(self.rect.height * 0.8))

    def manejar_eventos(self, evento):
        modificado = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evento.pos):
                self.dragging = True
                modificado = True
        elif evento.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif evento.type == pygame.MOUSEMOTION:
            if self.dragging:
                rel_x = max(0, min(evento.pos[0] - self.rect.x, self.rect.width))
                ratio = rel_x / self.rect.width
                self.val = self.min_val + ratio * (self.max_val - self.min_val)
                modificado = True
        return modificado

def dibujar_cuadricula(pantalla, offsetX, offsetY, ancho, alto, espacio):
    for x in range(offsetX, ancho, espacio):
        pygame.draw.line(pantalla, GRAY_LINE, (x, 0), (x, alto), 1)
    for y in range(0, alto, espacio):
        if y > offsetY:
            pygame.draw.line(pantalla, GRAY_LINE, (offsetX, y), (ancho, y), 1)

def renderizar():
    pygame.init()
    ancho, alto = 1000, 600
    panel_w = 360
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Animación de Cinemática del Punto")
    reloj = pygame.time.Clock()
    
    fuente_titulo = pygame.font.SysFont("Segoe UI", 24, bold=True)
    fuente_math = pygame.font.SysFont("Segoe UI", 18, italic=True)
    fuente_ui = pygame.font.SysFont("Segoe UI", 16)

    # Inicia en X ajustado al panel, Y en el suelo (500)
    proyectil = Proyectil(panel_w + 40, 500)
    
    # Sliders
    slider_v = Slider(30, 150, 240, 10, 20.0, 200.0, 90.0)
    slider_a = Slider(30, 230, 240, 10, 0.0, 90.0, 45.0)
    slider_g = Slider(30, 310, 240, 10, 20.0, 300.0, 98.0)

    corriendo = True
    while corriendo:
        dt = reloj.tick(60) / 1000.0
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            
            # Si mueves un slider, la simulación se reinicia para previsualizar
            v_mod = slider_v.manejar_eventos(evento)
            a_mod = slider_a.manejar_eventos(evento)
            g_mod = slider_g.manejar_eventos(evento)
            
            if v_mod or a_mod or g_mod:
                proyectil.detener()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    proyectil.disparar()

        # Actualizar variables desde los sliders
        proyectil.vel_inicial = slider_v.val
        proyectil.angulo_grados = slider_a.val
        proyectil.gravedad = slider_g.val

        proyectil.actualizar(dt)

        # Cálculos de datos físicos
        angulo_rad = math.radians(proyectil.angulo_grados)
        v0y = proyectil.vel_inicial * math.sin(angulo_rad)
        v0x = proyectil.vel_inicial * math.cos(angulo_rad)
        
        tiempo_total_teorico = (2 * v0y) / proyectil.gravedad
        distancia_max = v0x * tiempo_total_teorico
        altura_max = (v0y ** 2) / (2 * proyectil.gravedad)

        # --- DIBUJO ---
        pantalla.fill(BG_COLOR)
        
        # Cuadrícula del área de simulación
        dibujar_cuadricula(pantalla, panel_w, 0, ancho, alto, 40)

        # Suelo
        pygame.draw.line(pantalla, TEXT_COLOR, (panel_w, 500), (ancho, 500), 2)

        # Cañón (Línea indicadora)
        fin_canon_x = proyectil.x0 + 40 * math.cos(angulo_rad)
        fin_canon_y = proyectil.y0 - 40 * math.sin(angulo_rad)
        pygame.draw.line(pantalla, ORANGE_ACCENT, (proyectil.x0, proyectil.y0), (fin_canon_x, fin_canon_y), 4)

        # Dibujar Trayectoria Proyectada (Línea punteada)
        puntos_trayectoria = proyectil.obtener_trayectoria_proyectada()
        if len(puntos_trayectoria) > 1:
            pygame.draw.aalines(pantalla, GRAY_LINE, False, puntos_trayectoria)

        # Dibujar Proyectil actual
        pygame.draw.circle(pantalla, GREEN_NEON, (int(proyectil.x), int(proyectil.y)), 8)
        pygame.draw.circle(pantalla, GREEN_NEON, (int(proyectil.x), int(proyectil.y)), 14, 2) # Brillo

        # --- PANEL UI ---
        pygame.draw.rect(pantalla, PANEL_COLOR, (0, 0, panel_w, alto))
        pygame.draw.rect(pantalla, (20, 20, 22), (0, 0, panel_w, alto), 2) # Borde del panel

        tit = fuente_titulo.render("Cinemática del Punto", True, TEXT_COLOR)
        pantalla.blit(tit, (30, 30))
        
        sub = fuente_math.render("Tiro Parabólico Interactivo", True, BLUE_ACCENT)
        pantalla.blit(sub, (30, 65))

        # Dibujar Controles
        textos_sliders = [
            (f"Velocidad Inicial (v0): {slider_v.val:.1f} px/s", 125, slider_v),
            (f"Ángulo de Disparo (θ): {slider_a.val:.1f}°", 205, slider_a),
            (f"Gravedad (g): {slider_g.val:.1f} px/s²", 285, slider_g)
        ]

        for texto, pos_y, slider_obj in textos_sliders:
            sup_texto = fuente_ui.render(texto, True, TEXT_COLOR)
            pantalla.blit(sup_texto, (30, pos_y))
            slider_obj.draw(pantalla)

        # Separador
        pygame.draw.line(pantalla, GRAY_LINE, (30, 360), (panel_w - 30, 360), 1)

        # Datos en tiempo real
        sup_datos_tit = fuente_ui.render("Datos Físicos (Predicción):", True, ORANGE_ACCENT)
        pantalla.blit(sup_datos_tit, (30, 380))

        datos = [
            f"Altura Máxima: {altura_max:.1f} px",
            f"Alcance Máximo: {distancia_max:.1f} px",
            f"Tiempo de Vuelo: {tiempo_total_teorico:.2f} s"
        ]
        
        for i, dato in enumerate(datos):
            sup_dato = fuente_ui.render(dato, True, TEXT_COLOR)
            pantalla.blit(sup_dato, (30, 415 + i * 25))

        # Botón / Instrucción
        pygame.draw.rect(pantalla, BLUE_ACCENT, (30, 520, panel_w - 60, 40), border_radius=5)
        sup_btn = fuente_titulo.render("PRESIONA ESPACIO", True, BG_COLOR)
        pantalla.blit(sup_btn, (75, 525))

        pygame.display.flip()

    pygame.quit()