import math

class MotorRigido:
    def __init__(self):
        self.angulo_rad = 0.0
        self.vel_angular = 0.0      # ω (rad/s)
        self.acel_angular = 0.0     # α (rad/s²)
        
        # Parámetros del motor (Controlables)
        self.torque_motor = 50.0    # Fuerza de giro (N·m)
        self.inercia = 10.0         # Resistencia a girar (Masa/Tamaño) (kg·m²)
        self.friccion = 2.0         # Rozamiento de los baleros
        
        self.motor_encendido = False
        self.fase = "SISTEMA DETENIDO"

    def toggle_motor(self):
        self.motor_encendido = not self.motor_encendido

    def actualizar(self, dt):
        # 1. Calcular el torque neto (Fuerza del motor menos la fricción)
        torque_neto = 0.0
        if self.motor_encendido:
            torque_neto += self.torque_motor
        
        # La fricción frena proporcionalmente a qué tan rápido gira
        torque_neto -= self.friccion * self.vel_angular
        
        # 2. Segunda Ley de Newton para rotación: α = τ / I
        self.acel_angular = torque_neto / self.inercia
        
        # 3. Integración cinemática
        self.vel_angular += self.acel_angular * dt
        
        # Detener completamente si está apagado y ya gira muy lento
        if not self.motor_encendido and self.vel_angular < 0.05:
            self.vel_angular = 0.0
            self.acel_angular = 0.0
            self.fase = "SISTEMA DETENIDO"
        else:
            self.angulo_rad += self.vel_angular * dt
            
            # Detectar la fase para la UI
            if self.motor_encendido:
                if self.acel_angular > 0.5:
                    self.fase = "ACELERANDO (ARRANQUE)"
                else:
                    self.fase = "VELOCIDAD CONSTANTE (EQUILIBRIO)"
            else:
                self.fase = "FRENANDO POR FRICCIÓN"