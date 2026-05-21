import numpy as np
from matplotlib.path import Path
import matplotlib.pyplot as plt

#Flow properties
U0=50
density=1.225
Pref=101325

#Geometrical parameters
###Domain length and height
L=7
H=1.5
###Minimum height of the car with respect to the floor
hmin=0.16
hin=0.4##################NOT SPECIFIED IN PROJECT PART 2
###Venturi
Lv=1.5
###Flat floor
Lf=2.5
###Diffuser
Ld=2
alpha=10
###Wheel radius and position of the center
R=0.35
#x wheel front
xwf=2.6
#x wheel rear
xwr=6.2
#y of both wheels
yw=0.35

# upper compartment wheel
body_y = 1.0
body_x1 = 0.4
body_x2 = 6.6

#Numerical parameters
Nx,Ny=200,100
max_iter=1000
tolerance=10**-3

def p_coef(P):
    return (P-Pref)/(0.5*density*U0**2)

###height of the outlet
alpha_rad=alpha*np.pi/180
hout=hmin+Ld*np.sin(alpha_rad)

# upper compartment
H_compartment = 1.0

# 3 DATOS DEL PERFIL ALAR
# perfil NACA 2412 invertido como aproximacion de un aleron de F1
chord = 0.8
camber = 0.04
p_camber = 0.40
thickness = 0.12
angle_deg = -8.0
x_le = 1           # posición borde de ataque
y_le = 0.3           # altura borde de ataque




# devuelve los puntos del contorno cerrado del perfil NACA (sin rotar)
def naca4(c, m, p, t, n):
    x_local = np.linspace(0, c, n)
    xc = x_local/c # x adimensional a lo largo de c

    # espesor del perfil(desde el medio hasta arriba). Formula sacada de: https://en.wikipedia.org/wiki/NACA_airfoil
    yt = 5*t*c*(0.2969*np.sqrt(xc) - 0.1260*xc - 0.3516*xc**2 + 0.2843*xc**3 - 0.1015*xc**4)

    # linea media aproximada
    yc = np.zeros(n)
    dyc = np.zeros(n) # se usa para la inclinacion local del perfil(dyc/dx)
    for k in range(n):
        if xc[k] < p: # si x se encuentra en antes del punto maximo: Formula sacada de: https://en.wikipedia.org/wiki/NACA_airfoil
            yc[k] = m/p**2*(2*p*xc[k] - xc[k]**2)*c
            dyc[k] = 2*m/p**2*(p - xc[k])
        else: # si x se encuentra en despues del punto maximo: Formula sacada de: https://en.wikipedia.org/wiki/NACA_airfoil
            yc[k] = m/(1-p)**2 * ((1 - 2*p) + 2*p*xc[k] - xc[k]**2)*c
            dyc[k] = 2*m/(1 - p)**2*(p - xc[k])

    # angulo local de la linea media
    theta = np.arctan(dyc)
    # superficie superior. Formulas tambien extraidas de: https://en.wikipedia.org/wiki/NACA_airfoil
    x_upper = x_local - yt * np.sin(theta)
    y_upper = yc + yt * np.cos(theta)
    # superficie inferior
    x_lower = x_local + yt * np.sin(theta)
    y_lower = yc - yt * np.cos(theta)

    # Se unen los puntos
    x_profile = np.concatenate([x_upper[::-1], x_lower[1:]])
    y_profile = np.concatenate([y_upper[::-1], y_lower[1:]])

    return x_profile, y_profile, x_upper, y_upper, x_lower, y_lower

xp, yp, xu, yu, xl, yl = naca4(chord, camber, p_camber, thickness, 120)

# invertir perfil para que funcione como aleron de f1
yp = -yp
yu = -yu
yl = -yl

# rotar y colocar el perfil
angle = np.deg2rad(angle_deg)
x_rot = xp*np.cos(angle) - yp*np.sin(angle) + x_le # rotacion en 2D + desplazamiento
y_rot = xp*np.sin(angle) + yp*np.cos(angle) + y_le

xu_rot = xu*np.cos(angle) - yu*np.sin(angle) + x_le # idem pero para los maximos y minimos
yu_rot = xu*np.sin(angle) + yu*np.cos(angle) + y_le
xl_rot = xl*np.cos(angle) - yl*np.sin(angle) + x_le
yl_rot = xl*np.sin(angle) + yl*np.cos(angle) + y_le


