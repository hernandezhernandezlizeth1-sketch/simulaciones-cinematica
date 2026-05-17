import math
import random

class Proyectil:
    def __init__(self, x0_m):
        self.x0_m = x0_m  
        self.vel_inicial = 25.0    # m/s
        self.angulo_grados = 45.0  # Grados
        self.altura_inicial = 10.0 # Metros de altura inicial
        self.gravedad = 9.81       # m/s^2 (Tierra)
        
        # Factor de cámara lenta: 0.20 significa que 1 segundo real tarda 5 segundos en la pantalla
        self.factor_tiempo = 0.20 
        
        self.reiniciar()
        self.generar_objetivo()

    def generar_objetivo(self):
        self.objetivo_x_m = random.uniform(40.0, 95.0)
        self.hit = False

    def disparar(self):
        self.reiniciar()
        self.en_movimiento = True

    def reiniciar(self):
        self.x_m = self.x0_m
        self.y_m = self.altura_inicial
        self.tiempo_simulado = 0.0
        self.en_movimiento = False
        self.hit = False
        self.fase = "PREPARACIÓN"

    def actualizar(self, dt):
        if not self.en_movimiento:
            return

        # Aplicamos la cámara lenta al delta de tiempo
        dt_lento = dt * self.factor_tiempo
        self.tiempo_simulado += dt_lento

        angulo_rad = math.radians(self.angulo_grados)
        vx = self.vel_inicial * math.cos(angulo_rad)
        vy_inicial = self.vel_inicial * math.sin(angulo_rad)
        
        # ECUACIONES CINEMÁTICAS REALES (Con altura inicial y0)
        self.x_m = self.x0_m + vx * self.tiempo_simulado
        self.y_m = self.altura_inicial + (vy_inicial * self.tiempo_simulado) - (0.5 * self.gravedad * (self.tiempo_simulado ** 2))
        
        vy_actual = vy_inicial - self.gravedad * self.tiempo_simulado

        # Hitbox del objetivo (Suelo)
        if abs(self.x_m - self.objetivo_x_m) <= 2.5 and self.y_m <= 0:
            self.hit = True
            self.en_movimiento = False
            self.y_m = 0
            self.fase = "¡IMPACTO EN META!"
            return

        # Condición de parada en el suelo
        if self.y_m <= 0:
            self.y_m = 0
            self.en_movimiento = False
            self.fase = "IMPACTO FUERA DE META"
        elif abs(vy_actual) < 0.4:
            self.fase = "ÁPICE (ALTURA MÁXIMA)"
        elif vy_actual > 0:
            self.fase = "SUBIDA CONTINUA"
        else:
            self.fase = "DESCENSO ACELERADO"

    def obtener_trayectoria_proyectada(self):
        puntos = []
        angulo_rad = math.radians(self.angulo_grados)
        vx = self.vel_inicial * math.cos(angulo_rad)
        vy = self.vel_inicial * math.sin(angulo_rad)
        
        t = 0.0
        dt_sim = 0.05
        x_sim = self.x0_m
        y_sim = self.altura_inicial
        
        while y_sim >= 0 and x_sim < 120.0:
            puntos.append((x_sim, y_sim))
            t += dt_sim
            x_sim = self.x0_m + vx * t
            y_sim = self.altura_inicial + vy * t - 0.5 * self.gravedad * (t ** 2)
            
        puntos.append((x_sim, 0.0))
        return puntos