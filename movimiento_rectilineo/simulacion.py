class CarroMRU:
    def __init__(self):
        self.x0_m = 0.0       # Posición inicial (metros)
        self.x_m = 0.0        # Posición actual (metros)
        self.vel_kmh = 60.0   # Velocidad en km/h (Controlable)
        self.vel_ms = 0.0     # Velocidad en m/s
        
        self.meta_m = 500.0   # Destino a 500 metros
        self.tiempo = 0.0
        self.en_movimiento = False
        self.fase = "DETENIDO"

    def arrancar(self):
        self.x_m = self.x0_m
        self.tiempo = 0.0
        # Conversión: 1 km/h = 1000m / 3600s = 1/3.6 m/s
        self.vel_ms = self.vel_kmh / 3.6 
        self.en_movimiento = True
        self.fase = "EN RUTA (VELOCIDAD CONSTANTE)"

    def reiniciar(self):
        self.en_movimiento = False
        self.tiempo = 0.0
        self.x_m = self.x0_m
        self.fase = "DETENIDO"

    def actualizar(self, dt):
        if not self.en_movimiento:
            return

        self.tiempo += dt
        
        # Fórmula maestra del MRU
        self.x_m = self.x0_m + (self.vel_ms * self.tiempo)

        # Checar si ya llegó a la meta
        if self.x_m >= self.meta_m:
            self.x_m = self.meta_m
            self.en_movimiento = False
            self.fase = "DESTINO ALCANZADO"