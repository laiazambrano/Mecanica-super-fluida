import matplotlib.pyplot as plt
from parameters import *
import numpy as np

###this function returns the height depending on x
def height(x):
    '''
    if 0<=x<=0.256: #or 1.32<x<=1.5:
        return hmin+(hin-hmin)/2*(1+np.cos(np.pi*x/Lv))#we used this formula for a soft reduction
    elif 0.256<x<=1.32:
        return np.sqrt(0.55**2-(x-0.8)**2)+0.35
    elif 1.32<x<=2:
        return 1.2458-x*0.5429
    elif 2<x<=4:
        return hmin
    elif 4<x<=5.66:
        return hmin+(x-4)*np.tan(alpha_rad)
    elif 5.66<x<=6.727:
        return np.sqrt(0.55**2-(x-6.2)**2)+0.35
    else:
        return hout
    '''
    return 1.5


def mesh():
    x=np.linspace(0,L,Nx)
    y=np.linspace(0,H,Ny)

    X,Y=np.meshgrid(x,y)

    dx=x[1]-x[0]
    dy=y[1]-y[0]

    return x,y,X,Y,dx,dy

def apply_height(X,Y):
    #apply height function to every x position
    ##functions of front and rear wheels

    h=np.vectorize(height)(X)
    # wheels as solid circles
    front_wheel = ((X - xwf) ** 2 + (Y - yw) ** 2) <= R ** 2
    rear_wheel = ((X - xwr) ** 2 + (Y - yw) ** 2) <= R ** 2
    #fluid below tunnel upper limit
    fluid_limit=Y<=h
    #fluid above tunnel upper limit
    solid_limit = (Y > h)
    solid_limit = solid_limit | front_wheel | rear_wheel
    fluid_limit = ~solid_limit

    return fluid_limit,solid_limit,h,front_wheel, rear_wheel
