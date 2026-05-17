import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches

# --- PARÁMETROS FÍSICOS REALES (DINÁMICA ROTACIONAL) ---
w0 = 15.0             # Velocidad angular inicial (rad/s) (~143 RPM)
inercia = 8.0         # Momento de inercia del disco (kg·m²)
friccion_eje = 1.5    # Coeficiente de rozamiento dinámico (N·m·s)

# Ecuaciones diferenciales resueltas para frenado por fricción:
# Torque_friccion = -b * w
# dw/dt = -b*w / I  -->  w(t) = w0 * exp(-(b/I)*t)
alpha_inicial = -(friccion_eje * w0) / inercia  # Aceleración angular inicial

# Tiempo estimado para que baje a velocidad casi nula
t_total = 7.0
t = np.linspace(0, t_total, num=150)

# Calcular vectores de velocidad y aceleración angular a lo largo del tiempo
w = w0 * np.exp(-(friccion_eje / inercia) * t)
alpha = -(friccion_eje * w) / inercia

# Integrar el ángulo (θ) para saber cuánto ha girado
theta = (w0 * inercia / friccion_eje) * (1 - np.exp(-(friccion_eje / inercia) * t))

# --- CONFIGURACIÓN VISUAL DEL LABORATORIO ---
plt.style.use('dark_background')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5), dpi=100)
fig.suptitle('Laboratorio del Cuerpo Rígido: Inercia y Fricción Dinámica', color='#00aaff', fontsize=14, fontweight='bold')

# Panel izquierdo: Disco en rotación
ax1.set_xlim(-1.5, 1.5)
ax1.set_ylim(-1.5, 1.5)
ax1.set_aspect('equal')
ax1.axis('off')

# Panel derecho: Gráfico de desaceleración (ω vs t)
ax2.set_xlim(0, t_total)
ax2.set_ylim(0, w0 + 2)
ax2.set_xlabel('Tiempo de Frenado (segundos)')
ax2.set_ylabel('Velocidad Angular ω (rad/s)')
ax2.grid(color='#222222', linestyle='--', linewidth=0.5)

# Elementos del panel izquierdo (Disco)
cuerpo_disco = patches.Circle((0, 0), 1.0, fill=False, color='#777788', lw=3)
ax1.add_patch(cuerpo_disco)
radio_referencia, = ax1.plot([], [], color='#00aaff', lw=4, label='Radio de Control')
punto_periferia, = ax1.plot([], [], 'o', color='#39ff14', markersize=10)
ax1.legend(loc='lower left')

# Elementos del panel derecho (Gráfica)
curva_velocidad, = ax2.plot([], [], color='#00aaff', lw=2, label='Curva de Disipación')
marcador_grafica, = ax2.plot([], [], 'o', color='#39ff14', markersize=8)
ax2.legend(loc='upper right')

# Cuadro telemétrico 
cuadro_texto = ax1.text(-1.4, 1.4, '', fontsize=10, verticalalignment='top', color='white', family='monospace',
                        bbox=dict(boxstyle='round', facecolor='#111115', alpha=0.9, edgecolor='#00aaff'))

def animar(i):
    t_actual = t[i]
    ang_actual = theta[i]
    w_actual = w[i]
    alpha_actual = alpha[i]
    
    # Calcular coordenadas cartesianas del punto de control del disco (x = R*cos(θ), y = R*sin(θ))
    rx = np.cos(ang_actual)
    ry = np.sin(ang_actual)
    
    # Actualizar dibujo del disco
    radio_referencia.set_data([0, rx], [0, ry])
    punto_periferia.set_data([rx], [ry])
    
    # Actualizar gráfica de decaimiento
    curva_velocidad.set_data(t[:i], w[:i])
    marcador_grafica.set_data([t_actual], [w_actual])
    
    rpm = (w_actual * 60) / (2 * np.pi)
    torque_friccion = -friccion_eje * w_actual
    
    # TELEMETRÍA DINÁMICA DE ROTACIÓN
    explicacion = f"REPORTE DE ROTACIÓN | Tiempo: {t_actual:.2f} s\n"
    explicacion += "-"*43 + "\n"
    explicacion += f"Vel. Angular (ω) : {w_actual:.2f} rad/s ({rpm:.0f} RPM)\n"
    explicacion += f"Acel. Angular (α): {alpha_actual:.2f} rad/s²\n"
    explicacion += f"Torque de Fricción: τ_f = {torque_friccion:.2f} N·m\n"
    explicacion += f"Momento Inercia(I): {inercia:.1f} kg·m² [Fijo]\n"
    explicacion += "-"*43 + "\n"

    # Explicación física paso a paso
    if w_actual < 0.2:
        explicacion += "ESTADO: EQUILIBRIO EN REPOSO\n"
        explicacion += "La energía cinética rotacional se disipó\n"
        explicacion += "por completo en forma de calor en el eje."
        punto_periferia.set_color('#ff3333')
    elif t_actual < 1.5:
        explicacion += "FASÉ 1: CORTE DE ENERGÍA\n"
        explicacion += "El motor se apaga. El objeto sigue girando\n"
        explicacion += "por pura Inercia Rotacional (Ley de Inercia).\n"
        explicacion += "La fricción empieza a restar momento angular."
    elif t_actual < 4.0:
        explicacion += "FASE 2: DESACELERACIÓN NO LINEAL\n"
        explicacion += "Al bajar las RPM, el torque de fricción\n"
        explicacion += "también disminuye. La pérdida de velocidad\n"
        explicacion += "se vuelve asintótica (curva exponencial).\n"
        explicacion += "Ecuación: α = τ_friccion / Inercia"
    else:
        explicacion += "FASE 3: AGOTAMIENTO DE MOMENTO\n"
        explicacion += "La velocidad residual es baja.\n"
        explicacion += "El rozamiento mecánico consume los últimos\n"
        explicacion += "Joules de energía cinética del sólido."

    cuadro_texto.set_text(explicacion)
    return radio_referencia, punto_periferia, curva_velocidad, marcador_grafica, cuadro_texto

# Ejecución de la animación
animacion = FuncAnimation(fig, animar, frames=len(t), interval=45, blit=False)

print("Procesando dinámicas del Cuerpo Rígido...")
animacion.save('rigido_laboratorio_lento.gif', fps=22, writer='pillow')
print("¡Listo! Archivo 'rigido_laboratorio_lento.gif'.")