import numpy as np
G = 6.67e-11

def get_a(i, x, y, density, spaceDensity, v, vf, planets, flag):
    a = 0
    #print(spaceDensity)
    atan = 0
    for j in range(len(planets)):
        if i != j:
            if flag:
                if v[j][-1] < 1e-9 and vf[j][-1] > 0:
                    atan = np.pi / 2
                elif v[j][-1] < 1e-9 and vf[j][-1] < 0:
                    atan = 3*np.pi / 2
                elif v[j][-1] < 1e-9 and vf[j][-1] < 1e-9:
                    atan = 0
                else:
                    atan = np.arctan(abs(v[j][-1] / vf[j][-1]))
                a += (G * planets[j]['M'] * (x[j][-1] - x[i][-1]) / (((x[j][-1] - x[i][-1]) ** 2 + (y[j][-1] - y[i][-1]) ** 2) ** 0.5) ** 3)#x
                #a -= (((9 * np.pi /128) ** (1 / 3)) * (planets[j]['C_F'] * spaceDensity * v[i][-1] ** 2 / ((planets[j]['M'] * density ** 2) ** (1 / 3)))) * np.cos(abs(atan))
            else:
                if vf[j][-1] < 1e-9 and v[j][-1] > 0:
                    atan = np.pi / 2
                elif vf[j][-1] < 1e-9 and v[j][-1] < 0:
                    atan = 3*np.pi / 2
                elif vf[j][-1] < 1e-9 and v[j][-1] < 1e-9:
                    atan = 0
                else:
                    atan = np.arctan(abs(vf[j][-1] / v[j][-1]))
                a += (G * planets[j]['M'] * (x[j][-1] - x[i][-1]) / (
                            ((x[j][-1] - x[i][-1]) ** 2 + (y[j][-1] - y[i][-1]) ** 2) ** 0.5) ** 3) # y
               # a -= (((9 * np.pi / 128) ** (1 / 3)) * (planets[j]['C_F'] * spaceDensity * v[i][-1] ** 2 / (
                           # (planets[j]['M'] * density ** 2) ** (1 / 3)))) * np.sin(abs(atan))
        elif i == j:
            if flag:
                if v[j][-1] < 1e-9 and vf[j][-1] > 0:
                    atan = np.pi / 2
                elif v[j][-1] < 1e-9 and vf[j][-1] < 0:
                    atan = 3*np.pi / 2
                elif v[j][-1] < 1e-9 and vf[j][-1] < 1e-9:
                    atan = 0
                else:
                    atan = np.arctan(abs(v[j][-1] / vf[j][-1]))
               # a += (G * planets[j]['M'] * (x[j][-1] - x[i][-1]) / (((x[j][-1] - x[i][-1]) ** 2 + (y[j][-1] - y[i][-1]) ** 2) ** 0.5) ** 3)#x
                a -= (((9 * np.pi /128) ** (1 / 3)) * (planets[j]['C_F'] * spaceDensity * v[i][-1] ** 2 / ((planets[j]['M'] * density ** 2) ** (1 / 3)))) * np.cos(abs(atan))
            else:
                if vf[j][-1] < 1e-9 and v[j][-1] > 0:
                    atan = np.pi / 2
                elif vf[j][-1] < 1e-9 and v[j][-1] < 0:
                    atan = 3*np.pi / 2
                elif vf[j][-1] < 1e-9 and v[j][-1] < 1e-9:
                    atan = 0
                else:
                    atan = np.arctan(abs(vf[j][-1] / v[j][-1]))
                #a += (G * planets[j]['M'] * (x[j][-1] - x[i][-1]) / (
                            #((x[j][-1] - x[i][-1]) ** 2 + (y[j][-1] - y[i][-1]) ** 2) ** 0.5) ** 3) # y
                a -= (((9 * np.pi / 128) ** (1 / 3)) * (planets[j]['C_F'] * spaceDensity * v[i][-1] ** 2 / (
                            (planets[j]['M'] * density ** 2) ** (1 / 3)))) * np.sin(abs(atan))
            #a += G * planets[j]['M'] * (x[j][-1] - x[i][-1]) / (((x[j][-1] - x[i][-1]) ** 2 + (y[j][-1] - y[i][-1]) ** 2) ** 0.5) ** 3
            #a += ((9 * np.pi /128) ** (1 / 3)) * (planets[j]['C_F'] * spaceDensity * v[i][-1] ** 2 / ((planets[j]['M'] * density ** 2) ** (1 / 3)))
    return a


def scheme_Euler(time, step_time, density, spaceDensity, planets):
    n = len(planets)
    x,y,vx,vy,ax,ay = [[],[],[],[],[],[]]
    for i in range(n):
        x.append([]), y.append([]), vx.append([]), vy.append([]), ax.append([]), ay.append([])
        x[i].append(planets[i]['X'])
        y[i].append(planets[i]['Y'])
        vx[i].append(planets[i]['vX'])
        vy[i].append(planets[i]['vY'])
    for i in range(n):
        ax[i].append(get_a(i, x, y, density, spaceDensity, vx, ay, ax, planets, 1))
        ay[i].append(get_a(i, y, x, density, spaceDensity, vx, ay, ax, planets, 0))
    t = np.arange(0, time + step_time / 2, step_time)
    for j in range(len(t) - 1):
        for i in range(n):
            x[i].append(x[i][-1] + vx[i][-1] * step_time) #+ ax[i][-1] * (step_time ** 2) / 2)
            y[i].append(y[i][-1] + vy[i][-1] * step_time) # ay[i][-1] * (step_time ** 2) / 2)
            vx[i].append(vx[i][-1] + ax[i][-1] * step_time)
            vy[i].append(vy[i][-1] + ay[i][-1] * step_time)
        for i in range(n):
            ax[i].append(get_a(i, x, y, density, spaceDensity, vx, ay, ax, planets, 1))
            ay[i].append(get_a(i, y, x, density, spaceDensity, vx, ay, ax, planets, 0))
    return t, x, y, vx, vy


def scheme_Euler_Kramer(time, step_time, density, spaceDensity, planets):
    n = len(planets)
    x,y,vx,vy,ax,ay = [[],[],[],[],[],[]]
    for i in range(n):
        x.append([]), y.append([]), vx.append([]), vy.append([]), ax.append([]), ay.append([])
        x[i].append(planets[i]['X'])
        y[i].append(planets[i]['Y'])
        vx[i].append(planets[i]['vX'])
        vy[i].append(planets[i]['vY'])
    for i in range(n):
        ax[i].append(get_a(i, x, y, density, spaceDensity, vx, vy, planets, 1))
        ay[i].append(get_a(i, y, x, density, spaceDensity, vy, vx, planets, 0))
    t = np.arange(0, time + step_time / 2, step_time)
    for j in range(len(t) - 1):
        for i in range(n):
            vx[i].append(vx[i][-1] + ax[i][-1] * step_time)
            vy[i].append(vy[i][-1] + ay[i][-1] * step_time)
            x[i].append(x[i][-1] + vx[i][-1] * step_time)
            y[i].append(y[i][-1] + vy[i][-1] * step_time)
        for i in range(n):
            ax[i].append(get_a(i, x, y, density, spaceDensity, vx, vy,  planets, 1))
            ay[i].append(get_a(i, y, x, density, spaceDensity, vy, vx, planets, 0))
    return t, x, y, vx, vy


def scheme_Verle(time, step_time, density, spaceDensity, planets):
    n = len(planets)
    x,y,vx,vy,ax,ay = [[],[],[],[],[],[]]
    for i in range(n):
        x.append([]), y.append([]), vx.append([]), vy.append([]), ax.append([]), ay.append([])
        x[i].append(planets[i]['X'])
        y[i].append(planets[i]['Y'])
        vx[i].append(planets[i]['vX'])
        vy[i].append(planets[i]['vY'])
    for i in range(n):
        ax[i].append(get_a(i, x, y, density, spaceDensity, vx, planets, 1))
        ay[i].append(get_a(i, y, x, density, spaceDensity, vx, planets, 0))
    t = np.arange(0, time + step_time / 2, step_time)
    for i in range(n):
        x[i].append(x[i][-1] + vx[i][-1] * step_time)
        y[i].append(y[i][-1] + vy[i][-1] * step_time)
        vx[i].append(vx[i][-1] + ax[i][-1] * step_time)
        vy[i].append(vy[i][-1] + ay[i][-1] * step_time)
    for i in range(n):
        ax[i].append(get_a(i, x, y, density, spaceDensity, vx, planets, 1))
        ay[i].append(get_a(i, y, x, density, spaceDensity, vx, planets, 0))
    for i in range(n):
        x[i].append(2 * x[i][-1] - x[i][-2] + ax[i][-1] * step_time ** 2)
        y[i].append(2 * y[i][-1] - y[i][-2] + ay[i][-1] * step_time ** 2)
    for i in range(n):
        ax[i].append(get_a(i, x, y, density, spaceDensity, vx, planets, 1))
        ay[i].append(get_a(i, y, x, density, spaceDensity, vx, planets, 0))
    for j in range(len(t) - 3):
        for i in range(n):
            x[i].append(2 * x[i][-1] - x[i][-2] + ax[i][-1] * step_time ** 2)
            y[i].append(2 * y[i][-1] - y[i][-2] + ay[i][-1] * step_time ** 2)
            vx[i].append((x[i][-1] - x[i][-3]) / (2 * step_time))
            vy[i].append((y[i][-1] - y[i][-3]) / (2 * step_time))
        for i in range(n):
            ax[i].append(get_a(i, x, y, density, spaceDensity, vx, planets, 1))
            ay[i].append(get_a(i, y, x, density, spaceDensity, vx, planets, 0))
    for i in range(n):
        vx[i].append((x[i][-1] - x[i][-3]) / (2 * step_time))
        vy[i].append((y[i][-1] - y[i][-3]) / (2 * step_time))
    return t, x, y, vx, vy


def scheme_Biman(time, step_time, density, spaceDensity, planets):
    n = len(planets)
    x,y,vx,vy,ax,ay = [[],[],[],[],[],[]]
    for i in range(n):
        x.append([]), y.append([]), vx.append([]), vy.append([]), ax.append([]), ay.append([])
        x[i].append(planets[i]['X'])
        y[i].append(planets[i]['Y'])
        vx[i].append(planets[i]['vX'])
        vy[i].append(planets[i]['vY'])
    for i in range(n):
        ax[i].append(get_a(i, x, y, density, spaceDensity, vx, planets, 1))
        ay[i].append(get_a(i, y, x, density, spaceDensity, vx, planets, 0))
    t = np.arange(0, time + step_time / 2, step_time)
    for i in range(n):
        x[i].append(x[i][-1] + vx[i][-1] * step_time)
        y[i].append(y[i][-1] + vy[i][-1] * step_time)
        vx[i].append(vx[i][-1] + ax[i][-1] * step_time)
        vy[i].append(vy[i][-1] + ay[i][-1] * step_time)
    for i in range(n):
        ax[i].append(get_a(i, x, y, density, spaceDensity, vx, planets, 1))
        ay[i].append(get_a(i, y, x, density, spaceDensity, vx, planets, 0))
    for j in range(len(t) - 2):
        for i in range(n):
            x[i].append(x[i][-1] + vx[i][-1] * step_time - ((4 * ax[i][-1] - ax[i][-2]) * step_time ** 2) / 6)
            y[i].append(y[i][-1] + vy[i][-1] * step_time - ((4 * ay[i][-1] - ay[i][-2]) * step_time ** 2) / 6)
        for i in range(n):
            ax[i].append(get_a(i, x, y, density, spaceDensity, vx, planets, 1))  ##a_n+1
            ay[i].append(get_a(i, y, x, density, spaceDensity, vx, planets, 0))
        for i in range(n):
            vx[i].append(vx[i][-1] + (2 * ax[i][-1] + 5 * ax[i][-2] - ax[i][-3]) * step_time / 6)
            vy[i].append(vy[i][-1] + (2 * ay[i][-1] + 5 * ay[i][-2] - ay[i][-3]) * step_time / 6)
    return t, x, y, vx, vy