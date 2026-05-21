import numpy as np

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
xwf=0.8
#x wheel rear
xwr=6.2
#y of both wheels
yw=0.35

# upper compartment wheel
body_y = 1.0
body_x1 = 0.4
body_x2 = 6.6

#Numerical parameters
Nx,Ny=100,50
max_iter=1000
tolerance=10**-3

def p_coef(P):
    return (P-Pref)/(0.5*density*U0**2)

###height of the outlet
alpha_rad=alpha*np.pi/180
hout=hmin+Ld*np.sin(alpha_rad)

# upper compartment
H_compartment = 1.0


