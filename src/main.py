import tkinter as tk

from time import time_ns
from random import randint

from render import H2O

window = tk.Tk()
window.title("Water")
window.geometry("1280x720")
canvas = tk.Canvas(window, width=1280, height=720);

presets = {
    "solid": {
        "frame_rate": 24,
        "rotation_rate_range": (1, 2),
        "velocity_range": ((0, 1), (0, 1))
    },
    "liquid": {
        "frame_rate": 60,
        "rotation_rate_range": (1, 2),
        "velocity_range": ((-2, 2), (-2, 2))
    },
    "gas": {
        "frame_rate": 60,
        "rotation_rate_range": (1, 10),
        "velocity_range": ((-10, 10), (-10, 10))
    }
}

molecules = []
def generate(preset: str):
    global presets
    global molecules

    preset = presets[preset]

    if molecules == []:
        for i in range(50):
            h2o = H2O((randint(100, 1080), randint(100, 520)), rotation=randint(-180, 180), rotation_rate=randint(preset["rotation_rate_range"][0], preset["rotation_rate_range"][1]), velocity=(randint(preset["velocity_range"][0][0], preset["velocity_range"][0][1]), randint(preset["velocity_range"][1][0], preset["velocity_range"][1][1])))
            molecules.append(h2o)

    # molecules = []
    for molecule in molecules:
        molecule.rotation_rate = randint(preset["rotation_rate_range"][0], preset["rotation_rate_range"][1])
        molecule.velocity = (randint(preset["velocity_range"][0][0], preset["velocity_range"][0][1]), randint(preset["velocity_range"][1][0], preset["velocity_range"][1][1]))

temperature_slider = tk.Scale(window, from_=-50, to=150, tickinterval=20, length=int(canvas["height"]) - 20)
temperature_slider.place(x = 1080 + 190, y = 10, anchor=tk.NE) # x = int(window.winfo_screenwidth()) - 300, y = 10)

print(window.winfo_width())

state = tk.StringVar(window, value="state: solid")

state_label = tk.Label(window, textvariable=state)
state_label.place(x = 10, y = 10)

frame_rate = 60
current_state = "solid"
def updateState(event):
    global current_state
    global temperature_slider
    global state
    global frame_rate

    temperature = temperature_slider.get()

    if temperature <= 0 and current_state != "solid":
        frame_rate = presets["solid"]["frame_rate"]
        current_state = "solid"
        generate("solid")


    if 0 < temperature < 100 and current_state != "liquid":
        frame_rate = presets["liquid"]["frame_rate"]
        current_state = "liquid"
        generate("liquid")
        
    if temperature >= 100 and current_state != "gas":
        frame_rate = presets["gas"]["frame_rate"]
        current_state = "gas"
        generate("gas")
    
    state.set(f"state: {current_state}")

generate(current_state)

temperature_slider.bind("<ButtonRelease-1>", updateState)

def render():
    canvas.delete("all")

    for molecule in molecules:
        molecule.update(canvas)
    
    window.after(int(1000 / frame_rate), render)

render()

canvas.pack()
window.mainloop()
