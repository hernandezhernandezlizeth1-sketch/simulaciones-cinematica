import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches

# --- PARÁMETROS FÍSICOS (ESCALA REAL TIERRA) ---
v0 = 25.0          # Velocidad inicial (m/s)
angulo_deg = 45.0  # Ángulo de disparo (grados)
y0 = 10.0          # Altura inicial (m)
g = 9.81           # Gravedad terrestre (m/s^2)

angulo_rad = np.radians(angulo_deg)
v0x = v0 * np.cos(angulo_rad)
v0y = v0 * np.sin(angulo_rad)

# Calcular el tiempo total hasta tocar el suelo (Ecuación cuadrática)
# y(t) = y0 + v0y*t - 0.5*g*t^2 = 0
t_total = (v0y + np.sqrt(v0y**2 + 2 * g * y0)) / g
t = np.linspace(0, t_total, num=160) # 160 frames para que se vea la "cámara lenta"

# Ecuaciones de movimiento
x = v0x * t
y = y0 + v0y * t - 0.5 * g * t**2

# Coordenadas clave
x_max = v0x * t_total
h_max = y0 + (v0y**2) / (2 * g)

# --- CONFIGURACIÓN VISUAL DEL LABORATORIO ---
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(11, 6.5), dpi=100)
ax.set_xlim(-5, x_max + 15)
ax.set_ylim(0, h_max + 10)
ax.set_title('Laboratorio Cinemático: Análisis Segundo a Segundo', color='#00aaff', fontsize=15, fontweight='bold')
ax.set_xlabel('Distancia Horizontal (metros)')
ax.set_ylabel('Altura Vertical (metros)')
ax.grid(color='#333333', linestyle='--', linewidth=1)

# Dibujar la plataforma de altura inicial
plataforma = patches.Rectangle((-2, 0), 4, y0, facecolor='#444455', edgecolor='#888899', lw=2)
ax.add_patch(plataforma)

# Dibujar la Meta (calculada para que sea un Hit perfecto)
meta_ancho = 6
meta = patches.Rectangle((x_max - meta_ancho/2, 0), meta_ancho, 2, facecolor='#39ff14', edgecolor='#ffffff', lw=2)
ax.add_patch(meta)
ax.text(x_max, 3, f'META: {x_max:.1f}m', color='#39ff14', fontsize=10, ha='center', fontweight='bold')

# Elementos dinámicos
linea_trayectoria, = ax.plot([], [], color='#555566', linestyle='--', lw=2)
estela, = ax.plot([], [], color='#00d2ff', lw=3)
punto, = ax.plot([], [], 'o', color='#39ff14', markersize=10)

# Cuadro de explicación analítica
cuadro_texto = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=10,
                       verticalalignment='top', color='white', family='monospace',
                       bbox=dict(boxstyle='round', facecolor='#111115', alpha=0.9, edgecolor='#00aaff'))

def animar(i):
    # Actualizar dibujo
    linea_trayectoria.set_data(x, y) 
    estela.set_data(x[:i], y[:i])    
    punto.set_data([x[i]], [y[i]])     
    
    tiempo_actual = t[i]
    vy_actual = v0y - (g * tiempo_actual)
    segundo_entero = int(np.floor(tiempo_actual))
    
    # TEXTOS ANALÍTICOS DINÁMICOS
    explicacion = f"REPORTE CINEMÁTICO | Reloj: {tiempo_actual:.2f} s\n"
    explicacion += "-"*45 + "\n"
    explicacion += f"Posición : X = {x[i]:.2f} m  |  Y = {y[i]:.2f} m\n"
    explicacion += f"Velocidad: Vx = {v0x:.2f} m/s| Vy = {vy_actual:.2f} m/s\n"
    explicacion += "-"*45 + "\n"

    # Análisis segundo a segundo
    if i == len(t) - 1 or tiempo_actual >= t_total - 0.05:
        explicacion += "ESTADO: ¡IMPACTO EN LA META!\n"
        explicacion += "El objeto aterrizó exactamente en las coordenadas calculadas.\n"
        explicacion += f"Tiempo total: {t_total:.2f} s | Alcance (X): {x_max:.2f} m"
        punto.set_color('#ffaa00')
        punto.set_markersize(16)
    elif segundo_entero == 0:
        explicacion += "SITUACIÓN [0s a 1s]: IMPULSO INICIAL\n"
        explicacion += f"Sale desde y0={y0}m. El empuje vertical inicial es fuerte.\n"
        explicacion += "Ecuación X (MRU): x = v0·cos(θ)·t\n"
        explicacion += "Ecuación Y (MRUV): y = y0 + v0·sin(θ)·t - ½gt²"
    elif segundo_entero == 1:
        explicacion += "SITUACIÓN [1s a 2s]: PÉRDIDA DE VELOCIDAD VERTICAL\n"
        explicacion += "La gravedad drena energía cinética vertical.\n"
        explicacion += f"Cada segundo, Vy disminuye exactamente {g} m/s.\n"
        explicacion += "Vx permanece inmutable por inercia."
    elif segundo_entero == 2:
        explicacion += "SITUACIÓN [2s a 3s]: TRANSICIÓN AL ÁPICE\n"
        explicacion += "El proyectil alcanza su altura máxima.\n"
        explicacion += f"H_max calculada: {h_max:.2f} m. En este punto Vy ≈ 0.\n"
        explicacion += "La energía potencial llega a su límite."
        punto.set_color('#ffaa00')
    else:
        explicacion += f"SITUACIÓN [> 3s]: DESCENSO ACELERADO\n"
        explicacion += "El vector Vy se ha invertido (ahora es negativo).\n"
        explicacion += "La gravedad actúa a favor del movimiento hacia abajo.\n"
        explicacion += "Aproximación final al objetivo en el suelo."
        punto.set_color('#39ff14')

    cuadro_texto.set_text(explicacion)
    return linea_trayectoria, estela, punto, cuadro_texto

animacion = FuncAnimation(fig, animar, frames=len(t), interval=40, blit=True)

print("Procesando los cálculos y renderizando el GIF.")
animacion.save('cinematica_laboratorio_lento.gif', fps=25, writer='pillow')
print("¡Listo ahí tienes 'cinematica_laboratorio_lento.gif'.")