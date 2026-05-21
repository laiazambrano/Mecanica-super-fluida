import numpy as np
from parameters import *

def downforce_calc(P, h, x, fluid_limit, y):
    Nx = len(x)
    pressure_down = np.zeros(Nx)

    for i in range(Nx):
        h_i = h[0, i]
        y_target = 0.8 * h_i
        j = np.argmin(np.abs(y - y_target))
        pressure_down[i] = P[j, i]

    # remove nan values before integrating
    valid = ~np.isnan(pressure_down)

    downforce = np.trapezoid(
        Pref - pressure_down[valid],
        x[valid]
    )

    return pressure_down, downforce