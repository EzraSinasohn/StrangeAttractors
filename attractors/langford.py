def generate(a, b, c, d, e, f, x0, y0, z0, dt, steps):
    x = x0
    y = y0
    z = z0
    x_values = [x0]
    y_values = [y0]
    z_values = [z0]

    for _ in range(steps):
        dx = (z - b) * x - d * y
        dy = d * x + (z - b) * y
        dz = (
            c
            + a * z
            - z**3 / 3
            - (x**2 + y**2) * (1 + e * z)
            + f * z * x**3
        )
        x += dx * dt
        y += dy * dt
        z += dz * dt
        x_values.append(x)
        y_values.append(y)
        z_values.append(z)

    return x_values, y_values, z_values
