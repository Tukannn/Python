import numpy as np
import matplotlib.pyplot as plt
from cvxpy import *

# System parameters
m = 0.5 # mass (kg)
g = 9.81 # gravitational acceleration (m/s^2)
I = np.diag([1, 1, 1]) # moment of inertia matrix (kg*m^2)
invI = np.linalg.inv(I)
L = 0.25 # arm length (m)

# State space model
A = np.zeros((12,12))
A[0:6,6:12] = np.eye(6)
A[6,4] = -g
A[7,3] = g
B = np.zeros((12,4))
B[9,:] = 1/m
B[9:12,:] = invI @ [[L,0,-L,0],[0,-L,0,L],[1,-1,1,-1]]

# MPC parameters
N = 10 # prediction horizon
nx = A.shape[0] # number of states
nu = B.shape[1] # number of inputs

# MPC optimization problem
x = Variable((nx,N+1))
u = Variable((nu,N))
x_init = Parameter(nx)
x_ref = Parameter(nx)
Q = np.diag([10,10,10,1,1,1,1,1,1,1,1,1])
R = np.diag([1e-6,1e-6,1e-6,1e-3])
objective = 0
constraints = [x[:,0] == x_init]
for k in range(N):
    objective += quad_form(x[:,k]-x_ref,Q) + quad_form(u[:,k],R)
    constraints += [x[:,k+1] == A@x[:,k] + B@u[:,k]]
prob = Problem(Minimize(objective),constraints)

# Simulation
Tsim = 10 # simulation time (s)
dt = 0.01 # time step (s)
Nsim = int(Tsim/dt) # number of time steps
t_sim = np.linspace(0,Tsim,Nsim) # time array

x0_sim = [1.5,-0.5,np.pi/4,np.pi/6,np.pi/16,np.pi/32] + [0]*6 # initial state
x_sim = np.zeros((Nsim,len(x0_sim)))
x_sim[0,:] = x0_sim

u_sim = np.zeros((Nsim-1,len(R)))
for i in range(Nsim-1):
    x_init.value = x_sim[i,:]
    x_ref.value = [0]*nx
    prob.solve()
    u_sim[i,:] = u[:,0].value
    x_sim[i+1,:] = A @ x_sim[i,:] + B @ u_sim[i,:]

# Define waypoints
waypoints = [[0, 0, 1], [0, 0, 2], [0, 0, 3]]
waypoint_idx = 0

for i in range(Nsim - 1):
    x_init.value = x_sim[i, :]

    # Update reference state based on waypoint sequence
    if np.abs(x_sim[i, 2] - waypoints[waypoint_idx][2]) < 0.1:
        waypoint_idx += 1
    x_ref.value = waypoints[waypoint_idx] + [0] * (nx - 3)

    prob.solve()
    u_sim[i, :] = u[:, 0].value
    x_sim[i + 1, :] = A @ x_sim[i, :] + B @ u_sim[i, :]


# Plot results
plt.figure()
plt.subplot(3,2,1)
plt.plot(t_sim,x_sim[:,0])
plt.ylabel('x (m)')
plt.subplot(3,2,3)
plt.plot(t_sim,x_sim[:,1])
plt.ylabel('y (m)')
plt.subplot(3,2,5)
plt.plot(t_sim,x_sim[:,2])
plt.ylabel('z (m)')
plt.xlabel('Time (s)')
plt.subplot(3,2,2)
plt.plot(t_sim,x_sim[:,3]*180/np.pi)
plt.ylabel('Roll (deg)')
plt.subplot(3,2,4)
plt.plot(t_sim,x_sim[:,4]*180/np.pi)
plt.ylabel('Pitch (deg)')
plt.subplot(3,2,6)
plt.plot(t_sim,x_sim[:,5]*180/np.pi)
plt.ylabel('Yaw (deg)')
plt.xlabel('Time (s)')

#plt.figure()
#for i in range(4):
#    plt.subplot(4,1,i+1)
#    plt.plot(t_sim[:-1],u_sim[:,i])
#    plt.ylabel(f'u{i+1}')
#    if i==3:
#        plt.xlabel('Time (s)')

plt.show()