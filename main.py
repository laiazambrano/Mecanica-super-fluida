import matplotlib.pyplot as plt
from geometry import *
from laplace import *
from velocity_pressure_cp import *
from downforce import *

x,y,X,Y,dx,dy=mesh()
fluid_limit,solid_limit,h,front_wheel, rear_wheel=apply_height(X,Y)

###Tunnel geometry plot
plt.figure(figsize=(10,3))
plt.contourf(X,Y,solid_limit)
plt.xlabel('x(m)')
plt.ylabel('y(m))')
plt.title("Tunnel geometry")
plt.tight_layout()
plt.savefig("Tunnel_geometry.png")
plt.show()

print(height(1.32))

###creation of the stream function with boundary conditions
sf=stream_function(Y,h)
sf_boundary=boundary_conditions(sf,Y,h,fluid_limit, front_wheel,rear_wheel)
sf_final=laplace(sf_boundary, fluid_limit,max_iter,tolerance,Y,h,front_wheel,rear_wheel)

###Plot of the streamlines
plt.figure(figsize=(10,3))
plt.contour(X,Y, sf_final, levels=30)
plt.contourf(X,Y,solid_limit, levels=1, alpha=0.3)
plt.xlabel('x(m)')
plt.ylabel('y(m)')
plt.title('Streamlines')
plt.tight_layout()
plt.savefig("Tunnel_streamlines.png")
plt.show()

###computing velocity
u, v, V = velocity(sf_final, dx, dy, fluid_limit)

###plot of the velocity field
V_plot = V.copy()
V_plot[solid_limit] = np.nan
plt.figure(figsize=(10, 3))
cf = plt.contourf(X, Y, V_plot, levels=100)
plt.contourf(X, Y, solid_limit, levels=1, alpha=0.3)
plt.colorbar(cf, label='Velocity magnitude [m/s]')
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.title('Velocity field')
plt.tight_layout()
plt.savefig("Tunnel_velocity_field.png")
plt.show()


###plot of the pressure field
P=pressure(V)
plt.figure(figsize=(10,3))
plt.contourf(X,Y,P, levels=30)
plt.contourf(X,Y,solid_limit, levels=1, alpha=0.3)
cf = plt.contourf(X, Y, P, levels=100)
plt.colorbar(cf,label='Pressure [Pa]')
plt.title('Pressure field')
plt.xlabel('x(m)')
plt.ylabel('y(m)')
plt.tight_layout()
plt.savefig("Tunnel_pressure_field.png")
plt.show()




###plot of the cp
cp=cp(P)
plt.figure(figsize=(10,3))
plt.contourf(X,Y,cp, levels=30)
plt.contourf(X,Y,solid_limit, levels=1, alpha=0.3)
cf = plt.contourf(X, Y, cp, levels=100)
plt.colorbar(cf,label='Pressure coefficient')
plt.title('Pressure coefficient field')
plt.xlabel('x(m)')
plt.ylabel('y(m)')
plt.tight_layout()
plt.savefig("Tunnel_p_coef_field.png")
plt.show()


###plot of the mean velocity along the tunnel
V_plot = V.copy()
V_plot[solid_limit] = np.nan
V_plot[V_plot > 600] = 600

valid_columns = ~np.all(np.isnan(V_plot), axis=0)

V_mean = np.nanmean(V_plot[:, valid_columns], axis=0)
x_valid = x[valid_columns]

plt.figure()
plt.plot(x_valid, V_mean)
plt.xlabel("x(m)")
plt.ylabel("Mean velocity (m/s)")
plt.title("Mean velocity along the tunnel")
plt.grid()
plt.tight_layout()
plt.savefig("Tunnel_mean_velocity.png")
plt.show()

###downforce computation
pressure_down,downforce=downforce_calc(P,h,x,fluid_limit,y)
print(f"Downforce per unit width: {downforce} N/m")

plt.figure(figsize=(10,3))
plt.plot(x,pressure_down)
plt.xlabel("x (m)")
plt.ylabel("Pressure (Pa)")
plt.title("Pressure distribution under the car")
plt.grid()
plt.savefig("Pressure_under_car.png")
plt.show()
