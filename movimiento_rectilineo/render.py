import pygame
from simulacion import CarroMRU

# Paleta Dark Mode
BG_COLOR = (25, 27, 30)
PANEL_COLOR = (35, 38, 42)
TEXT_COLOR = (230, 230, 230)
ROAD_COLOR = (50, 52, 56)
ACCENT = (0, 200, 255)
CAR_COLOR = (255, 60, 60)
GREEN_OK = (50, 255, 100)

# Escala: 1 metro = 1.5 píxeles para que quepan los 500m en la pantalla
PPM = 1.5 
ORIGEN_X = 350

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, start_val, label, unit):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val, self.max_val = min_val, max_val
        self.val = start_val
        self.label, self.unit = label, unit
        self.dragging = False

    def draw(self, surf, font):
        pygame.draw.rect(surf, (60, 60, 65), self.rect, border_radius=4)
        ratio = (self.val - self.min_val) / (self.max_val - self.min_val)
        fill_w = int(ratio * self.rect.width)
        pygame.draw.rect(surf, ACCENT, (self.rect.x, self.rect.y, fill_w, self.rect.height), border_radius=4)
        pygame.draw.circle(surf, (255, 255, 255), (self.rect.x + fill_w, self.rect.centery), 7)
        txt = font.render(f"{self.label}: {self.val:.0f} {self.unit}", True, TEXT_COLOR)
        surf.blit(txt, (self.rect.x, self.rect.y - 20))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.dragging = True; return True
        elif event.type == pygame.MOUSEBUTTONUP: self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            rel = max(0, min(event.pos[0] - self.rect.x, self.rect.width))
            self.val = self.min_val + (rel / self.rect.width) * (self.max_val - self.min_val)
            return True
        return False

def dibujar_carro(surf, x_px, y_px):
    # Carrocería
    pygame.draw.rect(surf, CAR_COLOR, (x_px - 20, y_px - 15, 50, 20), border_radius=5)
    # Cabina
    pygame.draw.rect(surf, (200, 200, 200), (x_px - 5, y_px - 25, 25, 12), border_radius=3)
    # Llantas
    pygame.draw.circle(surf, (10, 10, 10), (x_px - 10, y_px + 5), 7)
    pygame.draw.circle(surf, (10, 10, 10), (x_px + 20, y_px + 5), 7)
    pygame.draw.circle(surf, (150, 150, 150), (x_px - 10, y_px + 5), 3) # Rines
    pygame.draw.circle(surf, (150, 150, 150), (x_px + 20, y_px + 5), 3)

def renderizar():
    pygame.init()
    sw, sh = 1150, 450
    pantalla = pygame.display.set_mode((sw, sh))
    pygame.display.set_caption("Caso de Estudio: MRU (Carretera)")
    
    f_ui = pygame.font.SysFont("Consolas", 14)
    f_bold = pygame.font.SysFont("Consolas", 15, bold=True)
    f_title = pygame.font.SysFont("Consolas", 20, bold=True)
    
    coche = CarroMRU()
    # Slider de Velocidad y Distancia
    slider_v = Slider(30, 100, 240, 10, 10.0, 180.0, 60.0, "Velocímetro", "km/h")
    slider_d = Slider(30, 170, 240, 10, 100.0, 500.0, 500.0, "Distancia a Meta", "m")

    reloj = pygame.time.Clock()

    while True:
        dt = reloj.tick(60) / 1000.0 # Tiempo delta en segundos reales
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return
            
            movido = slider_v.handle_event(e) or slider_d.handle_event(e)
            if movido: coche.reiniciar()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE: coche.arrancar()
                if e.key == pygame.K_r: coche.reiniciar()

        # Actualizar variables
        if not coche.en_movimiento:
            coche.vel_kmh = slider_v.val
            coche.meta_m = slider_d.val

        coche.actualizar(dt)

        # --- DIBUJO ---
        pantalla.fill(BG_COLOR)
        
        # Carretera
        y_carril = 250
        pygame.draw.rect(pantalla, ROAD_COLOR, (ORIGEN_X, y_carril - 40, sw - ORIGEN_X, 80))
        # Líneas punteadas
        for x_line in range(ORIGEN_X, sw, 40):
            pygame.draw.rect(pantalla, (200, 200, 50), (x_line, y_carril - 2, 20, 4))

        # Marcas de distancia (Metros reales a Píxeles)
        for m in range(0, int(coche.meta_m) + 50, 50):
            x_px = ORIGEN_X + (m * PPM)
            if x_px < sw:
                pygame.draw.line(pantalla, (100, 100, 110), (x_px, y_carril + 40), (x_px, y_carril + 50), 2)
                pantalla.blit(f_ui.render(f"{m}m", True, (150, 150, 150)), (x_px - 10, y_carril + 55))

        # Dibujar Meta
        meta_px = ORIGEN_X + (coche.meta_m * PPM)
        pygame.draw.rect(pantalla, (255, 255, 255), (meta_px, y_carril - 40, 10, 80))
        for i in range(4): # Patrón a cuadros
            pygame.draw.rect(pantalla, (0, 0, 0), (meta_px, y_carril - 40 + (i*20), 5, 10))
            pygame.draw.rect(pantalla, (0, 0, 0), (meta_px + 5, y_carril - 30 + (i*20), 5, 10))

        # Dibujar Carro
        carro_px = ORIGEN_X + (coche.x_m * PPM)
        dibujar_carro(pantalla, carro_px, y_carril)

        # --- PANEL UI ---
        pygame.draw.rect(pantalla, PANEL_COLOR, (0, 0, 310, sh))
        pygame.draw.rect(pantalla, (20, 20, 22), (0, 0, 310, sh), 2)
        
        pantalla.blit(f_title.render("MOVIMIENTO RECT. UNIF.", True, ACCENT), (20, 20))
        
        slider_v.draw(pantalla, f_ui)
        slider_d.draw(pantalla, f_ui)

        pygame.draw.line(pantalla, (80,80,80), (20, 220), (290, 220))
        pantalla.blit(f_bold.render("CONTROLES:", True, CAR_COLOR), (20, 240))
        pantalla.blit(f_ui.render("[ESPACIO] Arrancar Coche", True, TEXT_COLOR), (20, 265))
        pantalla.blit(f_ui.render("[R] Reiniciar Posición", True, TEXT_COLOR), (20, 290))

        # --- EXPLICADOR DINÁMICO ---
        box_rect = pygame.Rect(330, 20, 780, 110)
        pygame.draw.rect(pantalla, (15, 18, 22), box_rect, border_radius=5)
        pygame.draw.rect(pantalla, ACCENT, box_rect, 2, border_radius=5)

        # Cálculos en tiempo real
        t_total_teorico = coche.meta_m / (coche.vel_kmh / 3.6) if coche.vel_kmh > 0 else 0
        
        col_fase = GREEN_OK if coche.en_movimiento else TEXT_COLOR
        if coche.fase == "DESTINO ALCANZADO": col_fase = ACCENT

        info = [
            f"ESTADO: {coche.fase}",
            f"Reloj: {coche.tiempo:.2f} s  |  Posición (X): {coche.x_m:.1f} m",
            f"Velocidad Constante (v): {coche.vel_kmh:.1f} km/h  ->  {(coche.vel_kmh / 3.6):.2f} m/s",
            f"Aceleración (a): 0 m/s² (Sin frenos ni acelerador)"
        ]

        for i, txt in enumerate(info):
            color = col_fase if i == 0 else TEXT_COLOR
            pantalla.blit(f_bold.render(txt, True, color), (350, 35 + i*20))

        # Teoría a la derecha del recuadro
        pantalla.blit(f_bold.render("ECUACIÓN PRINCIPAL:", True, CAR_COLOR), (800, 35))
        pantalla.blit(f_ui.render("x(t) = x0 + v * t", True, TEXT_COLOR), (800, 55))
        pantalla.blit(f_ui.render(f"Tiempo estimado: {t_total_teorico:.1f} s", True, GREEN_OK), (800, 75))

        pygame.display.flip()

    pygame.quit()