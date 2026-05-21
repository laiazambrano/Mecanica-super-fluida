import numpy as np
from parameters import *
from geometry import *

#sf=stream function
def stream_function(Y,h):
    sf=U0*Y
    sf[Y>h]=np.nan
    return sf

#boundary conditions
#ground: sf=0
def boundary_conditions(sf,Y,h,fluid_limit, front_wheel, rear_wheel):
    Ny,Nx=sf.shape
    sf[0,:]=0
    #inlet: sf=U0*Y
    sf[:,0]=U0*Y[:,0]
    sf[~fluid_limit[:,0],0]=np.nan
    #sf[Y[:, 0] > h[0, 0], 0] = np.nan
    #outlet: d(sf)/dx=0
    sf[:,-1]=sf[:,-2]
    #sf_top=U0*hin
    #upper wall of the tunnel
    for i in range(Nx):
    #to find the fluid points in this vertical column
        fluid_indices=np.where(fluid_limit[:,i])[0]
        #if len(fluid_indices)>0:
            #j_top=fluid_indices[-1]
            #sf[j_top,i]=sf_top
    # wheels: since they touch the ground, same streamline as ground
    sf[front_wheel] = 0
    sf[rear_wheel] = 0

    # other solid parts, but NOT the wheels
    other_solid = (~fluid_limit) & (~front_wheel) & (~rear_wheel)
    sf[other_solid] = np.nan

    return sf


#applying Laplace
def laplace(sf,fluid_limit,max_iter,tolerance,Y,h, front_wheel, rear_wheel):
    Ny,Nx=sf.shape
    for ite in range(max_iter):
        sf_old=sf.copy()
        for j in range(1,Ny-1):
            for i in range(1,Nx-1):
                if fluid_limit[j,i]:
                    neighbors=[
                        sf[j+1,i],
                        sf[j-1,i],
                        sf[j,i-1],
                        sf[j,i+1]
                    ]
                    valid_neighbors = [
                        value for value in neighbors
                        if not np.isnan(value)
                    ]
                    if len(valid_neighbors)>0:
                        sf[j,i]=np.mean(valid_neighbors)
        sf = boundary_conditions(sf,Y,h,fluid_limit,front_wheel,rear_wheel)
        error = np.nanmax(np.abs(sf-sf_old))
        if error<tolerance:
            print(f"Converged after {ite} iterations")
            break
    return sf
