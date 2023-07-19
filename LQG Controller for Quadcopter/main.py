import numpy as np
from scipy import signal
from control import lqr


# Define the system constants
m = 1.0  # Mass of the quadcopter
g = 9.81  # Gravity
l = 0.25  # Length of each arm
Ixx = 0.05  # Moment of inertia in x-axis
Iyy = 0.05  # Moment of inertia in y-axis
Izz = 0.1  # Moment of inertia in z-axis


# System matrices
A = np.array([[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, -g, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, g, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

B = np.array([[0, 0, 0, 0],
[0, 0, 0, 0],
[0, 0, 0, 0],
[0, 0, 0, 0],
[1/m, 0, 0, 0],
[0, 0, 0, 0],
[0, 0, 0, 0],
[0, 0, 0, 0],
[0, 0, 0, 0],
[0, 1/Ixx, 0, 0],
[0, 0, 1/Iyy, 0],
[0, 0, 0, 1/Izz]])

C = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]])

D = np.zeros((6, 4))

# LQR controller design
Q = np.eye(A.shape[0])
R = np.array([[0.1, 0, 0, 0],
              [0, 10, 0, 0],
              [0, 0, 10, 0],
              [0, 0, 0, 10]])
K, S, E = lqr(A, B, Q, R)

# Kalman filter design
W = np.array([[27]])  # process noise covariance
V = np.array([[28]])  # measurement noise covariance
_, L, _ = signal.lqe(A, W, C, V)


# LQG controller
class LQGController:
    def __init__(self):
        self.x_hat = np.zeros((A.shape[1], B.shape[1]))

    def update(self, y):
        # Kalman filter update
        self.x_hat += L * (y - C @ self.x_hat)

        # Compute control input
        u = -K @ self.x_hat

        # Update state estimate
        self.x_hat = A @ self.x_hat + B * u

        return u


# Example usage
lqg = LQGController()
y = np.array([[29]])  # measurement
u = lqg.update(y)



