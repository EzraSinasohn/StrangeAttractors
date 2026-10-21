import numpy as np
import matplotlib.pyplot as plt
prandtl = 10
rayleigh = 28
geo = 8.0/3.0
tb = 0.208186
la = 0.95
lb = 0.7
lc = 0.6
ld = 3.5
le = 0.25
lf = 0.1
ra = 0.2
rb = 0.2
rc = 5.7
x0 = 0.1
y0 = 0
z0 = 0
dt = 0.01
N = 10000
yaw = -45
pitch = 15

def lorenz(prandtl, rayleigh, geo, x0, y0, z0, dt, N):
    x = x0
    y = y0
    z = z0
    x_list = [x0]
    y_list = [y0]
    z_list = [z0]
    for i in range(N):
        dx = prandtl*(y-x)
        dy = x*(rayleigh-z)-y
        dz = (x*y)-(geo*z)
        x += dx * dt
        y += dy * dt
        z += dz * dt
        x_list.append(x)
        y_list.append(y)
        z_list.append(z)
    return [x_list, y_list, z_list]

def thomas(b, x0, y0, z0, dt, N):
    x = x0
    y = y0
    z = z0
    x_list = [x0]
    y_list = [y0]
    z_list = [z0]
    for i in range(N):
        dx = np.sin(y) - (b * x)
        dy = np.sin(z) - (b * y)
        dz = np.sin(x) - (b * z)
        x += dx * dt
        y += dy * dt
        z += dz * dt
        x_list.append(x)
        y_list.append(y)
        z_list.append(z)
    return [x_list, y_list, z_list]

def langford(a, b, c, d, e, f, x0, y0, z0, dt, N):
    x = x0
    y = y0
    z = z0
    x_list = [x0]
    y_list = [y0]
    z_list = [z0]
    for i in range(N):
        dx = (z - b) * x - d * y
        dy = d * x + (z - b) * y
        dz = c + a * z - ((z ** 3) / 3) - ((x ** 2) + (y ** 2)) * (1 + e * z) + f * z * (x ** 3)
        x += dx * dt
        y += dy * dt
        z += dz * dt
        x_list.append(x)
        y_list.append(y)
        z_list.append(z)
    return [x_list, y_list, z_list]

def rossler(a, b, c, x0, y0, z0, dt, N):
    x = x0
    y = y0
    z = z0
    x_list = [x0]
    y_list = [y0]
    z_list = [z0]
    for i in range(N):
        dx = -y - z
        dy = x + a * y
        dz = b + z * (x - c)
        x += dx * dt
        y += dy * dt
        z += dz * dt
        x_list.append(x)
        y_list.append(y)
        z_list.append(z)
    return [x_list, y_list, z_list]

def plot_attractor(values, yaw = -45, pitch = 15):
    graph_3d_figure = plt.figure(2)
    graph_3d = graph_3d_figure.add_subplot(projection = '3d')
    graph_3d.view_init(azim = yaw, elev = pitch)
    graph_3d.plot3D(values[0], values[1], values[2], linewidth = 0.5)
    
def timelapse(values, yaw = -45, pitch = 15, spin = True):
    for i in range(0, len(values[0]), 10):
        graph_3d_figure = plt.figure(1)
        graph_3d = graph_3d_figure.add_subplot(projection = '3d')
        if spin:
            graph_3d.view_init(azim = 0.5 * i, elev = pitch)
        else:
            graph_3d.view_init(azim = yaw, elev = pitch)
        graph_3d.plot3D(values[0][0:i], values[1][0:i], values[2][0:i], linewidth = 0.5)
        plt.pause(0.0001)

def timelapse1(values, yaw = -45, pitch = 15, spin = True):
    for i in range(0, len(values[0]), 10):
        graph_3d_figure = plt.figure(1)
        graph_3d = graph_3d_figure.add_subplot(projection = '3d')
        if spin:
            graph_3d.view_init(azim = -90 + np.atan2(values[0][i], values[2][i])*180/np.pi, elev = pitch)
        else:
            graph_3d.view_init(azim = yaw, elev = pitch)
        graph_3d.plot3D(values[0][0:i], values[1][0:i], values[2][0:i], linewidth = 0.5)
        plt.pause(0.0001)
        
def cycle(values, speed = 10, pitch = 15):
    for i in range(0, 361, speed):
        graph_3d_figure = plt.figure(1)
        graph_3d = graph_3d_figure.add_subplot(projection = '3d')
        graph_3d.view_init(azim = i, elev = pitch)
        graph_3d.plot3D(values[0], values[1], values[2])
        plt.pause(0.001)
        
lorenz_plot = lorenz(prandtl, rayleigh, geo, x0, y0, z0, dt, N)
thomas_plot = thomas(tb, x0, y0, z0, dt, N)
langford_plot = langford(la, lb, lc, ld, le, lf, x0, y0, z0, dt, N)
rossler_plot = rossler(ra, rb, rc, x0, y0, z0, dt, N)
#plot_attractor(lorenz_plot, 90, 0)
#plot_attractor(thomas_plot, 45)
#cycle(langford_plot)
#plot_attractor(langford_plot)
#plot_attractor(rossler_plot)
#timelapse(lorenz_plot, 90, 0, False)
timelapse1(lorenz_plot)
#timelapse(thomas_plot)
