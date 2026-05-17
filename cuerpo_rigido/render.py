import pygame
import math
from simulacion import MotorRigido

# Paleta Dark Mode / Dashboard
BG_COLOR = (20, 22, 26)
PANEL_COLOR = (30, 33, 38)
TEXT_COLOR = (230, 230, 240)
ACCENT_BLUE = (0, 180, 255)
GREEN_ON = (46, 204, 113)
RED_OFF = (231, 76, 60)
ORANGE_WARN = (243, 156, 18)

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, start_val, label, unit):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val, self.max_val = min_val, max_val
        self.val = start_val
        self.label, self.unit = label, unit
        self.dragging = False

    def draw(self, surf, font):
        pygame.draw.rect(surf, (50, 50, 55), self.rect, border_radius=4)
        ratio = (self.val - self.min_val) / (self.max_val - self.min_val)
        fill_w = int(ratio * self.rect.width)
        pygame.draw.rect(surf, ACCENT_BLUE, (self.rect.x, self.rect.y, fill_w, self.rect.height), border_radius=4)
        pygame.draw.circle(surf, (255, 255, 255), (self.rect.x + fill_w, self.rect.centery), 7)
        txt = font.render(f"{self.label}: {self.val:.1f} {self.unit}", True, TEXT_COLOR)
        surf.blit(txt, (self.rect.x, self.rect.y - 20))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP: self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            rel = max(0, min(event.pos[0] - self.rect.x, self.rect.width))
            self.val = self.min_val + (rel / self.rect.width) * (self.max_val - self.min_val)

def dibujar_skin(surf, x, y, angulo, tipo):
    radio = 80
    if tipo == 0: # Engrane Industrial
        pygame.draw.circle(surf, (100, 105, 110), (x, y), radio - 10)
        pygame.draw.circle(surf, BG_COLOR, (x, y), 20) # Eje central
        for i in range(12):
            a = angulo + (i * math.pi / 6)
            pts = [
                (x + (radio-10)*math.cos(a-0.1), y + (radio-10)*math.sin(a-0.1)),
                (x + radio*math.cos(a-0.05), y + radio*math.sin(a-0.05)),
                (x + radio*math.cos(a+0.05), y + radio*math.sin(a+0.05)),
                (x + (radio-10)*math.cos(a+0.1), y + (radio-10)*math.sin(a+0.1))
            ]
            pygame.draw.polygon(surf, (120, 125, 130), pts)
            pygame.draw.line(surf, (70, 75, 80), (x, y), (x + (radio-10)*math.cos(a), y + (radio-10)*math.sin(a)), 2)
            
    elif tipo == 1: # Ventilador
        pygame.draw.circle(surf, (40, 40, 40), (x, y), 15)
        for i in range(4):
            a = angulo + (i * math.pi / 2)
            aspa = pygame.Surface((radio*2, radio*2), pygame.SRCALPHA)
            pygame.draw.ellipse(aspa, (200, 200, 210, 180), (radio, radio-15, radio-10, 30))
            aspa_rotada = pygame.transform.rotate(aspa, -math.degrees(a))
            rect = aspa_rotada.get_rect(center=(x, y))
            surf.blit(aspa_rotada, rect)
            
    elif tipo == 2: # Llanta / Rueda
        pygame.draw.circle(surf, (30, 30, 35), (x, y), radio, 15) # Neumático
        pygame.draw.circle(surf, (180, 180, 190), (x, y), radio - 15, 5) # Rin exterior
        for i in range(5): # Rayos
            a = angulo + (i * 2 * math.pi / 5)
            pygame.draw.line(surf, (180, 180, 190), (x, y), (x + (radio-15)*math.cos(a), y + (radio-15)*math.sin(a)), 8)
        pygame.draw.circle(surf, BG_COLOR, (x, y), 10)

def renderizar():
    pygame.init()
    sw, sh = 1150, 650
    pantalla = pygame.display.set_mode((sw, sh))
    pygame.display.set_caption("Simulador: Dinámica de Cuerpo Rígido")
    
    f_ui = pygame.font.SysFont("Consolas", 14)
    f_bold = pygame.font.SysFont("Consolas", 15, bold=True)
    f_title = pygame.font.SysFont("Consolas", 20, bold=True)
    
    motor = MotorRigido()
    sliders = [
        Slider(30, 80, 240, 10, 10.0, 200.0, 50.0, "Torque Motor (τ)", "N·m"),
        Slider(30, 150, 240, 10, 1.0, 50.0, 10.0, "Momento Inercia (I)", "kg·m²"),
        Slider(30, 220, 240, 10, 0.1, 10.0, 2.0, "Fricción Eje", "")
    ]
    
    skin_idx = 0
    nombres_skins = ["Engrane Transmisión", "Ventilador Industrial", "Llanta de Vehículo"]
    reloj = pygame.time.Clock()

    while True:
        dt = reloj.tick(60) / 1000.0
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return
            for s in sliders: s.handle_event(e)

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE: motor.toggle_motor()
                if e.key == pygame.K_s: skin_idx = (skin_idx + 1) % 3

        # Actualizar física
        motor.torque_motor = sliders[0].val
        motor.inercia = sliders[1].val
        motor.friccion = sliders[2].val
        motor.actualizar(dt)

        # Cálculos derivados para mostrar
        rpm = (motor.vel_angular * 60) / (2 * math.pi)
        vueltas = motor.angulo_rad / (2 * math.pi)

        # --- DIBUJO ---
        pantalla.fill(BG_COLOR)
        
        # Grid decorativo del laboratorio
        for x in range(300, sw, 50): pygame.draw.line(pantalla, (30, 32, 35), (x, 0), (x, sh))
        for y in range(0, sh, 50): pygame.draw.line(pantalla, (30, 32, 35), (300, y), (sw, y))

        # Dibujar Objeto Central
        centro_x, centro_y = 720, 250
        
        # Base/Soporte del motor
        pygame.draw.rect(pantalla, (40, 45, 50), (centro_x - 40, centro_y, 80, 150))
        pygame.draw.line(pantalla, (80, 85, 90), (centro_x - 60, centro_y + 150), (centro_x + 60, centro_y + 150), 6)
        
        dibujar_skin(pantalla, centro_x, centro_y, motor.angulo_rad, skin_idx)
        pantalla.blit(f_bold.render(nombres_skins[skin_idx], True, TEXT_COLOR), (centro_x - 80, centro_y - 120))

        # Vector de Velocidad Angular (Indicador visual)
        if motor.vel_angular > 0:
            radio_vector = 100
            pygame.draw.arc(pantalla, ACCENT_BLUE, (centro_x - radio_vector, centro_y - radio_vector, radio_vector*2, radio_vector*2), math.pi/4, math.pi/4 + min(motor.vel_angular/10, math.pi), 4)

        # --- PANEL UI IZQUIERDO ---
        pygame.draw.rect(pantalla, PANEL_COLOR, (0, 0, 300, sh))
        pygame.draw.rect(pantalla, (25, 28, 32), (0, 0, 300, sh), 3)
        pantalla.blit(f_title.render("CONTROL DE MOTOR", True, ACCENT_BLUE), (20, 20))
        
        for s in sliders: s.draw(pantalla, f_ui)
        
        # Botón Encendido/Apagado
        color_btn = GREEN_ON if motor.motor_encendido else RED_OFF
        txt_btn = "MOTOR ENCENDIDO" if motor.motor_encendido else "MOTOR APAGADO"
        pygame.draw.rect(pantalla, color_btn, (30, 290, 240, 40), border_radius=5)
        pantalla.blit(f_title.render(txt_btn, True, (20, 20, 20)), (45, 300))

        pygame.draw.line(pantalla, (70,70,70), (20, 360), (280, 360))
        pantalla.blit(f_bold.render("INSTRUCCIONES:", True, ORANGE_WARN), (30, 380))
        pantalla.blit(f_ui.render("[ESPACIO] Encender/Apagar", True, TEXT_COLOR), (30, 410))
        pantalla.blit(f_ui.render("[S] Cambiar Rotor", True, TEXT_COLOR), (30, 440))

        # --- PANEL DE FÍSICA INFERIOR ---
        box_rect = pygame.Rect(330, 430, sw - 360, 190)
        pygame.draw.rect(pantalla, PANEL_COLOR, box_rect, border_radius=8)
        pygame.draw.rect(pantalla, ACCENT_BLUE, box_rect, 2, border_radius=8)

        # Datos Telemétricos en vivo
        c_fase = GREEN_ON if "CONSTANTE" in motor.fase else (ORANGE_WARN if "ACELERANDO" in motor.fase else RED_OFF)
        pantalla.blit(f_title.render(f"ESTADO: {motor.fase}", True, c_fase), (350, 450))
        
        datos = [
            f"Velocidad Angular (ω): {motor.vel_angular:.2f} rad/s",
            f"Revoluciones x Minuto: {rpm:.0f} RPM",
            f"Aceleración Ang. (α) : {motor.acel_angular:.2f} rad/s²",
            f"Vueltas Totales (θ)  : {vueltas:.1f} revs"
        ]
        for i, d in enumerate(datos):
            pantalla.blit(f_ui.render(d, True, TEXT_COLOR), (350, 490 + i*22))

        # Explicación (Lado derecho del panel)
        pygame.draw.line(pantalla, (80,85,90), (700, 450), (700, 600))
        pantalla.blit(f_bold.render("ANÁLISIS DINÁMICO:", True, ACCENT_BLUE), (720, 450))
        
        teoria = []
        if motor.motor_encendido:
            if motor.acel_angular > 0.5:
                teoria = [
                    "El Torque del motor supera la fricción.",
                    "El objeto vence su Inercia (I) y se acelera.",
                    "Fórmula: α = (Torque - Fricción) / Inercia",
                    "RPM en aumento constante."
                ]
            else:
                teoria = [
                    "Equilibrio de Fuerzas alcanzado.",
                    "La fuerza del motor es igual a la fuerza",
                    "de fricción (Torque Neto = 0).",
                    "El motor gira a su Velocidad Terminal (RPM Máx)."
                ]
        else:
            if motor.vel_angular > 0:
                teoria = [
                    "Motor apagado. Torque aplicado = 0.",
                    "El objeto sigue girando gracias a su Inercia (I),",
                    "pero la fricción aplica una aceleración negativa (-α)",
                    "hasta detener el sistema por completo."
                ]
            else:
                teoria = [
                    "Sistema en reposo.",
                    "La Inercia (I) mantiene el objeto estático",
                    "hasta que se aplique un nuevo Torque externo."
                ]
                
        for i, linea in enumerate(teoria):
            pantalla.blit(f_ui.render(linea, True, (180, 190, 200)), (720, 490 + i*22))

        pygame.display.flip()

    pygame.quit()