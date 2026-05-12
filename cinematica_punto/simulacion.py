import math

class Proyectil:
    def __init__(self, x0, y0):
        self.x0 = x0
        self.y0 = y0
        # Parámetros controlados por la UI
        self.vel_inicial = 90.0
        self.angulo_grados = 45.0
        self.gravedad = 98.0
        
        self.x = x0
        self.y = y0
        self.tiempo = 0
        self.en_movimiento = False

    def disparar(self):
        self.tiempo = 0
        self.x = self.x0
        self.y = self.y0
        self.en_movimiento = True

    def detener(self):
        self.en_movimiento = False
        self.tiempo = 0
        self.x = self.x0
        self.y = self.y0

    def actualizar(self, dt):
        if not self.en_movimiento:
            return

        self.tiempo += dt
        angulo_rad = math.radians(self.angulo_grados)
        vx = self.vel_inicial * math.cos(angulo_rad)
        vy = -self.vel_inicial * math.sin(angulo_rad) 
        
        self.x = self.x0 + vx * self.tiempo
        self.y = self.y0 + vy * self.tiempo + 0.5 * self.gravedad * (self.tiempo ** 2)

        # Detener si toca el suelo
        if self.y >= self.y0 and self.tiempo > 0.1:
            self.y = self.y0
            self.en_movimiento = False

    def obtener_trayectoria_proyectada(self):
        # Calcula los puntos teóricos de la parábola para dibujarlos
        puntos = []
        angulo_rad = math.radians(self.angulo_grados)
        vx = self.vel_inicial * math.cos(angulo_rad)
        vy = -self.vel_inicial * math.sin(angulo_rad)
        
        t = 0
        dt_sim = 0.05
        y_sim = self.y0
        x_sim = self.x0
        
        while y_sim <= self.y0 and x_sim < 2000:
            puntos.append((x_sim, y_sim))
            t += dt_sim
            x_sim = self.x0 + vx * t
            y_sim = self.y0 + vy * t + 0.5 * self.gravedad * (t ** 2)
            
        puntos.append((x_sim, self.y0)) # Último punto en el suelo
        return puntos