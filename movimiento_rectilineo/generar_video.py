import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches

# --- PARÁMETROS FÍSICOS REALES (MRU) ---
vel_kmh = 90.0        # Velocidad constante del coche (km/h)
meta_m = 200.0        # Distancia total de la prueba (metros)

# Conversión de unidades real a m/s (90 / 3.6 = 25 m/s)
vel_ms = vel_kmh / 3.6

# Ecuación del tiempo teórico de viaje (t = x / v)
t_total = meta_m / vel_ms
t = np.linspace(0, t_total, num=120) # 120 cuadros para cámara lenta analítica

# Ecuación de movimiento lineal constante
x = vel_ms * t
y = np.zeros_like(t) # El coche va en línea recta sobre el suelo (Y = 0)

# --- CONFIGURACIÓN VISUAL DEL LABORATORIO ---
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(11, 5), dpi=100)
ax.set_xlim(-10, meta_m + 20)
ax.set_ylim(-5, 15)
ax.set_title('Laboratorio MRU: Análisis Lineal a Velocidad Constante', color='#00ffaa', fontsize=14, fontweight='bold')
ax.set_xlabel('Posición en el Espacio (metros)')
ax.get_yaxis().set_visible(False) # Ocultamos el eje Y porque es movimiento unidimensional
ax.grid(color='#222222', linestyle='--', linewidth=1)

# Dibujar la carretera (Piso de referencia)
plt.axhline(0, color='#555555', lw=3, zorder=1)

# Dibujar la línea de Meta
ax.axvline(meta_m, color='#ff3333', linestyle='--', lw=2)
ax.text(meta_m, 8, 'META', color='#ff3333', fontsize=10, ha='center', fontweight='bold')

# Elementos dinámicos del vehículo
estela, = ax.plot([], [], color='#00ffaa', lw=2, zorder=2)
coche = patches.Rectangle((0, 0), 6, 3, facecolor='#00ffaa', edgecolor='#ffffff', zorder=3)
ax.add_patch(coche)

# Cuadro de bitácora telemétrica
cuadro_texto = ax.text(0.02, 0.90, '', transform=ax.transAxes, fontsize=10,
                       verticalalignment='top', color='white', family='monospace',
                       bbox=dict(boxstyle='round', facecolor='#111115', alpha=0.9, edgecolor='#00ffaa'))

def animar(i):
    # Actualizar la posición del cuadro que representa el coche
    pos_x = x[i]
    coche.set_xy((pos_x - 3, 0)) # Centrar el coche en su coordenada X
    estela.set_data(x[:i], y[:i] + 1.5) # Línea de rastro a la mitad del chasis
    
    tiempo_actual = t[i]
    segundo_entero = int(np.floor(tiempo_actual))
    
    # TELEMETRÍA DINÁMICA
    explicacion = f"REPORTE MRU | Reloj de Ruta: {tiempo_actual:.2f} s\n"
    explicacion += "-"*50 + "\n"
    explicacion += f"Posición Actual    : X = {pos_x:.2f} m\n"
    explicacion += f"Velocidad de Crucero: v = {vel_kmh:.1f} km/h ({vel_ms:.2f} m/s)\n"
    explicacion += f"Aceleración Lineal : a = 0.00 m/s² [NULA]\n"
    explicacion += "-"*50 + "\n"

    # Análisis analítico de tramos temporales
    if i == len(t) - 1 or pos_x >= meta_m:
        explicacion += "ESTADO: ¡DESTINO FINAL LOGRADO!\n"
        explicacion += f"Tiempo de tránsito exacto: {t_total:.2f} segundos.\n"
        explicacion += "Demostración: En MRU la velocidad jamás varía."
        coche.set_facecolor('#ffaa00')
    elif segundo_entero == 0:
        explicacion += "ANÁLISIS [0s a 1s]: ARRANQUE DEL SISTEMA\n"
        explicacion += "El coche ya posee velocidad inicial uniforme.\n"
        explicacion += "Fórmula de posición: x(t) = x0 + v · t\n"
        explicacion += f"Progresión: Recorre exactamente {vel_ms:.1f} metros cada segundo."
    elif segundo_entero == 2:
        explicacion += "ANÁLISIS [2s a 3s]: COMPORTAMIENTO SIMÉTRICO\n"
        explicacion += "Principio fundamental del movimiento rectilíneo:\n"
        explicacion += "En intervalos de tiempo idénticos, el sistema\n"
        explicacion += "desplaza distancias exactamente iguales."
    else:
        explicacion += "ANÁLISIS: CONTINUIDAD CINEMÁTICA\n"
        explicacion += "No existen fuerzas externas netas (ΣF = 0).\n"
        explicacion += "Por la Primera Ley de Newton, el objeto mantiene\n"
        explicacion += "su estado de movimiento rectilíneo perpetuamente."

    cuadro_texto.set_text(explicacion)
    return estela, coche, cuadro_texto

animacion = FuncAnimation(fig, animar, frames=len(t), interval=40, blit=False)

print("Procesando ecuaciones MRU...")
animacion.save('mru_laboratorio_lento.gif', fps=25, writer='pillow')
print("¡Listo! Archivo 'mru_laboratorio_lento.gif' exportado exitosamente.")