import re
from math import sqrt
from tkinter import *
from tkinter import ttk
import matplotlib
from graphchart import graphchart


matplotlib.use("TkAgg")

G = 6.67e-11
M = 1.2166e30
clicked = False
planetsCount = 2
planets = [{
    'X': 0,
    'Y': 0,
    'vX': 0,
    'vY': 0,
    'M': 1.2166 * 10 ** 30,
    'E': 0,
}]
settings = {
    'timeStep': 36000,
    'totalTime': 31536000,
    'scheme': 'Эйлера-Крамера'
}


def build_chart(root, settings, planets):
    newWindow = Toplevel(root)
    newWindow.grab_set()
    graphchart(newWindow, settings, planets)
    #graphchart(newWindow, time, step_time, scheme, planets)

def create_enter_planet(frame):
    def on_entry_change(input):
        reg = '^(-?)(0|([1-9][0-9]*))(\\.[0-9]+)?$'
        if re.match(reg, input):
            return True
        else:
            return False

    def getPlanets(frame):
        global planetsCount
        global planets
        global clicked
        planetsCount = int(entry.get())
        for i in range(int(planetsCount) - 1):
            planets.append(
                {'X': float(149500000000 * (i + 1)), 'Y': float(0), 'vX': float(0), 'vY': float(sqrt((G * M) / 149500000000 / (i + 1))),
                 'M': float((i + 1) * 6.083 * 10 ** 24), 'E': float(0)})
        for widget in frame.grid_slaves():
            if widget['text'] == 'Сохранить' or widget['text'] == 'Новая система':
                widget.grid_remove()
        clicked = False
        window.destroy()
        create_settings_frame(planetsCount)

    window = Tk()
    reg = window.register(on_entry_change)
    window.title("Ввод тел")
    window.geometry("250x200")
    ttk.Label(window, text='Введите количество тел').grid(column=0, row=0, padx=55)
    entry = ttk.Entry(window, validate='key', validatecommand=(reg, '%P'))
    entry.grid(column=0, row=1, padx=55)
    ttk.Button(window, text='Ok', command=lambda: getPlanets(frame)).grid(column=0, row=2, pady=15)


def create_button_frame(container):
    frame = ttk.Frame(container)
    frame.columnconfigure(0, weight=1)

    def addButtons():
        global clicked
        if not clicked:
            ttk.Button(frame, text='Новая система', command=lambda: create_enter_planet(frame)).grid(column=0, row=1)
            ttk.Button(frame, text='Сохранить').grid(column=0, row=2)
            clicked = True
        else:
            for widget in frame.grid_slaves():
                if widget['text'] == 'Сохранить' or widget['text'] == 'Новая система':
                    widget.grid_remove()
            clicked = False
        return clicked

    ttk.Button(frame, text='Файл', command=addButtons).grid(column=0, row=0)
    ttk.Button(frame, text='Параметры', command=lambda: create_settings_frame(planetsCount)).grid(column=1, row=0)
    ttk.Button(frame, text='Запуск модели', command=lambda: build_chart(root, settings, planets)).grid(column=2, row=0)
    ttk.Button(frame, text='Остановка').grid(column=3, row=0)

    for widget in frame.winfo_children():
        widget.grid(padx=10, pady=5)

    return frame


def create_settings_frame(planetsCount):
    window = Tk()
    global settings
    global planets
    if len(planets) == 1:
        for i in range(int(planetsCount) - 1):
            print(float(sqrt(((G * M) / 149500000000) * (i + 1))))
            planets.append(
                {'X': float(149500000000 * (i + 1)), 'Y': float(0), 'vX': float(0), 'vY': float(sqrt((G * M) / 149500000000 / (i + 1))),
                 'M': float((i + 1) * 6.083 * 10 ** 24), 'E': float(0)})


    def on_entry_change(input, name):
        global settings
        reg = '^(-?)(0|([1-9][0-9]*))(\\.[0-9]+)?$'
        if re.match(reg, input):
            settings[name] = input
            return True
        else:
            return False

    # def on_sun_change(input, name):
    #     global sun
    #     #print(name)
    #     reg = '\d+[eE][+-]\d+|\d+\.?\d*|\.\d+'
    #     if re.match(reg, input):
    #         sun[name] = input
    #         return True
    #     else:
    #         return False

    def on_planets_change(input, index, key):
        global planets
        #print(planets[0][key])
        reg = '\d+[eE][+-]\d+|\d+\.?\d*|\.\d+'
        if re.match(reg, input):
            planets[int(index)][key] = float(input)
            return True
        else:
            return False

    def selected(event):
        global settings
        selection = combobox.get()
        settings['scheme'] = selection

    def toInput():
        print(settings)
        print(planets)

    window.title("Параметры")
    window.geometry("1260x500")
    frame1 = ttk.Frame(window)
    frame1.columnconfigure(0, weight=1)
    ttk.Label(frame1, text='Шаг по времени, c').grid(column=0, row=0)
    reg = window.register(on_entry_change)
    # regsun = window.register(on_sun_change)
    regplanets = window.register(on_planets_change)
    entryStep = Entry(frame1, validate="key", validatecommand=(reg, '%P', 'timeStep'))
    entryStep.grid(column=1, row=0, padx=10)
    ttk.Label(frame1, text='Время моделирования, c').grid(column=0, row=1)
    entryTotalTime = Entry(frame1, validate="key", validatecommand=(reg, '%P', 'totalTime'))
    entryTotalTime.grid(column=1, row=1, padx=10)
    schemes = ['Эйлера', 'Эйлера-Крамера', 'Верле', 'Бимана']
    schemes_var = StringVar(value=schemes[0])
    ttk.Label(frame1, text='Выбор схемы').grid(column=2, row=1)
    combobox = ttk.Combobox(frame1, textvariable=schemes_var, values=schemes)
    combobox.current(1)
    combobox.bind("<<ComboboxSelected>>", selected)
    combobox.grid(column=3, row=1)
    frame1.grid(column=1, row=0)
    columns = ("№", "X", "Y", "vX", "vY", "M")
    frameTable = ttk.Frame(window)
    frameTable.columnconfigure(0, weight=1)
    frameTable.grid(column=1, row=1)
    for i in range(len(columns)):
        ttk.Label(frameTable, text=columns[i], borderwidth=2, relief="ridge", width=30,
                  justify=CENTER).grid(column=i, row=0)
    for i in range(planetsCount):
        ttk.Label(frameTable, text=i, justify=CENTER).grid(column=0, row=i + 1)
    # for i in sun:
    #     if i == 'E':
    #         break
    #     e1 = ttk.Entry(frameTable, validate="key", validatecommand=(regsun, '%P', i), width=30)
    #     e1.grid(column=list(sun.keys()).index(i) + 1, row=1)
    #     e1.insert(0, sun[i])
    for item in planets:
        for value in item:
            if value == 'E':
                break
            e2 = ttk.Entry(frameTable, validate="key", validatecommand=(regplanets, '%P', planets.index(item), value), width=30)
            e2.grid(column=list(item.keys()).index(value) + 1, row=planets.index(item) + 1)
            e2.insert(0, item[value])

    ttk.Button(frame1, text='Ввод', command=toInput).grid(column=5, row=0)


root = Tk()
root.title("Математическое моделирование")
root.geometry('1080x720')
ttk.Style().theme_use("alt")
button_frame = create_button_frame(root)
button_frame.pack(anchor=NW)
root.mainloop()
