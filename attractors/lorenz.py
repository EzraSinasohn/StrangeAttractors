def generate(prandtl, rayleigh, geo, x0, y0, z0, dt, steps):
    x = x0
    y = y0
    z = z0
    x_values = [x0]
    y_values = [y0]
    z_values = [z0]

    for _ in range(steps):
        dx = prandtl * (y - x)
        dy = x * (rayleigh - z) - y
        dz = x * y - geo * z
        x += dx * dt
        y += dy * dt
        z += dz * dt
        x_values.append(x)
        y_values.append(y)
        z_values.append(z)

    return x_values, y_values, z_values
