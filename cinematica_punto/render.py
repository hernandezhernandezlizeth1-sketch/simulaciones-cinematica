import pygame
import math
from simulacion import Proyectil

BG_COLOR = (18, 20, 22)
PANEL_COLOR = (28, 30, 34)
TEXT_COLOR = (230, 235, 240)
BLUE_LINE = (0, 160, 255)
GREEN_NEON = (57, 255, 20)
ORANGE = (255, 110, 0)
RED = (255, 60, 60)
YELLOW = (255, 210, 0)

# CONFIGURACIÓN DE ESCALA REAL
PPM = 7.0  # Píxeles por cada Metro real
ORIGEN_PX_X = 330
ORIGEN_PX_Y = 580  # El suelo está abajo

def m_to_px(x_m, y_m):
    x_px = ORIGEN_PX_X + (x_m * PPM)
    y_px = ORIGEN_PX_Y - (y_m * PPM)
    return int(x_px), int(y_px)

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, start_val, label, unit):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val, self.max_val = min_val, max_val
        self.val = start_val
        self.label = label
        self.unit = unit
        self.dragging = False

    def draw(self, surf, font):
        pygame.draw.rect(surf, (55, 55, 60), self.rect, border_radius=4)
        ratio = (self.val - self.min_val) / (self.max_val - self.min_val)
        fill_w = int(ratio * self.rect.width)
        pygame.draw.rect(surf, BLUE_LINE, (self.rect.x, self.rect.y, fill_w, self.rect.height), border_radius=4)
        pygame.draw.circle(surf, (255, 255, 255), (self.rect.x + fill_w, self.rect.centery), 7)
        txt = font.render(f"{self.label}: {self.val:.2f} {self.unit}", True, TEXT_COLOR)
        surf.blit(txt, (self.rect.x, self.rect.y - 22))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.dragging = True; return True
        elif event.type == pygame.MOUSEBUTTONUP: 
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            rel = max(0, min(event.pos[0] - self.rect.x, self.rect.width))
            self.val = self.min_val + (rel / self.rect.width) * (self.max_val - self.min_val)
            return True
        return False

def renderizar():
    pygame.init()
    sw, sh = 1150, 680
    pantalla = pygame.display.set_mode((sw, sh))
    pygame.display.set_caption("Laboratorio de Física de Precisión - Cámara Lenta")
    
    f_ui = pygame.font.SysFont("Consolas", 13)
    f_bold = pygame.font.SysFont("Consolas", 14, bold=True)
    f_title = pygame.font.SysFont("Consolas", 18, bold=True)
    
    proyectil = Proyectil(0.0)
    
    sliders = [
        Slider(30, 80, 240, 8, 5.0, 40.0, 25.0, "Velocidad Inicial (v0)", "m/s"),
        Slider(30, 150, 240, 8, 0.0, 90.0, 45.0, "Ángulo de Disparo (θ)", "°"),
        Slider(30, 220, 240, 8, 0.0, 30.0, 10.0, "Altura Inicial (y0)", "m"),
        Slider(30, 290, 240, 8, 1.0, 20.0, 9.81, "Aceleración Gravedad (g)", "m/s²")
    ]

    reloj = pygame.time.Clock()

    while True:
        dt = reloj.tick(60) / 1000.0 # 60 FPS reales
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return
            movido = False
            for s in sliders:
                if s.handle_event(e): movido = True
            if movido: proyectil.reiniciar()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE: proyectil.disparar()
                if e.key == pygame.K_r: proyectil.reiniciar()
                if e.key == pygame.K_n: proyectil.generar_objetivo()

        # Vincular sliders
        proyectil.vel_inicial = sliders[0].val
        proyectil.angulo_grados = sliders[1].val
        proyectil.altura_inicial = sliders[2].val
        proyectil.gravedad = sliders[3].val
        
        if not proyectil.en_movimiento and not proyectil.hit and proyectil.fase == "PREPARACIÓN":
            proyectil.y_m = proyectil.altura_inicial

        proyectil.actualizar(dt)

        # Matrícula de ecuaciones
        ang_rad = math.radians(proyectil.angulo_grados)
        v0x = proyectil.vel_inicial * math.cos(ang_rad)
        v0y = proyectil.vel_inicial * math.sin(ang_rad)

        # --- RENDER DE ESCENARIO ---
        pantalla.fill(BG_COLOR)
        
        # Malla métrica (Líneas cada 10 metros)
        for m_x in range(0, 120, 10):
            px_x, _ = m_to_px(m_x, 0)
            pygame.draw.line(pantalla, (32, 35, 40), (px_x, 0), (px_x, sh))
            if m_x % 20 == 0:
                pantalla.blit(f_ui.render(f"{m_x}m", True, (90, 95, 100)), (px_x + 3, ORIGEN_PX_Y + 8))
                
        for m_y in range(0, 60, 10):
            _, px_y = m_to_px(0, m_y)
            pygame.draw.line(pantalla, (32, 35, 40), (ORIGEN_PX_X, px_y), (sw, px_y))
            pantalla.blit(f_ui.render(f"{m_y}m", True, (90, 95, 100)), (ORIGEN_PX_X - 35, px_y - 7))

        # Línea de tierra
        pygame.draw.line(pantalla, TEXT_COLOR, (ORIGEN_PX_X, ORIGEN_PX_Y), (sw, ORIGEN_PX_Y), 3)

        # Dibujar Plataforma de Altura Inicial
        if proyectil.altura_inicial > 0:
            base_px_x, base_px_y = m_to_px(0, 0)
            top_px_x, top_px_y = m_to_px(0, proyectil.altura_inicial)
            pygame.draw.rect(pantalla, (60, 65, 75), (base_px_x - 15, top_px_y, 15, base_px_y - top_px_y))
            pygame.draw.line(pantalla, ORANGE, (base_px_x - 15, top_px_y), (base_px_x, top_px_y), 2)

        # Zona Objetivo
        obj_x, obj_y = m_to_px(proyectil.objetivo_x_m, 0)
        ancho_meta = int(5.0 * PPM) 
        color_meta = GREEN_NEON if proyectil.hit else RED
        pygame.draw.rect(pantalla, color_meta, (obj_x - ancho_meta//2, obj_y, ancho_meta, 8))
        pantalla.blit(f_bold.render(f"META: {proyectil.objetivo_x_m:.2f}m", True, color_meta), (obj_x - 40, obj_y + 25))

        # Vector de predicción (Parábola teórica completa)
        pts_m = proyectil.obtener_trayectoria_proyectada()
        pts_px = [m_to_px(pt[0], pt[1]) for pt in pts_m]
        if len(pts_px) > 1: pygame.draw.aalines(pantalla, (70, 75, 80), False, pts_px)

        # Proyectil
        p_x, p_y = m_to_px(proyectil.x_m, proyectil.y_m)
        pygame.draw.circle(pantalla, GREEN_NEON, (p_x, p_y), 8)
        pygame.draw.circle(pantalla, BLUE_LINE, (p_x, p_y), 13, 1)

        # --- INTERFAZ PANEL IZQUIERDO ---
        pygame.draw.rect(pantalla, PANEL_COLOR, (0, 0, 300, sh))
        pygame.draw.rect(pantalla, (15, 15, 15), (0, 0, 300, sh), 3)
        pantalla.blit(f_title.render("PARÁMETROS TIERRA", True, BLUE_LINE), (20, 20))
        
        for s in sliders: s.draw(pantalla, f_ui)
        
        pygame.draw.line(pantalla, (70,70,70), (20, 340), (280, 340))
        pantalla.blit(f_bold.render("CONTROLES:", True, ORANGE), (25, 360))
        pantalla.blit(f_ui.render("[ESPACIO] Lanzar (Cámara Lenta)", True, TEXT_COLOR), (25, 385))
        pantalla.blit(f_ui.render("[R] Reiniciar variables", True, TEXT_COLOR), (25, 410))
        pantalla.blit(f_ui.render("[N] Reubicar objetivo", True, TEXT_COLOR), (25, 435))
        
        # Indicador visual del factor
        pantalla.blit(f_bold.render("VELOCIDAD DEL MOTOR:", True, YELLOW), (25, 480))
        pantalla.blit(f_ui.render(f"Tiempo real desacelerado al 20%", True, TEXT_COLOR), (25, 505))
        pygame.draw.rect(pantalla, YELLOW, (25, 530, 240, 6), border_radius=3)

        # --- EXPLICADOR ANALÍTICO SEGUNDO A SEGUNDO ---
        box_rect = pygame.Rect(320, 20, 480, 175)
        s_box = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
        s_box.fill((10, 10, 12, 230))
        pantalla.blit(s_box, (box_rect.x, box_rect.y))
        pygame.draw.rect(pantalla, BLUE_LINE, box_rect, 2, border_radius=4)

        seg_actual = math.floor(proyectil.tiempo_simulado)
        vy_t = v0y - (proyectil.gravedad * proyectil.tiempo_simulado)

        textos = [
            f"REPORTE: {proyectil.fase}",
            f"Reloj del Proyectil: {proyectil.tiempo_simulado:.2f} segundos",
            f"Posición actual   : X = {proyectil.x_m:.2f}m  |  Y = {proyectil.y_m:.2f}m",
            f"Vectores de Vel.  : Vx = {v0x:.2f}m/s | Vy = {vy_t:.2f}m/s"
        ]

        # Añadir análisis físico dinámico según la línea de tiempo
        if proyectil.fase == "PREPARACIÓN":
            textos.append("FÓRMULA BASE: y(t) = y0 + v0·sin(θ)t - ½gt²")
            textos.append("El proyectil se sitúa estático esperando ignición.")
            color_fase = TEXT_COLOR
        else:
            color_fase = GREEN_NEON if "META" in proyectil.fase else (YELLOW if "ÁPICE" in proyectil.fase else ORANGE)
            if seg_actual == 0:
                textos.append("SITUACIÓN [0s a 1s]: El impulso inicial domina.")
                textos.append("Fórmula horizontal (MRU): x = v0·cos(θ)·t")
            elif seg_actual == 1:
                textos.append("SITUACIÓN [1s a 2s]: La gravedad drena energía.")
                textos.append("Cada segundo Vy disminuye exactamente g m/s.")
            elif seg_actual == 2:
                textos.append("SITUACIÓN [2s a 3s]: Energía potencial en aumento.")
                textos.append("La velocidad en X jamás cambia por la ausencia de aire.")
            elif seg_actual == 3:
                textos.append("SITUACIÓN [3s a 4s]: Curvatura parabólica crítica.")
                textos.append("Ecuación vertical: y = y0 + v0y·t - 0.5·g·t²")
            else:
                textos.append("SITUACIÓN [> 4s]: Descenso por energía gravitatoria.")
                textos.append("El vector Vy apunta hacia abajo y acelera de forma constante.")

        for i, linea in enumerate(textos):
            col = color_fase if i == 0 else TEXT_COLOR
            font = f_bold if i == 0 or i == 4 else f_ui
            pantalla.blit(font.render(linea, True, col), (box_rect.x + 15, box_rect.y + 15 + (i * 24)))

        pygame.display.flip()

    pygame.quit()