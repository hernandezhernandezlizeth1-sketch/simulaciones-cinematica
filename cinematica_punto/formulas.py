# Fórmulas de MRUV / Tiro Parabólico
def pos_x(x0, vx, t): 
    return x0 + vx * t

def pos_y(y0, vy, a, t): 
    return y0 + vy * t + 0.5 * a * (t ** 2)

def vel_y(vy, a, t): 
    return vy + a * t