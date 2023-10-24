import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
from matplotlib.widgets import Button
import tkinter.filedialog as fd
from computations import scheme_Euler, scheme_Euler_Kramer, scheme_Verle, scheme_Biman
mpl.use('TkAgg')


colors = ["red", "blue", "green", "black", "orange", "peru", "aqua", "pink", "olive", "lime"]
len_colors = 10
G = 6.67e-11
button = None
line_ani = None
def _vxy(v, planets, general_m, n):
    impulse = 0
    for i in range(len(planets)):
        impulse += v[i][n] * planets[i]['M']
    return impulse / general_m
def _energy(x, y, vx, vy, planets, n):
    energy = 0
    for i in range(len(planets)):
        energy += planets[i]['M'] * (vx[i][n] ** 2 + vy[i][n] ** 2) / 2
    for i in range(len(planets)):
        for j in range(i + 1, len(planets)):
            energy -= G * planets[i]['M'] * planets[j]['M'] / ((x[i][n] - x[j][n]) ** 2 + (y[i][n] - y[j][n]) ** 2) ** 0.5
    return energy

def graphchart(win, settings, planets):
    time = int(settings['totalTime'])
    step_time = int(settings['timeStep'])
    scheme = settings['scheme']
    def to_file(event):
        data = ''
        for i in planets:
            data += f"x={i['X']} y={i['Y']} vx={i['vX']} vy={i['vY']} m={i['M']} \n"
        last = len(vx[0]) - 1
        vxF = _vxy(vx, planets, general_m, last)
        vyF = _vxy(vy, planets, general_m, last)
        energy = _energy(x, y, vx, vy, planets, last)
        data += f'\nvX Final = {vxF} vY Final = {vyF} Energy Final = {energy}'
        new_file = fd.asksaveasfile(title="Сохранить файл", defaultextension=".txt",
                                    filetypes=(("Текстовый файл", "*.txt"),))

        if new_file:
            new_file.write(data)
            new_file.close()

    def animate_func(num):
            global button

            ax.clear()  # Очищаем фигуру для обновления линии, точки,
            # заголовка и осей  # Обновляем линию траектории (num+1 из-за индексации Python)
            for i in range(len(planets)):
                ax.plot(x[i][:num + 1], y[i][:num + 1], color=colors[i % len_colors])
                         # Обновляем локацию точки
                ax.scatter(x[i][num], y[i][num], color=colors[i % len_colors])  # Добавляем постоянную начальную точку

            ax.set_xlim([xmin - (xmax - xmin) * 0.2, xmax + (xmax - xmin) * 0.2])
            ax.set_ylim([ymin - (ymax - ymin) * 0.2, ymax + (ymax - ymin) * 0.2])
            vxm = _vxy(vx, planets, general_m, num)
            vym = _vxy(vy, planets, general_m, num)
            energy = _energy(x, y, vx, vy, planets, num)
            # Добавляем метки
            ax.set_title(f'Время = {str(np.round(t[num], decimals=2))} sec \n'
                        f'Vx = {vxm} \n'
                        f'Vy = {vym} \n'
                        f'E = {energy}', bbox=dict(boxstyle='round', fc='w'))
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            button = Button(button_place, 'Save')
            button.on_clicked(to_file)
    if scheme == 'Эйлера-Крамера':
        t, x, y, vx, vy = scheme_Euler_Kramer(time, step_time, planets)
    elif scheme == 'Эйлера':
        t, x, y, vx, vy = scheme_Euler(time, step_time, planets)
    elif scheme == 'Верле':
        t, x, y, vx, vy = scheme_Verle(time, step_time, planets)
    elif scheme == 'Бимана':
        t, x, y, vx, vy = scheme_Biman(time, step_time, planets)
    general_m = sum([i['M'] for i in planets])
    xmin = xmax = x[0][0]
    ymin = ymax = y[0][0]
    for i in range(len(planets)):
        for j in range(len(x[0])):
            if xmin > x[i][j]:
                xmin = x[i][j]
            if xmax < x[i][j]:
                xmax = x[i][j]
            if ymin > y[i][j]:
                ymin = y[i][j]
            if ymax < y[i][j]:
                ymax = y[i][j]
    fig = plt.figure(figsize=(7, 7))
    ax = plt.axes()
    ax.set_facecolor("black")
    button_place = plt.axes((0.40, 0.005, 0.15, 0.04))
    global line_ani
    line_ani = animation.FuncAnimation(fig, animate_func, interval=1,
                                       frames=len(x[0]), repeat=False)
    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.draw()

    canvas.get_tk_widget().pack()

    toolbar = NavigationToolbar2Tk(canvas, win)
    toolbar.update()

    canvas.get_tk_widget().pack()