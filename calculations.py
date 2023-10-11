import numpy as np
G = 6.67e-11
V = 299792458

def get_a(i, x, y, planets):
    a = 0
    for j in range(len(planets)):
        if i != j:
            a += G * planets[j]['M'] * (x[j][-1] - x[i][-1]) / (((x[j][-1] - x[i][-1]) ** 2 + (y[j][-1] - y[i][-1]) ** 2) ** 0.5) ** 3
            #print("DO", a)
            #print("AF", a)
    return a


def scheme_Euler(time, step_time, planets):
    #planets.sort(key=lambda planet: planet[4])
    n = len(planets)
    x = []
    y = []
    vx = []
    vy = []
    ax = []
    ay = []
    for i in range(n):
        x.append([])
        y.append([])
        vx.append([])
        vy.append([])
        ax.append([])
        ay.append([])
        x[i].append(planets[i]['X'])
        y[i].append(planets[i]['Y'])
        vx[i].append(planets[i]['vX'])
        vy[i].append(planets[i]['vY'])
    for i in range(n):
        ax[i].append(get_a(i, x, y, planets))
        ay[i].append(get_a(i, y, x, planets))
    t = np.arange(0, time + step_time / 2, step_time)
    for j in range(len(t) - 1):
        for i in range(n):
            x[i].append(x[i][-1] + vx[i][-1] * step_time) #+ ax[i][-1] * (step_time ** 2) / 2)
            y[i].append(y[i][-1] + vy[i][-1] * step_time) # ay[i][-1] * (step_time ** 2) / 2)
            vx[i].append(vx[i][-1] + ax[i][-1] * step_time)
            vy[i].append(vy[i][-1] + ay[i][-1] * step_time)
        for i in range(n):
            ax[i].append(get_a(i, x, y, planets))
            ay[i].append(get_a(i, y, x, planets))
    return t, x, y, vx, vy


def scheme_Euler_Kramer(time, step_time, planets):
    #planets.sort(key=lambda planet: planet[4])

    n = len(planets)
    x = []
    y = []
    vx = []
    vy = []
    ax = []
    ay = []
    for i in range(n):
        print(type(planets[i]['X']))
        x.append([])
        y.append([])
        vx.append([])
        vy.append([])
        ax.append([])
        ay.append([])
        x[i].append(planets[i]['X'])
        y[i].append(planets[i]['Y'])
        vx[i].append(planets[i]['vX'])
        vy[i].append(planets[i]['vY'])
    for i in range(n):
        ax[i].append(get_a(i, x, y, planets))
        ay[i].append(get_a(i, y, x, planets))
    t = np.arange(0, time + step_time / 2, step_time)
    for j in range(len(t) - 1):
        for i in range(n):
            vx[i].append(vx[i][-1] + ax[i][-1] * step_time)
            vy[i].append(vy[i][-1] + ay[i][-1] * step_time)
            x[i].append(x[i][-1] + vx[i][-1] * step_time)
            y[i].append(y[i][-1] + vy[i][-1] * step_time)
        for i in range(n):
            ax[i].append(get_a(i, x, y, planets))
            ay[i].append(get_a(i, y, x, planets))
    return t, x, y, vx, vy


def scheme_Verle(time, step_time, planets):
    #planets.sort(key=lambda planet: planet[4])
    n = len(planets)
    x = []
    y = []
    vx = []
    vy = []
    ax = []
    ay = []
    for i in range(n):
        x.append([])
        y.append([])
        vx.append([])
        vy.append([])
        ax.append([])
        ay.append([])
        x[i].append(planets[i]['X'])
        y[i].append(planets[i]['Y'])
        vx[i].append(planets[i]['vX'])
        vy[i].append(planets[i]['vY'])
    for i in range(n):
        ax[i].append(get_a(i, x, y, planets))
        ay[i].append(get_a(i, y, x, planets))
    t = np.arange(0, time + step_time / 2, step_time)
    for i in range(n):
        x[i].append(x[i][-1] + vx[i][-1] * step_time)
        y[i].append(y[i][-1] + vy[i][-1] * step_time)
        vx[i].append(vx[i][-1] + ax[i][-1] * step_time)
        vy[i].append(vy[i][-1] + ay[i][-1] * step_time)
    for i in range(n):
        ax[i].append(get_a(i, x, y, planets))
        ay[i].append(get_a(i, y, x, planets))
    for i in range(n):
        x[i].append(2 * x[i][-1] - x[i][-2] + ax[i][-1] * step_time ** 2)
        y[i].append(2 * y[i][-1] - y[i][-2] + ay[i][-1] * step_time ** 2)
    for i in range(n):
        ax[i].append(get_a(i, x, y, planets))
        ay[i].append(get_a(i, y, x, planets))
    for j in range(len(t) - 3):
        for i in range(n):
            x[i].append(2 * x[i][-1] - x[i][-2] + ax[i][-1] * step_time ** 2)
            y[i].append(2 * y[i][-1] - y[i][-2] + ay[i][-1] * step_time ** 2)
            vx[i].append((x[i][-1] - x[i][-3]) / (2 * step_time))
            vy[i].append((y[i][-1] - y[i][-3]) / (2 * step_time))
        for i in range(n):
            ax[i].append(get_a(i, x, y, planets))
            ay[i].append(get_a(i, y, x, planets))
    for i in range(n):
        vx[i].append((x[i][-1] - x[i][-3]) / (2 * step_time))
        vy[i].append((y[i][-1] - y[i][-3]) / (2 * step_time))
    print('AX', len(ax[0]))
    print('X', len(x[0]))
    print('VX', len(vx[0]))
    return t, x, y, vx, vy


def scheme_Biman(time, step_time, planets):
    #planets.sort(key=lambda planet: planet[4])
    n = len(planets)
    x = []
    y = []
    vx = []
    vy = []
    ax = []
    ay = []
    for i in range(n):
        x.append([])
        y.append([])
        vx.append([])
        vy.append([])
        ax.append([])
        ay.append([])
        x[i].append(planets[i]['X'])
        y[i].append(planets[i]['Y'])
        vx[i].append(planets[i]['vX'])
        vy[i].append(planets[i]['vY'])
    for i in range(n):
        ax[i].append(get_a(i, x, y, planets))
        ay[i].append(get_a(i, y, x, planets))
    t = np.arange(0, time + step_time / 2, step_time)
    for i in range(n):
        x[i].append(x[i][-1] + vx[i][-1] * step_time)
        y[i].append(y[i][-1] + vy[i][-1] * step_time)
        vx[i].append(vx[i][-1] + ax[i][-1] * step_time)
        vy[i].append(vy[i][-1] + ay[i][-1] * step_time)
    for i in range(n):
        ax[i].append(get_a(i, x, y, planets))
        ay[i].append(get_a(i, y, x, planets))
    for j in range(len(t) - 2):
        for i in range(n):
            x[i].append(x[i][-1] + vx[i][-1] * step_time - ((4 * ax[i][-1] - ax[i][-2]) * step_time ** 2) / 6)
            y[i].append(y[i][-1] + vy[i][-1] * step_time - ((4 * ay[i][-1] - ay[i][-2]) * step_time ** 2) / 6)
        for i in range(n):
            ax[i].append(get_a(i, x, y, planets))
            ay[i].append(get_a(i, y, x, planets))
        for i in range(n):
            vx[i].append(vx[i][-1] + (2 * ax[i][-1] + 5 * ax[i][-2] - ax[i][-3]) * step_time / 6)
            vy[i].append(vy[i][-1] + (2 * ay[i][-1] + 5 * ay[i][-2] - ay[i][-3]) * step_time / 6)
    print('AX', len(ax[0]))
    print('X', len(x[0]))
    print('VX', len(vx[0]))
    return t, x, y, vx, vy