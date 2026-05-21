import numpy as np
from parameters import *

def velocity(sf, dx, dy, fluid_limit):
    Ny,Nx=sf.shape
    u=np.zeros((Ny,Nx))
    v=np.zeros((Ny,Nx))
    u[:]=np.nan
    v[:]=np.nan
    for j in range(1,Ny-1):
        for i in range(1,Nx-1):
            valid=(
                fluid_limit[j,i]
                and fluid_limit[j+1,i]
                and fluid_limit[j-1,i]
                and fluid_limit[j,i+1]
                and fluid_limit[j,i-1]
            )
            if valid:
                # u=d(sf)/dy
                u[j,i]=(sf[j+1,i]-sf[j-1,i])/(2*dy)
                # v=-d(sf)/dx
                v[j,i]=-(sf[j,i+1]-sf[j,i-1])/(2*dx)
    V=np.sqrt(u**2+v**2)
    return u,v,V

def pressure(V):
    return Pref+0.5*density*(U0**2-V**2)

def cp(P):
    return (P-Pref)/(0.5*density*U0**2)