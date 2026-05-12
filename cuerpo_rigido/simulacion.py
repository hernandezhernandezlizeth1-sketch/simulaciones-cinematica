import math

class OsciladorAngular:
    def __init__(self):
        self.frecuencia = 1.0  # f: vueltas por segundo
        self.tiempo = 0.0
        self.historial_y = []  # Para dibujar la onda
        self.max_puntos = 300  # Resolución de la estela

    def actualizar(self, dt):
        self.tiempo += dt
        
        # Velocidad angular: ω = 2πf
        omega = 2 * math.pi * self.frecuencia
        
        # Ángulo actual: θ = ωt
        angulo = omega * self.tiempo
        
        # Proyección en Y (normalizada de -1 a 1)
        y_norm = math.sin(angulo)
        
        # Guardamos el punto al inicio de la lista
        self.historial_y.insert(0, y_norm)
        if len(self.historial_y) > self.max_puntos:
            self.historial_y.pop()
            
        return angulo, y_norm